from collections import OrderedDict

from tonguetwister.chunks.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import maybe_encode_bytes


class MemoryMap(RecordsChunk):
    @classmethod
    def _set_endianess(cls, stream: ByteBlockIO):
        stream.set_little_endian()

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['n_four_cc_available'] = stream.uint32()
        header['n_four_cc_used'] = stream.uint32()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['first_empty_idx'] = stream.uint32()  # Free pointer

        return header

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        return [MapEntry.parse(stream, header, i) for i in range(header['n_four_cc_available'])]

    def find_record_id_by_address(self, address):
        for i, record in enumerate(self.records):
            if record.address == address:
                return i

        return -1


class MapEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['active'] = index < parent_header['n_four_cc_used']
        data['four_cc'] = maybe_encode_bytes(stream.string_raw(4), data['active'])
        data['block_length'] = stream.uint32()
        data['block_address'] = stream.uint32()
        data['protected_flag'] = stream.uint32()
        data['u1'] = stream.uint32()

        return data

    @property
    def address(self):
        return self.data['block_address']
