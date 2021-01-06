from collections import OrderedDict

from tonguetwister.disassembler.chunks.bitmap_data import BitmapData
from tonguetwister.disassembler.chunks.castmembers.palette import PaletteCastMember
from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class Thumbnail(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint16()
        header['top'] = stream.int16()
        header['left'] = stream.int16()
        header['bottom'] = stream.int16()
        header['right'] = stream.int16()
        header['data_length'] = stream.uint32()

        return header

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        body = OrderedDict()
        body['data'] = stream.read_bytes(header['data_length'])
        body['data_as_bytes'] = grouper(body['data'], 2)

        return body

    @property
    def width(self):
        return self.header['right'] - self.header['left']

    @property
    def height(self):
        return self.header['bottom'] - self.header['top']

    def image_data(self):
        bit_depth = 8
        bytes_per_row = self.width + (0 if (self.width % 2 == 0) else 1)
        palette = 0  # Mac palette

        return BitmapData.unpack_bitmap_data(
            ByteBlockIO(self.body['data']),
            self.width,
            self.height,
            bit_depth,
            bytes_per_row,
            PaletteCastMember.get_predefined_palette(bit_depth, palette)
        )
