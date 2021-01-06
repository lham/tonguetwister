from tonguetwister.disassembler.chunk import EntryMapChunk, InternalChunkEntry
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class ResourceKeyTable(EntryMapChunk):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['header_length'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['n_record_slots'] = stream.uint32()
        header['n_record_slots_used'] = stream.uint32()

        return header

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        return [ResourceKeyTableEntry.parse(stream, header, i) for i in range(header['n_record_slots'])]


class ResourceKeyTableEntry(InternalChunkEntry):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['parent_resource_id', 'resource_id', 'four_cc']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO, header, index):
        data = {}
        data['active'] = index < header['n_record_slots_used']
        data['resource_id'] = stream.uint32()
        data['parent_resource_id'] = stream.uint32()
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])

        return data

    def is_active(self):
        return self._data['active']
