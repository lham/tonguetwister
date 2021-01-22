from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class CastAssocEntry(InternalEntryParser):
    public_data_attrs = ['resource_id']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['resource_id'] = stream.uint32()

        return data


class CastAssocTable(EntryMapChunkParser):
    sections = ['entries']

    # noinspection PyMethodOverriding
    @classmethod
    def parse_entries(cls, stream: ByteBlockIO):
        data = []
        while stream.tell() < stream.size():
            data.append(CastAssocEntry.parse(stream))

        return data
