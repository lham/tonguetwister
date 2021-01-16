from tonguetwister.disassembler.chunkparser import ChunkParser, EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO
from tonguetwister.lib.property_reader import PropertyReader, property_reader


class CastLibraryPropertyReader(PropertyReader):
    @property_reader(0)
    def name(self, stream):
        return stream.string_auto()

    @property_reader(1)
    def external_path(self, stream):
        return stream.string_auto()

    @property_reader(3)
    def _3(self, stream):
        record = {}
        record['cast_member_id_first'] = stream.uint16()
        record['cast_member_id_last'] = stream.uint16()
        record['cast_resource_id'] = stream.uint32()

        return record


class MovieCastLibraries(EntryMapChunkParser):
    """
    This Chunk was introduced in Director 5 to allow Movies to have multiple Casts.
    The Cast Properties, which used to be a part of the Config, were moved here.
    This is a list which has the names, filenames (if external), minimum and maximum
    member number (will touch again on this in a moment), number of members, and most
    importantly, ResourceIDs of the Casts. That’s right — Casts have ResourceIDs too!
    And again — they’re not exclusive, so it can be the same ResourceID as anything else.
    -- https://medium.com/@nosamu/a-tour-of-the-adobe-director-file-format-e375d1e063c0
    """

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        data = {}
        data['header_length'] = stream.uint32()
        data['?n_props'] = stream.uint32()
        data['?n_items_per_prop'] = stream.uint16()

        data['n_offsets'] = stream.int32()
        data['u2'] = stream.uint32()

        return data

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        data = stream.auto_property_list(
            CastLibraryPropertyReader,
            header['header_length'] + 6,
            header['n_offsets'],
            header['?n_props']
        )

        return [CastEntry.parse(stream, entry) for entry in data.values()]


class CastEntry(InternalEntryParser):
    public_data_attrs = ['name', 'cast_resource_id', 'cast_member_id_first', 'cast_member_id_last']

    @classmethod
    def parse_data(cls, _, entry):
        data = {}
        data.update(entry)

        return data

    def is_linked(self):
        return len(self._data['external_path']) > 0

    @property
    def external_path(self):
        if self.is_linked():
            return self._data['external_path']

        return None

