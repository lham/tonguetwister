from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class InitialMap(Chunk):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['mmap_count'] = stream.uint32()
        header['mmap_address'] = stream.uint32()
        header['?version'] = stream.uint32()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['u3'] = stream.uint32()

        return header

    @property
    def mmap_address(self):
        return self.header['mmap_address']
