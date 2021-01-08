from tonguetwister.disassembler.chunks.bitmap_data import BitmapData
from tonguetwister.disassembler.chunks.castmembers.palette import PaletteCastMember
from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.lib.stream import ByteBlockIO


class Thumbnail(ChunkParser):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['header_length'] = stream.uint16()
        data['top'] = stream.int16()
        data['left'] = stream.int16()
        data['bottom'] = stream.int16()
        data['right'] = stream.int16()
        data['image_data_length'] = image_data_length = stream.uint32()
        data['data'] = stream.read_bytes(image_data_length)

        return data

    @property
    def width(self):
        return self._data['right'] - self._data['left']

    @property
    def height(self):
        return self._data['bottom'] - self._data['top']

    def image_data(self):
        bit_depth = 8
        bytes_per_row = self.width + (0 if (self.width % 2 == 0) else 1)
        palette = 0  # Mac palette

        return BitmapData.unpack_bitmap_data(
            ByteBlockIO(self._data['data']),
            self.width,
            self.height,
            bit_depth,
            bytes_per_row,
            PaletteCastMember.get_predefined_palette(bit_depth, palette)
        )
