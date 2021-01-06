from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class FontXtraMap(Chunk):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        header = {}
        header['font_map'] = stream.string_raw(stream.size())

        return header

    @property
    def font_map(self):
        return self._data['font_map']
