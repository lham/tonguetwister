from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class BitmapData(Chunk):
    RLE_BREAK_POINT = 128

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        # Probably using https://en.wikipedia.org/wiki/PackBits algorithm
        data = OrderedDict()
        data['rle_data'] = rle = []

        while not stream.is_depleted():
            header_byte = stream.uint8()
            if header_byte >= BitmapData.RLE_BREAK_POINT:
                rle.append((header_byte, stream.uint8()))
            else:
                rle.append((header_byte, stream.read_bytes(header_byte + 1)))

        return data

    def decode_rle_data(self, palette):
        image_data = []
        for header_byte, palette_indices in self.body['rle_data']:
            if header_byte >= BitmapData.RLE_BREAK_POINT:
                color_tuple = palette[palette_indices]  # In this case, palette_indices is a singular int value
                length = (0x100 - header_byte) + 1  # Two's complement of an 8bit byte + 1
                color_data = [color_tuple for _ in range(length)]
            else:
                color_data = [palette[index] for index in palette_indices]

            image_data.extend(color_data)

        return image_data
