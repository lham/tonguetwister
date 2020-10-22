from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class FontXtraMap(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['font_map'] = stream.string_raw(stream.size())

        return header

    @property
    def font_map(self):
        return self.header['font_map']
