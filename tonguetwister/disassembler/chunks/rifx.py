from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class Rifx(Chunk):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['version'] = stream.uint32()

        return data

    @property
    def version(self):
        return self._data['version']
