from tonguetwister.disassembler.chunks.bitmap_data import BitmapData
from tonguetwister.disassembler.chunks.cast_association_map import CastAssociationMap
from tonguetwister.disassembler.chunks.cast_key_map import CastKeyMap
from tonguetwister.disassembler.chunks.cast_library_info import CastLibraryInfo
from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.disassembler.chunk import UndefinedChunk
from tonguetwister.disassembler.chunks.rifx import Rifx
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

CHUNK_MAP = {
    'BITD': BitmapData,
    'CAS*': CastAssociationMap,
    'CASt': CastMember,
    'ccl ': UndefinedChunk,
    'Cinf': CastLibraryInfo,
    'CLUT': UndefinedChunk,
    'DRCF': DirectorConfig,
    'ediM': EditableMedia,
    'Fmap': FontMap,
    'FXmp': FontXtraMap,
    'imap': InitialMap,
    'KEY*': CastKeyMap,
    'Lctx': LingoContext,
    'Lnam': LingoNamelist,
    'Lscr': LingoScript,
    'MCsL': MovieCastLibraries,
    'mmap': MemoryMap,
    'RIFX': Rifx,
    'RTE0': UndefinedChunk,
    'RTE1': UndefinedChunk,
    'RTE2': UndefinedChunk,
    'SCRF': UndefinedChunk,
    'Sord': SortOrder,
    'STXT': StyledText,
    'THUM': Thumbnail,
    'VWFI': VideoWorksFileInfo,
    'VWSC': VideoWorksScore,
    'XTRl': UndefinedChunk,
}
