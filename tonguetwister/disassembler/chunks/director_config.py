from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class DirectorConfig(Chunk):

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        """
        We should be able to find
        - version number
        - stage size
        - background color

        In older versions cast properties were stored here.
        -- https://medium.com/@nosamu/a-tour-of-the-adobe-director-file-format-e375d1e063c0
        """
        header = OrderedDict()
        header['chunk_length'] = stream.uint16()  # Inclusive self
        header['?version'] = stream.uint16()

        header['stage_top'] = stream.int16()
        header['stage_left'] = stream.int16()
        header['stage_bottom'] = stream.int16()
        header['stage_right'] = stream.int16()

        header['u1'] = stream.read_bytes(66)
        header['u1_b4'] = grouper(header['u1'], 4)
        header['u1_b2'] = grouper(header['u1'], 2)

        header['palette'] = stream.int16()
        header['u2'] = stream.uint32()

        return header

    @property
    def stage_rect(self):
        return {
            'top': self.header['stage_top'],
            'right': self.header['stage_right'],
            'bottom': self.header['stage_bottom'],
            'left': self.header['stage_left']
        }
