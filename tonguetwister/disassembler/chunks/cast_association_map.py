from tonguetwister.disassembler.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class CastAssociationMap(RecordsChunk):
    sections = ['records']

    @classmethod
    def parse_records(cls, stream: ByteBlockIO):
        data = []
        while stream.tell() < stream.size():
            data.append(MapEntry.parse(stream))

        return data


class MapEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = {}
        data['mmap_idx'] = stream.uint32()

        return data
