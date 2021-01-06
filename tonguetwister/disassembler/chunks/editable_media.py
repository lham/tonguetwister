from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class EditableMedia(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['data'] = stream.read_bytes()

        return header
