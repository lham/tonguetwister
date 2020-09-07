from collections import OrderedDict

from tonguetwister.chunks.cast_association_map import CastAssociationMap
from tonguetwister.chunks.cast_key_map import CastKeyMap
from tonguetwister.chunks.cast_library_info import CastLibraryInfo
from tonguetwister.chunks.cast_member import CastMember
from tonguetwister.chunks.drcf import DRCF
from tonguetwister.chunks.font_map import FontMap
from tonguetwister.chunks.initial_map import InitialMap
from tonguetwister.chunks.lingo_context import LingoContext
from tonguetwister.chunks.lingo_namelist import LingoNamelist
from tonguetwister.chunks.lingo_script import LingoScript
from tonguetwister.chunks.memory_map import MemoryMap
from tonguetwister.chunks.styled_text import StyledText
from tonguetwister.lib.byte_block_io import ByteBlockIO

FOUR_CC_FUNCTION_MAP = {
    'CASt': '_parse_cast',
    'STXT': '_parse_stxt',
    'Cinf': '_parse_cinf',
    'Fmap': '_parse_fmap',
    'free': '_parse_undefined',
    'Lctx': '_parse_lctx',
    'Lnam': '_parse_lnam',
    'Lscr': '_parse_lscr',
    'CAS*': '_parse_cas_star',
    'imap': '_parse_imap',
    'DRCF': '_parse_drcf',
    'ccl ': '_parse_undefined',
    'RIFX': '_parse_rifx',
    'mmap': '_parse_mmap',
    'KEY*': '_parse_key_star',
    'RTE0': '_parse_undefined',
    'RTE1': '_parse_undefined',
    'RTE2': '_parse_undefined',
    'FXmp': '_parse_undefined',
    'MCsL': '_parse_undefined',
    'Sord': '_parse_undefined'
}


class RifxParser:
    def __init__(self, filename=None, silent=False):
        # Logging variables
        self.stack_depth = 0
        self.silent = silent

        # Parsing state variables
        self.current_four_cc = None
        self.current_address = None
        self.version = None
        self.stream = None

        # Parse results
        self.styled_texts = OrderedDict()
        self.cast_members = OrderedDict()
        self.font_map = None
        self.namelist = None
        self.cast_library_info = None
        self.lingo_scripts = OrderedDict()
        self._imap = None
        self.cast_assoc_map = None
        self.cast_key_map = None
        self.memory_map = None
        self.lingo_context = None
        self.cast_lib = []
        self._drcf = None

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
            self.current_address = address + 12  # Add 12 bytes for the four_cc code

            chunk_parser_function = getattr(self, FOUR_CC_FUNCTION_MAP[four_cc], self._undefined_function)
            chunk_parser_function(chunk_stream)

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
        RifxParser._strip_padding_from_uneven_chunk(stream, chunk_length)

        return four_cc, address, chunk

    @staticmethod
    def _strip_padding_from_uneven_chunk(stream, chunk_length):
        if chunk_length % 2 != 0:
            padding = stream.uint8()
            if padding != 0:
                raise RuntimeError('Padding is non-zero')

    def _undefined_function(self, stream):
        self._print_chunk_info('FOUR_CC PARSER FUNCTION NOT IMPLEMENTED')
        stream.read_bytes()

    def _print_chunk_info(self, message=''):
        if self.silent:
            return

        print((
            f'{self._indent_string()}'
            f'[{self.current_address:2d} / {self.current_address:#6x}] :: '
            f"{self.current_four_cc}{f' --> {message}' if message else ''}"
        ))

    def _indent_string(self, offset=0):
        return '    ' * (self.stack_depth + offset)

    def _parse_stxt(self, stream):
        self.styled_texts[self.current_address] = StyledText.parse(stream)
        self._print_chunk_info()
        # print repr(self.styled_texts[self.current_address])

    def _parse_cast(self, stream):
        self.cast_members[self.current_address] = CastMember.parse(stream)
        self._print_chunk_info()
        # print repr(self.cast_members[self.current_address])

    def _parse_fmap(self, stream):
        self.font_map = FontMap.parse(stream)
        self.font_map.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.font_map)

    def _parse_lnam(self, stream):
        self.namelist = LingoNamelist.parse(stream)
        self.namelist.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.namelist)

    def _parse_cinf(self, stream):
        self.cast_library_info = CastLibraryInfo.parse(stream)
        self.cast_library_info.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.cast_library_info)

    def _parse_lscr(self, stream):
        self.lingo_scripts[self.current_address] = LingoScript.parse(stream)
        self._print_chunk_info()
        # print repr(self.lingo_scripts[self.current_address])

    def _parse_imap(self, stream):
        self._imap = InitialMap.parse(stream)
        self._imap.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self._imap)

    def _parse_drcf(self, stream):
        self._drcf = DRCF.parse(stream)
        self._drcf.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self._imap)

    def _parse_cas_star(self, stream):
        self.cast_assoc_map = CastAssociationMap.parse(stream)
        self.cast_assoc_map.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.cast_assoc_map)

    def _parse_key_star(self, stream):
        self.cast_key_map = CastKeyMap.parse(stream)
        self.cast_key_map.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.cast_key_map)

    def _parse_mmap(self, stream):
        self.memory_map = MemoryMap.parse(stream)
        self.memory_map.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.memory_map)

    def _parse_lctx(self, stream):
        self.lingo_context = LingoContext.parse(stream)
        self.lingo_context.current_address = self.current_address
        self._print_chunk_info()
        # print repr(self.lingo_context)

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
