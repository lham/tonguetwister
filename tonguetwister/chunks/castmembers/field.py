from collections import OrderedDict

from tonguetwister.chunks.castmembers.core import SpecificCastMember
from tonguetwister.lib.byte_block_io import ByteBlockIO


# noinspection DuplicatedCode
class FieldCastMember(SpecificCastMember):
    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        data = OrderedDict()
        data['u1'] = stream.uint32()
        data['u2'] = stream.uint32()
        data['u3'] = stream.uint32()
        data['u4'] = stream.uint32()
        data['u5'] = stream.uint32()
        data['u6'] = stream.uint32()
        data['u7'] = stream.uint32()
        data['u8'] = stream.uint32()
        data['u9'] = stream.uint16()
        data['u10'] = stream.uint32()
        data['u11'] = stream.uint32()
        data['u12'] = stream.uint32()
        data['u13'] = stream.uint32()
        data['u14'] = stream.uint32()
        data['u15'] = stream.uint32()
        data['u16'] = stream.uint32()
        data['u17'] = stream.uint32()
        data['u18'] = stream.uint32()

        data['text_length'] = stream.uint8()
        data['text'] = stream.string(data['text_length'])

        return data

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        footer = OrderedDict()
        footer['c1'] = (stream.uint16(), stream.uint16(), stream.uint16())
        footer['c2'] = (stream.uint16(), stream.uint16(), stream.uint16())
        footer['c3'] = (stream.uint16(), stream.uint16(), stream.uint16())
        footer['u1'] = stream.uint8()
        footer['u2'] = stream.uint8()
        footer['u3'] = stream.uint8()
        footer['u4'] = stream.uint8()
        footer['u5'] = stream.uint8()
        footer['u6'] = stream.uint8()
        footer['u7'] = stream.uint8()
        footer['u8'] = stream.uint8()
        footer['u9'] = stream.uint8()
        footer['u10'] = stream.uint8()
        footer['u11'] = stream.uint8()

        return footer
