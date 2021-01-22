from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class ResourceAssocTableEntry(InternalEntryParser):
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


class ResourceAssocTable(EntryMapChunkParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN
    entry_class = ResourceAssocTableEntry

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['header_length'] = stream.uint16()
        header['entry_length'] = stream.uint16()
        header['allocated_array_elements'] = stream.uint32()
        header['used_array_elements'] = stream.uint32()

        return header
