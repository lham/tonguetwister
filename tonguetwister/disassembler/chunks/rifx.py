from tonguetwister.disassembler.chunk import ChunkParser
from tonguetwister.lib.byte_block_io import ByteBlockIO


class Rifx(ChunkParser):
    public_data_attrs = ['version']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['version'] = stream.uint32()

        return data
