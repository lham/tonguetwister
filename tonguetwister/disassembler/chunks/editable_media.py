from collections import OrderedDict

from tonguetwister.disassembler.chunk import ChunkParser
from tonguetwister.lib.byte_block_io import ByteBlockIO


class EditableMedia(ChunkParser):
    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['data'] = stream.read_bytes()

        return header
