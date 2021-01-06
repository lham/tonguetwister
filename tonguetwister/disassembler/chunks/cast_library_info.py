from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class CastLibraryInfo(Chunk):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['u1'] = stream.uint32()
        data['skip_length'] = stream.uint16()
        data['ux'] = stream.read_bytes(2 * data['skip_length'])
        data['u2'] = stream.uint32()
        data['u3'] = stream.uint32()
        data['body_length'] = stream.uint32()

        # body['u1'] = stream.read_bytes(20)
        # body['text_length'] = stream.uint8()
        # body['text'] = stream.string(body['text_length'])
        # stream.read_pad(1)
        stream.read_bytes()

        return data
