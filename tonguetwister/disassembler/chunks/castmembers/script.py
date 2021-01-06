from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.lib.byte_block_io import ByteBlockIO


# noinspection DuplicatedCode
class ScriptCastMember(CastMember):
    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        data = {}
        data['u1'] = stream.uint32()

        data['script_number'] = (stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8())
        data['u6'] = stream.uint32()
        data['u7'] = stream.uint32()

        data['script_id'] = stream.uint32()
        data['u9'] = stream.uint32()
        data['u10'] = stream.uint32()
        data['u11'] = stream.uint32()
        stream.read_bytes()

        return data

        data['u12'] = stream.uint16()
        data['u13'] = stream.uint32()
        data['u14'] = stream.uint32()
        data['u15'] = stream.uint32()
        data['u16'] = stream.uint32()
        data['u17'] = stream.uint32()
        data['u18'] = stream.uint32()
        data['u19'] = stream.uint32()
        data['u20'] = stream.uint32()
        data['u21'] = stream.uint32()
        data['u22'] = stream.uint32()
        data['u23'] = stream.uint32()
        data['u24'] = stream.uint32()
        data['u25'] = stream.uint32()
        data['u26'] = stream.uint32()

        data['u27'] = stream.uint32()
        if data['u15'] > 0:
            data['text'] = stream.string_auto()

        data['u28'] = stream.uint8()
        data['u29'] = stream.uint8()
        data['u30'] = stream.uint8()
        data['u31'] = stream.uint8()
        data['u32'] = stream.uint8()
        data['u33'] = stream.uint8()
        data['u34'] = stream.uint8()
        data['u35'] = stream.uint8()

        return data

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        footer = {}
        #footer['u1'] = stream.uint8()
        #footer['u2'] = stream.uint8()

        return footer
