from tonguetwister.chunks.cast_association_map import CastAssociationMap
from tonguetwister.chunks.cast_key_map import CastKeyMap
from tonguetwister.chunks.cast_library_info import CastLibraryInfo
from tonguetwister.chunks.cast_member import CastMember
from tonguetwister.chunks.chunk import UndefinedChunk
from tonguetwister.chunks.drcf import DRCF
from tonguetwister.chunks.font_map import FontMap
from tonguetwister.chunks.initial_map import InitialMap
from tonguetwister.chunks.lingo_context import LingoContext
from tonguetwister.chunks.lingo_namelist import LingoNamelist
from tonguetwister.chunks.lingo_script import LingoScript
from tonguetwister.chunks.memory_map import MemoryMap
from tonguetwister.chunks.styled_text import StyledText
from tonguetwister.lib.byte_block_io import ByteBlockIO


CHUNK_MAP = {
    'CASt': CastMember,
    'STXT': StyledText,
    'Cinf': CastLibraryInfo,
    'Fmap': FontMap,
    'free': UndefinedChunk,
    'Lctx': LingoContext,
    'Lnam': LingoNamelist,
    'Lscr': LingoScript,
    'CAS*': CastAssociationMap,
    'imap': InitialMap,
    'DRCF': DRCF,
    'ccl ': UndefinedChunk,
    'RIFX': UndefinedChunk,
    'mmap': MemoryMap,
    'KEY*': CastKeyMap,
    'RTE0': UndefinedChunk,
    'RTE1': UndefinedChunk,
    'RTE2': UndefinedChunk,
    'FXmp': UndefinedChunk,
    'MCsL': UndefinedChunk,
    'Sord': UndefinedChunk
}


class FileDisassembler:
    def __init__(self, filename=None, silent=False):
        # Logging variables
        self.silent = silent

        # Parsing state variables
        self.current_four_cc = None
        self.current_address = None
        self.stream = None

        # Parse results
        self.version = None
        self.chunks = []

        # Maybe load file
        if filename is not None:
            self.load_file(filename)

    def load_file(self, filename):
        with open(filename, 'rb') as f:
            stream = ByteBlockIO(f.read())
            four_cc, addr, chunk_stream = self._parse_command(stream)

            if four_cc == 'RIFX':
                self.version = chunk_stream.uint32()
                self.stream = ByteBlockIO(chunk_stream.read_bytes())
            else:
                raise RuntimeError(f'Input file {filename} does not contain a RIFX file header')

    def unpack(self):
        while not self.stream.is_depleted():
            four_cc, address, chunk_stream = self._parse_command(self.stream)
            self.current_four_cc = four_cc
            self.current_address = address

            self._print_chunk_info()
            self.chunks.append((self.current_address, CHUNK_MAP[four_cc].parse(chunk_stream, four_cc)))

            if not chunk_stream.is_depleted():
                print(chunk_stream.get_processed_bytes_string())
                print(chunk_stream.get_unprocessed_bytes_array())
                raise RuntimeError(f'[{four_cc}]: Unprocessed data remains')

    @staticmethod
    def _parse_command(stream):
        address = stream.tell()
        four_cc = stream.string(4)

        chunk_length = stream.uint32()
        chunk = ByteBlockIO(stream.read_bytes(chunk_length))
        FileDisassembler._strip_padding_from_uneven_chunk(stream, chunk_length)
        bytes_read = 12  # 4 for the four_cc, 4 for the chunk_length, and then 4 unknown/padding?

        return four_cc, address + bytes_read, chunk

    @staticmethod
    def _strip_padding_from_uneven_chunk(stream, chunk_length):
        if chunk_length % 2 != 0:
            padding = stream.uint8()
            if padding != 0:
                raise RuntimeError('Padding is non-zero')

    def _print_chunk_info(self, message=''):
        if self.silent:
            return

        print((
            f'[{self.current_address:2d} / {self.current_address:#6x}] :: '
            f"{self.current_four_cc}{f' --> {message}' if message else ''}"
        ))

    def _create_cast_lib(self):
        self.cast_lib = []

        """
        Iterate the CAS*:
          Add CASt to cast library AS entry:
            i = mmap-index of CASt in mmap
            Lookup mmap[i], add CASt data to entry

            k = mmap-index of key*(cast_mmap_idx=i)
            Lookup mmap[k] and add media type data to entry
        """

    @property
    def lingo_scripts(self):
        return [chunk for _, chunk in self.chunks if isinstance(chunk, LingoScript)]

    @property
    def namelist(self):
        namelists = [chunk for _, chunk in self.chunks if isinstance(chunk, LingoNamelist)]
        if len(namelists) > 1:
            print('Warning: More than one namelist')

        return namelists[0]
