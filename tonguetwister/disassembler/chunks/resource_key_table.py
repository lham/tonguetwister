from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalChunkEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class ResourceKeyTable(EntryMapChunkParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['header_length'] = stream.uint16()
        header['entry_length'] = stream.uint16()
        header['allocated_array_elements'] = stream.uint32()
        header['used_array_elements'] = stream.uint32()

        return header

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        entries = [ResourceKeyTableEntry.parse(stream) for _ in range(header['used_array_elements'])]

        # Read the allocated but unused array slots
        stream.read_bytes(header['entry_length'] * (header['allocated_array_elements'] - header['used_array_elements']))

        return entries


class ResourceKeyTableEntry(InternalChunkEntryParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['parent_resource_id', 'child_resource_id', 'child_four_cc']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['child_resource_id'] = stream.uint32()
        data['parent_resource_id'] = stream.uint32()
        data['child_four_cc'] = stream.string_raw(4)

        return data

    @property
    def primary_key(self):
        return self.parent_resource_id, self.child_four_cc
