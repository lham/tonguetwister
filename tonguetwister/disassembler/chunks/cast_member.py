import logging
from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.disassembler.mappings.cast_member_types import CastMemberTypeMapping
from tonguetwister.lib.byte_block_io import ByteBlockIO

logger = logging.getLogger('tonguetwister.disassembler.cast_member')
logger.setLevel(logging.DEBUG)


class CastMember(Chunk):
    sections = ['header', 'body', 'footer']

    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        stream.set_endianess(cls.endianess)
        header = cls.parse_header(stream)

        mapping = CastMemberTypeMapping.get()
        if mapping[header['media_type']] is not None:
            return mapping[header['media_type']].parse_member(stream, address, four_cc, header)

        logger.warning(f'Unknown media type ({header["media_type"]}) for cast member.')
        stream.read_bytes()

        return cls(address, four_cc, **{'header': header, 'body': None, 'footer': None})

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['media_type'] = stream.uint32()
        header['data_length'] = stream.uint32()
        header['footer_length'] = stream.uint32()

        return header

    @classmethod
    def parse_member(cls, stream: ByteBlockIO, address, four_cc, generic_header):
        data = cls._parse_member_data(stream, generic_header['data_length'])
        footer = cls._parse_member_footer(stream, generic_header['footer_length'])

        return cls(address, four_cc, **{'header': generic_header, 'body': data, 'footer': footer})

    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        return None

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        return None
