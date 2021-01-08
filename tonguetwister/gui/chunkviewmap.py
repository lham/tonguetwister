from tonguetwister.disassembler.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.disassembler.chunks.font_xtra_map import FontXtraMap
from tonguetwister.disassembler.chunks.lingo_script import LingoScript
from tonguetwister.disassembler.chunks.memory_map import MemoryMap
from tonguetwister.disassembler.chunks.resource_key_table import ResourceKeyTable
from tonguetwister.disassembler.chunks.thumbnail import Thumbnail
from tonguetwister.disassembler.chunks.video_works_score import VideoWorksScore
from tonguetwister.gui.chunkview import ChunkView
from tonguetwister.gui.components.bitmap_cast_member import BitmapCastMemberView
from tonguetwister.gui.components.font_xtra_map import FontXtraMapView
from tonguetwister.gui.components.memorymap import MemoryMapView
from tonguetwister.gui.components.resourcekeytable import ResourceKeyTableView
from tonguetwister.gui.components.score import ScoreView
from tonguetwister.gui.components.script import ScriptPanel
from tonguetwister.gui.components.thumbnail import ThumbnailView

CHUNK_VIEW_MAP = {
    MemoryMap: MemoryMapView,
    ResourceKeyTable: ResourceKeyTableView,
    VideoWorksScore: ScoreView,
    LingoScript: ScriptPanel,
    BitmapCastMember: BitmapCastMemberView,
    Thumbnail: ThumbnailView,
    FontXtraMap: FontXtraMapView,
    ChunkParser: ChunkView
}
