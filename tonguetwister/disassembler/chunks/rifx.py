from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.lib.stream import ByteBlockIO


class Rifx(ChunkParser):
    public_data_attrs = ['version']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['version'] = stream.uint32()

        return data
