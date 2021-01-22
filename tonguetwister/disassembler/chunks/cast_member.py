import logging
from collections import OrderedDict

from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.disassembler.mappings.castmembers import CastMemberTypeMapping
from tonguetwister.lib.stream import ByteBlockIO

logger = logging.getLogger('tonguetwister.disassembler.cast_member')
logger.setLevel(logging.DEBUG)


class CastMember(ChunkParser):
    sections = ['header', 'body', 'footer']

    @classmethod
    def parse(cls, stream: ByteBlockIO):
        stream.set_endianess(cls.endianess)
        header = cls.parse_header(stream)

        mapping = CastMemberTypeMapping.get()
        if mapping[header['media_type']] is not None:
            return mapping[header['media_type']].parse_member(stream, header)

        logger.warning(f'Unknown media type ({header["media_type"]}) for cast member.')
        stream.read_bytes()

        return cls(**{'header': header, 'body': None, 'footer': None})

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['media_type'] = stream.uint32()
        header['data_length'] = stream.uint32()
        header['footer_length'] = stream.uint32()

        return header

    @classmethod
    def parse_member(cls, stream: ByteBlockIO, generic_header):
        data = cls._parse_member_data(stream, generic_header['data_length'])
        footer = cls._parse_member_footer(stream, generic_header['footer_length'])

        return cls(**{'header': generic_header, 'body': data, 'footer': footer})

    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        return None

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        return None

    @property
    def type_name(self):
        mapping = CastMemberTypeMapping.get()
        type_specific_parser = mapping[self._header['media_type']]

        if type_specific_parser is not None:
            return type_specific_parser.__name__

        return 'Unknown'
