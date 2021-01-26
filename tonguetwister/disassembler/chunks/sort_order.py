from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class CastMemberReferenceEntry(InternalEntryParser):
    public_data_attrs = ['cast_number', 'cast_member_slot_number']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['cast_number'] = stream.uint16()
        data['cast_member_slot_number'] = stream.uint16()

        return data


class SortOrder(EntryMapChunkParser):
    entry_class = CastMemberReferenceEntry

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['allocated_array_elements'] = stream.uint32()
        header['used_array_elements'] = stream.uint32()
        header['header_length'] = stream.uint16()
        header['entry_length'] = stream.uint16()

        return header
