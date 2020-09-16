from collections import OrderedDict

from tonguetwister.chunks.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class CastKeyMap(RecordsChunk):
    @classmethod
    def _set_endianess(cls, stream: ByteBlockIO):
        stream.set_little_endian()

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['n_records'] = stream.uint32()
        header['n_used_record_slots'] = stream.uint32()

        return header

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        return [MapEntry.parse(stream, header, i) for i in range(header['n_records'])]

    def find_resource_chunk_mmap_id_by_cast_member_mmap_id(self, cast_mmap_id):
        for i, record in enumerate(self.records):
            if record.cast_mmap_id == cast_mmap_id:
                return record.mmap_id

        return -1


class MapEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['active'] = index < parent_header['n_used_record_slots']
        data['mmap_id'] = stream.uint32()
        data['cast_mmap_id'] = stream.uint32()
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])

        return data

    @property
    def cast_mmap_id(self):
        return self.data['cast_mmap_id']

    @property
    def mmap_id(self):
        return self.data['mmap_id']
