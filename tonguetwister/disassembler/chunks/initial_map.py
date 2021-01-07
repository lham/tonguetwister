from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.lib.byte_block_io import ByteBlockIO


class InitialMap(ChunkParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['mmap_address']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['mmap_count'] = stream.uint32()
        data['mmap_address'] = stream.uint32()
        data['?version'] = stream.uint32()
        data['u1'] = stream.uint32()
        data['u2'] = stream.uint32()
        data['u3'] = stream.uint32()

        return data
