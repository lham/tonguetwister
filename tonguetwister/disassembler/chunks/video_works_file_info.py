from tonguetwister.disassembler.chunk import ChunkParser
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


class VideoWorksFileInfo(ChunkParser):
    OPTION_FLAGS = {
        0x01: 'Pause When Window Inactive',  # Modify > Movie > Playback...
        0x40: 'Remap Palettes When Needed'  # Modify > Movie > Properties...
    }

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['header_length'] = stream.uint32()
        data['u1'] = stream.uint32()
        data['u2'] = stream.uint32()
        data['flags'] = stream.uint32()
        data['u4'] = stream.uint32()
        data['u5'] = stream.uint32()
        data['u6'] = stream.uint32()
        data['u7'] = stream.uint16()

        data['n_offsets'] = stream.uint32()
        data['u8'] = stream.uint32()

        data.update(stream.auto_property_list(
            FileInfoHeaderPropertyReader,
            data['header_length'] + 6,
            data['n_offsets']
        ))

        return data
