from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper, twos_complement


class BitmapData(Chunk):
    DEFAULT_ALPHA = 255
    RLE_BREAK_POINT = 0x80

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        data = OrderedDict()
        data['run_length_encoded_data'] = stream.read_bytes()
        data['byte_string'] = grouper(data['run_length_encoded_data'], 2)

        return data

    def decode_32bit_rle_data(self, width, height):
        stream = ByteBlockIO(self.body['run_length_encoded_data'])
        image_data = []

        # The data might be not be encoded, if so just read and return the data
        if stream.size() == width * height * 4:
            while not stream.is_depleted():
                color_tuple = [stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8()]
                color_tuple[0] = BitmapData.DEFAULT_ALPHA  # see ImageRow.to_list() for explanation
                image_data.append(color_tuple)

            return image_data

        # Decode the image data
        image_row = ImageRow(width)
        while not stream.is_depleted():
            header_byte = stream.uint8()

            if header_byte < BitmapData.RLE_BREAK_POINT:
                length = header_byte + 1
                byte_list = [stream.uint8() for _ in range(length)]
                image_row.add_byte_list(byte_list)
            else:
                length = twos_complement(header_byte) + 1
                byte = stream.uint8()
                image_row.add_duplicated_byte(length, byte)

            if image_row.is_complete():
                image_data.extend(image_row.to_list())
                image_row.reset()

        return image_data

    # Probably using https://en.wikipedia.org/wiki/PackBits algorithm
    def decode_8bit_rle_data(self, palette):
        stream = ByteBlockIO(self.body['run_length_encoded_data'])
        image_data = []

        while not stream.is_depleted():
            header_byte = stream.uint8()

            if header_byte < BitmapData.RLE_BREAK_POINT:
                length = header_byte + 1
                palette_indices = stream.read_bytes(length)
                color_data = [palette[index] for index in palette_indices]
            else:
                length = twos_complement(header_byte) + 1
                palette_index = stream.uint8()
                color_data = [palette[palette_index] for _ in range(length)]

            image_data.extend(color_data)

        return image_data


class ImageRow:
    def __init__(self, width):
        self.width = width
        self._a = []
        self._r = []
        self._g = []
        self._b = []

    def is_complete(self):
        return len(self._a) == len(self._r) == len(self._g) == len(self._b) == self.width

    def add_duplicated_byte(self, n_duplications, byte):
        self._next_channel().extend([byte] * n_duplications)

    def add_byte_list(self, byte_list):
        self._next_channel().extend(byte_list)

    def to_list(self):
        # Director 6 doesn't seem to support an alpha value, but encodes a zero byte anyway. Simply replace it!
        self._a = [BitmapData.DEFAULT_ALPHA] * self.width

        return list(zip(self._a, self._r, self._g, self._b))

    def reset(self):
        self._a = []
        self._r = []
        self._g = []
        self._b = []

    def _next_channel(self):
        if len(self._a) < self.width:
            return self._a
        if len(self._r) < self.width:
            return self._r
        if len(self._g) < self.width:
            return self._g
        if len(self._b) < self.width:
            return self._b
        raise RuntimeError('Next channel does not exist')
