from typing import Union

from tonguetwister.disassembler.chunks.bitmap_data import BitmapData
from tonguetwister.disassembler.chunks.cast_association_map import CastAssociationMap
from tonguetwister.disassembler.chunks.resource_key_table import ResourceKeyTable
from tonguetwister.disassembler.chunks.cast_library_info import CastLibraryInfo
from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.disassembler.chunk import UnknownChunkParser, ChunkParser
from tonguetwister.disassembler.chunks.director_config import DirectorConfig
from tonguetwister.disassembler.chunks.editable_media import EditableMedia
from tonguetwister.disassembler.chunks.font_map import FontMap
from tonguetwister.disassembler.chunks.font_xtra_map import FontXtraMap
from tonguetwister.disassembler.chunks.initial_map import InitialMap
from tonguetwister.disassembler.chunks.lingo_context import LingoContext
from tonguetwister.disassembler.chunks.lingo_namelist import LingoNamelist
from tonguetwister.disassembler.chunks.lingo_script import LingoScript
from tonguetwister.disassembler.chunks.memory_map import MemoryMap
from tonguetwister.disassembler.chunks.movie_cast_libraries import MovieCastLibraries
from tonguetwister.disassembler.chunks.sort_order import SortOrder
from tonguetwister.disassembler.chunks.styled_text import StyledText
from tonguetwister.disassembler.chunks.thumbnail import Thumbnail
from tonguetwister.disassembler.chunks.video_works_file_info import VideoWorksFileInfo
from tonguetwister.disassembler.chunks.video_works_score import VideoWorksScore
from tonguetwister.lib.byte_block_io import ByteBlockIO


CHUNK_MAP = {
    'RIFX': UnknownChunkParser,
    'imap': InitialMap,
    'mmap': MemoryMap,
    'DRCF': DirectorConfig,
    'Sord': SortOrder,
    'MCsL': MovieCastLibraries,
    'FXmp': FontXtraMap,
    'VWFI': VideoWorksFileInfo,
    'VWSC': VideoWorksScore,
    'CASt': CastMember,
    'STXT': StyledText,
    'Cinf': CastLibraryInfo,
    'Fmap': FontMap,
    'free': UnknownChunkParser,
    'Lctx': LingoContext,
    'Lnam': LingoNamelist,
    'Lscr': LingoScript,
    'CAS*': CastAssociationMap,
    'ccl ': UnknownChunkParser,
    'KEY*': ResourceKeyTable,
    'RTE0': UnknownChunkParser,
    'RTE1': UnknownChunkParser,
    'RTE2': UnknownChunkParser,
    'BITD': BitmapData,
    'XTRl': UnknownChunkParser,
    'ediM': EditableMedia,
    'THUM': Thumbnail,
    'CLUT': UnknownChunkParser,
    'SCRF': UnknownChunkParser
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
                self.stream = chunk_stream
            else:
                raise RuntimeError(f'Input file {filename} does not contain a RIFX file header')

    def unpack(self):
        while not self.stream.is_depleted():
            four_cc, address, chunk_stream = self._parse_command(self.stream)
            self.current_four_cc = four_cc
            self.current_address = address

            self._print_chunk_info()
            if four_cc in CHUNK_MAP:
                self.chunks.append((self.current_address, CHUNK_MAP[four_cc].parse(chunk_stream, address, four_cc)))
            else:
                print('WARNING: The four_cc', four_cc, 'is not in the CHUNK_MAP')
                chunk_stream.read_bytes()

            if not chunk_stream.is_depleted():
                print(chunk_stream.get_processed_bytes_string())
                print(chunk_stream.get_unprocessed_bytes_array())
                raise RuntimeError(f'[{four_cc}]: Unprocessed data remains')

    @staticmethod
    def _parse_command(stream):
        address = stream.tell()
        four_cc = stream.string_raw(4)

        chunk_length = stream.uint32()
        chunk_stream = ByteBlockIO(stream.read_bytes(chunk_length))
        FileDisassembler._strip_padding_from_uneven_chunk(stream, chunk_length, four_cc, address)
        bytes_read = 8  # 4 for the four_cc and 4 for the chunk_length

        return four_cc, address + bytes_read, chunk_stream

    @staticmethod
    def _strip_padding_from_uneven_chunk(stream, chunk_length, four_cc, address):
        if chunk_length % 2 != 0:
            padding = stream.uint8()
            #if padding != 0:
            #    raise RuntimeError(f'Padding is non-zero for {four_cc} at {address}')

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
    def lingo_scripts(self) -> list:
        return [chunk for _, chunk in self.chunks if isinstance(chunk, LingoScript)]

    @property
    def namelist(self) -> Union[LingoNamelist, None]:
        namelists = [chunk for _, chunk in self.chunks if isinstance(chunk, LingoNamelist)]
        if len(namelists) == 0:
            return None
        if len(namelists) > 1:
            print('Warning: More than one namelist')
        return namelists[0]

    @property
    def cast_key_map(self) -> Union[ResourceKeyTable, None]:
        cast_key_maps = [chunk for _, chunk in self.chunks if isinstance(chunk, ResourceKeyTable)]
        if len(cast_key_maps) == 0:
            return None
        if len(cast_key_maps) > 1:
            print('Warning: More than one namelist')
        return cast_key_maps[0]

    @property
    def mmap(self) -> Union[MemoryMap, None]:
        memory_maps = [chunk for _, chunk in self.chunks if isinstance(chunk, MemoryMap)]
        if len(memory_maps) == 0:
            return None
        if len(memory_maps) > 1:
            print('Warning: More than one namelist')
        return memory_maps[0]

    def find_chunk_by_mmap_id(self, mmap_id) -> Union[ChunkParser, None]:
        address = self.mmap[mmap_id].address
        for (chunk_address, chunk) in self.chunks:
            if chunk_address == address:
                return chunk

        return None
