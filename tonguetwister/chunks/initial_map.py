from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class InitialMap(Chunk):
    @classmethod
    def _set_endianess(cls, stream: ByteBlockIO):
        stream.set_little_endian()

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['mmap_count'] = stream.uint32()
        header['mmap_offset'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['u3'] = stream.uint32()
        header['u4'] = stream.uint32()
        header['u5'] = stream.uint32()

        return header
