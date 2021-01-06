from tonguetwister.disassembler.chunk import EntryMapChunk, InternalChunkEntry
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class CastKeyMap(EntryMapChunk):
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
        return [CastKeyMapEntry.parse(stream, header, i) for i in range(header['n_record_slots'])]

    def find_resource_chunk_mmap_id_by_cast_member_mmap_id(self, cast_mmap_id):
        for i, record in enumerate(self.entires):
            if record.cast_mmap_id == cast_mmap_id:
                return record.mmap_id

        return -1


class CastKeyMapEntry(InternalChunkEntry):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['cast_mmap_id', 'mmap_id', 'four_cc']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO, header, index):
        data = {}
        data['active'] = index < header['n_record_slots_used']
        data['mmap_id'] = stream.uint32()
        data['cast_mmap_id'] = stream.uint32()
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])

        return data

    def is_active(self):
        return self._data['active']

    @property
    def parent_resource_id(self):
        return self.cast_mmap_id

    @property
    def child_resource_id(self):
        return self.mmap_id
