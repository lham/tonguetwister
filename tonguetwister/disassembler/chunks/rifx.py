from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.lib.stream import ByteBlockIO


class Rifx(ChunkParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['version']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['version'] = stream.string_raw(4)

        return data
