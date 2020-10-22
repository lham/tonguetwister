from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class VideoWorksScore(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['data'] = stream.read_bytes()
        header['data-bytes'] = grouper(header['data'], 4)

        return header
