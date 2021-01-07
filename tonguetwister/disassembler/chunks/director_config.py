from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class DirectorConfig(ChunkParser):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        """
        We should be able to find
        - version number
        - stage size
        - background color

        In older versions cast properties were stored here.
        -- https://medium.com/@nosamu/a-tour-of-the-adobe-director-file-format-e375d1e063c0
        """
        data = {}
        data['chunk_length'] = stream.uint16()  # Inclusive self
        data['?version'] = stream.uint16()

        data['stage_top'] = stream.int16()
        data['stage_left'] = stream.int16()
        data['stage_bottom'] = stream.int16()
        data['stage_right'] = stream.int16()

        data['u1'] = stream.read_bytes(66)
        data['u1_b4'] = grouper(data['u1'], 4)
        data['u1_b2'] = grouper(data['u1'], 2)

        data['palette'] = stream.int16()
        data['u2'] = stream.uint32()

        return data

    @property
    def stage_rect(self):
        return {
            'top': self._data['stage_top'],
            'right': self._data['stage_right'],
            'bottom': self._data['stage_bottom'],
            'left': self._data['stage_left']
        }
