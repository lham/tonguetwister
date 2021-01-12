from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class MapEntry(InternalEntryParser):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['mmap_idx'] = stream.uint32()

        return data


class CastAssociationMap(EntryMapChunkParser):
    sections = ['entries']

    # noinspection PyMethodOverriding
    @classmethod
    def parse_entries(cls, stream: ByteBlockIO):
        data = []
        while stream.tell() < stream.size():
            data.append(MapEntry.parse(stream))

        return data
