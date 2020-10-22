from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk, RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class SortOrder(RecordsChunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['?n_record_slots_total'] = stream.uint32()
        header['?n_record_slots_used'] = stream.uint32()
        header['u3'] = stream.uint16()
        header['?record_length'] = stream.uint16()

        return header

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        return [CastMemberEntry.parse(stream, header, i) for i in range(header['?n_record_slots_total'])]


class CastMemberEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['cast_lib'] = stream.uint16()
        data['cast_slot'] = stream.uint16()

        return data
