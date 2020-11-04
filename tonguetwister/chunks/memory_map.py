from collections import OrderedDict

from tonguetwister.chunks.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class MemoryMap(RecordsChunk):
    @classmethod
    def _set_big_endianess(cls, stream: ByteBlockIO):
        stream.set_little_endian()

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['n_record_slots'] = stream.uint32()
        header['n_record_slots_used'] = stream.uint32()
        header['last_junk_record_id'] = stream.int32()
        header['?last_prev_mmap_id'] = stream.int32()
        header['first_empty_record_id'] = stream.int32()  # Free pointer

        return header

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        return [MapEntry.parse(stream, header, i) for i in range(header['n_record_slots'])]

    def find_record_id_by_address(self, address):
        for i, record in enumerate(self.records):
            if record.address == address:
                return i

        return -1


class MapEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['record_address'] = stream.tell()
        data['active'] = index < parent_header['n_record_slots_used']
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])
        data['chunk_length'] = stream.uint32()
        data['chunk_address'] = stream.uint32()
        data['flags'] = stream.uint32()
        data['u1'] = stream.uint16()
        data['u2'] = stream.uint16()

        return data

    @property
    def address(self):
        return self.data['chunk_address']
