from collections import OrderedDict

from tonguetwister.disassembler.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class CastAssociationMap(RecordsChunk):
    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        records = []
        while stream.tell() < stream.size():
            records.append(MapEntry.parse(stream))

        return records


class MapEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['mmap_idx'] = stream.uint32()

        return data
