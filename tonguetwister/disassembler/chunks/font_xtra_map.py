from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.lib.stream import ByteBlockIO


class FontXtraMap(ChunkParser):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        header = {}
        header['font_map'] = stream.string_raw(stream.size())

        return header

    @property
    def font_map(self):
        return self._data['font_map']
