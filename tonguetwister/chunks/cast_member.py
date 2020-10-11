from collections import OrderedDict

from tonguetwister.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.chunks.castmembers.field import FieldCastMember
from tonguetwister.chunks.castmembers.script import ScriptCastMember
from tonguetwister.chunks.castmembers.shape import ShapeCastMember
from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class CastMember(Chunk):
    CAST_MEMBER_TYPES = [
        None,
        BitmapCastMember,
        None,
        FieldCastMember,
        None,
        None,
        None,
        None,
        ShapeCastMember,
        None,
        None,
        ScriptCastMember,
        None,
        None,
        None,
        None,
        None,
        None,
        None
    ]

    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        cls._set_big_endianess(stream)
        header = cls._parse_header(stream)

        if cls.CAST_MEMBER_TYPES[header['media_type']] is not None:
            return cls.CAST_MEMBER_TYPES[header['media_type']].parse_member(stream, address, four_cc, header)

        print(f'WARNING: Unknown media type ({header["media_type"]}).')
        stream.read_bytes()

        return cls(address, four_cc, header, None, None)

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['media_type'] = stream.uint32()
        header['data_length'] = stream.uint32()
        header['footer_length'] = stream.uint32()

        return header
