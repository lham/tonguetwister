from enum import Enum

from tonguetwister.disassembler.chunks.bitmap_data import BitmapData
from tonguetwister.disassembler.chunks.cast_assoc_table import CastAssocTable
from tonguetwister.disassembler.chunks.resource_assoc_table import ResourceAssocTable
from tonguetwister.disassembler.chunks.cast_library_info import CastLibraryInfo
from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.disassembler.chunkparser import UnknownChunkParser, ChunkParser
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


class ChunkType(Enum):
    # Internal resources structure
    RIFX = ('RIFX', Rifx)
    InitialMap = ('imap', InitialMap)
    MemoryMap = ('mmap', MemoryMap)
    ResourceAssocTable = ('KEY*', ResourceAssocTable)
    Junk = ('junk', UnknownChunkParser)
    Free = ('free', UnknownChunkParser)

    # Config
    VideoWorksFileInfo = ('VWFI', VideoWorksFileInfo)
    DirectorConfig = ('DRCF', DirectorConfig)
    FontMap = ('Fmap', FontMap)
    FontXtraMap = ('FXmp', FontXtraMap)

    # Cast
    MovieCastLibraries = ('MCsL', MovieCastLibraries)
    CastAssocTable = ('CAS*', CastAssocTable)
    CastLibraryInfo = ('Cinf', CastLibraryInfo)
    SortOrder = ('Sord', SortOrder)
    CastMember = ('CASt', CastMember)
    CastThumbnail = ('THUM', Thumbnail)

    # Score
    VideoWorksScore = ('VWSC', VideoWorksScore)

    # Lingo
    LingoContext = ('Lctx', LingoContext)
    LingoNamelist = ('Lnam', LingoNamelist)
    LingoScript = ('Lscr', LingoScript)

    # Data resources
    BitmapData = ('BITD', BitmapData)
    CLUT = ('CLUT', UnknownChunkParser)
    EditableMedia = ('ediM', EditableMedia)
    StyledText = ('STXT', StyledText)

    # Unknown
    CCL = ('ccl ', UnknownChunkParser)
    RTE0 = ('RTE0', UnknownChunkParser)
    RTE1 = ('RTE1', UnknownChunkParser)
    RTE2 = ('RTE2', UnknownChunkParser)
    SCRF = ('SCRF', UnknownChunkParser)
    XTRl = ('XTRl', UnknownChunkParser)

    def __new__(cls, four_cc: str, parser: ChunkParser, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = four_cc

        obj._four_cc = four_cc
        obj._parser = parser

        return obj

    def __str__(self):
        return self._four_cc

    @property
    def parser(self):
        return self._parser

    @property
    def four_cc(self):
        return self._four_cc
