from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class CastLibraryInfo(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['skip_length'] = stream.uint16()
        header['ux'] = stream.read_bytes(2 * header['skip_length'])
        header['u2'] = stream.uint32()
        header['u3'] = stream.uint32()
        header['body_length'] = stream.uint32()

        return header

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        body = OrderedDict()
        # body['u1'] = stream.read_bytes(20)
        # body['text_length'] = stream.uint8()
        # body['text'] = stream.string(body['text_length'])
        # stream.read_pad(1)
        stream.read_bytes()

        return body
