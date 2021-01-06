from collections import OrderedDict

from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.lib.byte_block_io import ByteBlockIO


# noinspection DuplicatedCode
class ShapeCastMember(CastMember):
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
        data['u10'] = stream.uint16()
        data['u11'] = stream.uint16()
        data['u12'] = stream.uint16()
        data['u13'] = stream.uint16()
        data['u14'] = stream.uint16()
        data['record_length'] = stream.uint16()
        data['text'] = stream.string_auto()

        return data

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        footer = OrderedDict()
        footer['u1'] = stream.uint16()
        footer['u2'] = stream.uint16()
        footer['u3'] = stream.uint16()
        footer['u4'] = stream.uint16()
        footer['u5'] = stream.uint16()
        footer['u6'] = stream.uint16()
        footer['u7'] = stream.uint8()
        footer['u8'] = stream.uint8()
        footer['u9'] = stream.uint8()
        footer['u10'] = stream.uint8()
        footer['u11'] = stream.uint8()

        return footer
