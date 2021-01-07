from tonguetwister.disassembler.chunk import EntryMapChunkParser, InternalChunkEntryParser
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class MemoryMap(EntryMapChunkParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['header_length'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['n_record_slots'] = stream.uint32()
        header['n_record_slots_used'] = stream.uint32()
        header['last_junk_record_id'] = stream.int32()
        header['?last_prev_mmap_id'] = stream.int32()
        header['first_empty_record_id'] = stream.int32()  # Free pointer

        return header

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        return [MemoryMapEntry.parse(stream, header, i) for i in range(header['n_record_slots'])]

    def find_record_id_by_address(self, address):
        for i, record in enumerate(self.entires):
            if record.address == address:
                return i

        return -1


class MemoryMapEntry(InternalChunkEntryParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['four_cc', 'index', 'chunk_length', 'chunk_address']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO, header, index):
        data = {}
        data['record_address'] = stream.tell()
        data['index'] = index
        data['active'] = index < header['n_record_slots_used']
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])
        data['chunk_length'] = stream.uint32()
        data['chunk_address'] = stream.uint32()
        data['flags'] = stream.uint32()
        data['u1'] = stream.uint16()
        data['u2'] = stream.uint16()

        return data

    def is_active(self):
        return self._data['active'] and self._data['four_cc'] != 'free' and self._data['four_cc'] != 'junk'

    @property
    def address(self):
        return self._data['chunk_address']
