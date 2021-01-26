from tonguetwister.disassembler.chunks.cast_assoc_table import CastAssocTable
from tonguetwister.disassembler.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.disassembler.chunks.font_xtra_map import FontXtraMap
from tonguetwister.disassembler.chunks.lingo_script import LingoScript
from tonguetwister.disassembler.chunks.memory_map import MemoryMap
from tonguetwister.disassembler.chunks.movie_cast_libraries import MovieCastLibraries
from tonguetwister.disassembler.chunks.resource_assoc_table import ResourceAssocTable
from tonguetwister.disassembler.chunks.sort_order import SortOrder
from tonguetwister.disassembler.chunks.thumbnail import Thumbnail
from tonguetwister.disassembler.chunks.video_works_score import VideoWorksScore
from tonguetwister.gui.chunkview import ChunkView
from tonguetwister.gui.chunkviews.bitmapcastmember import BitmapCastMemberView
from tonguetwister.gui.chunkviews.cast_assoc_table import CastAssocTableView
from tonguetwister.gui.chunkviews.fontxtramap import FontXtraMapView
from tonguetwister.gui.chunkviews.memorymap import MemoryMapView
from tonguetwister.gui.chunkviews.moviecastlibraries import MovieCastLibrariesView
from tonguetwister.gui.chunkviews.resource_assoc_table import ResourceAssocTableView
from tonguetwister.gui.chunkviews.score import ScoreView
from tonguetwister.gui.chunkviews.sort_order import SortOrderView
from tonguetwister.gui.components.script import ScriptPanel
from tonguetwister.gui.chunkviews.thumbnail import ThumbnailView

CHUNK_VIEW_MAP = {
    MemoryMap: MemoryMapView,
    ResourceAssocTable: ResourceAssocTableView,
    MovieCastLibraries: MovieCastLibrariesView,
    CastAssocTable: CastAssocTableView,
    SortOrder: SortOrderView,
    VideoWorksScore: ScoreView,
    LingoScript: ScriptPanel,
    BitmapCastMember: BitmapCastMemberView,
    Thumbnail: ThumbnailView,
    FontXtraMap: FontXtraMapView,
    ChunkParser: ChunkView
}
