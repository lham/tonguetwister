from tonguetwister.disassembler.chunk import EntryMapChunk, InternalChunkEntry
from tonguetwister.lib.byte_block_io import ByteBlockIO


class CastAssociationMap(EntryMapChunk):
    sections = ['entries']

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO):
        data = []
        while stream.tell() < stream.size():
            data.append(MapEntry.parse(stream))

        return data


class MapEntry(InternalChunkEntry):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['mmap_idx'] = stream.uint32()

        return data
