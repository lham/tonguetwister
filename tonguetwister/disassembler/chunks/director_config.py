from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class DirectorConfig(Chunk):
    """
    The Config, as you might imagine, has some basic properties about the movie itself.
    This includes the version number, stage size, background colour and etc. In older
    Director versions where only one Cast was allowed, Cast Properties were also stored
    here, but now they are stored somewhere else. Also, it’s worth mentioning that Config
    is not actually a guessed name, as it is one of the clipboard types registered by
    Director, so we know this is its official name.
    -- https://medium.com/@nosamu/a-tour-of-the-adobe-director-file-format-e375d1e063c0

    """
    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
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
