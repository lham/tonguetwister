from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class SpecificCastMember(Chunk):
    @classmethod
    def parse_member(cls, stream: ByteBlockIO, four_cc, generic_header):
        data = cls._parse_member_data(stream, generic_header['data_length'])
        footer = cls._parse_member_footer(stream, generic_header['footer_length'])

        return cls(four_cc, generic_header, data, footer)

    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        return None

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        return None
