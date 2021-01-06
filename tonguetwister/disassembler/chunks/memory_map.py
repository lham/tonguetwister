from collections import OrderedDict

from tonguetwister.disassembler.chunk import RecordsChunk, InternalChunkRecord, UndefinedChunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class MemoryMap(RecordsChunk):
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
    def parse_records(cls, stream: ByteBlockIO, header):
        return [MemoryMapEntry.parse(stream, header, i) for i in range(header['n_record_slots'])]

    def find_record_id_by_address(self, address):
        for i, record in enumerate(self._records):
            if record.address == address:
                return i

        return -1

    @property
    def entries(self):
        return self._records


class MemoryMapEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['record_address'] = stream.tell()
        data['index'] = index
        data['active'] = index < parent_header['n_record_slots_used']
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])
        data['chunk_length'] = stream.uint32()
        data['chunk_address'] = stream.uint32()
        data['flags'] = stream.uint32()
        data['u1'] = stream.uint16()
        data['u2'] = stream.uint16()

        return data

    def get_class(self):
        from tonguetwister.disassembler.mappings.four_cc import CHUNK_MAP

        if self.data['four_cc'] not in CHUNK_MAP:
            return UndefinedChunk

        return CHUNK_MAP[self.data['four_cc']]

    def is_active(self):
        return self.data['active'] and self.data['four_cc'] != 'free' and self.data['four_cc'] != 'junk'

    @property
    def four_cc(self):
        return self.data['four_cc']

    @property
    def address(self):
        return self.data['chunk_address']

    @property
    def index(self):
        return self.data['index']
