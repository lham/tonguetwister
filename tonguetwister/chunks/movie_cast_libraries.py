from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
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
        record = OrderedDict()
        record['cast_member_id_first'] = stream.uint16()
        record['cast_member_id_last'] = stream.uint16()
        record['cast_resource_id'] = stream.uint32()

        return record


class MovieCastLibraries(Chunk):
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint32()
        header['?n_props'] = stream.uint32()
        header['?n_items_per_prop'] = stream.uint16()

        header['n_offsets'] = stream.int32()
        header['u2'] = stream.uint32()

        header.update(stream.auto_property_list(
            CastLibraryPropertyReader(),
            header['header_length'] + 6,
            header['n_offsets'],
            header['?n_props']
        ))

        return header
