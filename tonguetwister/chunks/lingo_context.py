from collections import OrderedDict

from tonguetwister.chunks.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class LingoContext(RecordsChunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['n_scripts'] = stream.uint32()
        header['n_scripts_2'] = stream.uint32()
        header['records_offset'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['u4'] = stream.uint16()
        header['u5'] = stream.uint16()
        header['lnam_id'] = stream.uint32()
        header['n_used?'] = stream.uint16()
        header['u6'] = stream.uint16()
        header['first_empty_slot_idx'] = stream.uint16()
        header['u7'] = stream.uint16()
        header['u8'] = stream.uint16()
        header['u9'] = stream.uint16()
        stream.read_bytes(56)

        return header

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        stream.seek(header['records_offset'])
        return [ContextEntry.parse(stream, header, i) for i in range(header['n_scripts'])]


class ContextEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['script_number'] = (stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8())
        data['mmap_idx'] = stream.uint32()
        data['u2'] = stream.uint16()
        data['u3'] = stream.uint16()

        return data
