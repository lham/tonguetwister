from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class DirectorConfig(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['chunk_length'] = stream.uint16()  # Inclusive self
        header['?version'] = stream.uint16()

        header['stage_top'] = stream.int16()
        header['stage_left'] = stream.int16()
        header['stage_bottom'] = stream.int16()
        header['stage_right'] = stream.int16()

        header['u1'] = stream.read_bytes(66)
        header['u1_b4'] = grouper(header['u1'], 4)
        header['u1_b2'] = grouper(header['u1'], 2)

        header['palette'] = stream.int16()
        header['u2'] = stream.uint32()

        return header
