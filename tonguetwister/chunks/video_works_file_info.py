from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.property_reader import PropertyReader, property_reader


class FileInfoHeaderPropertyReader(PropertyReader):
    @property_reader(0)
    def created_by(self, stream):
        return stream.string_auto()

    @property_reader(1)
    def updated_by(self, stream):
        return stream.string_auto()

    @property_reader(2)
    def path(self, stream):
        return stream.string_auto()


class VideoWorksFileInfo(Chunk):
    OPTION_FLAGS = {
        0x01: 'Pause When Window Inactive',  # Modify > Movie > Playback...
        0x40: 'Remap Palettes When Needed'  # Modify > Movie > Properties...
    }

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint32()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['flags'] = stream.uint32()
        header['u4'] = stream.uint32()
        header['u5'] = stream.uint32()
        header['u6'] = stream.uint32()
        header['u7'] = stream.uint16()

        header['n_offsets'] = stream.uint32()
        header['u8'] = stream.uint32()

        header.update(stream.auto_property_list(
            FileInfoHeaderPropertyReader(),
            header['header_length'] + 6,
            header['n_offsets']
        ))

        return header
