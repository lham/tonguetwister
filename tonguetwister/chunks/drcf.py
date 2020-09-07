from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class DRCF(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['chunk_length'] = stream.uint16()
        header['u1'] = stream.read_bytes()

        return header
