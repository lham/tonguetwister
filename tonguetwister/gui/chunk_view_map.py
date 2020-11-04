from tonguetwister.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.chunks.chunk import RecordsChunk, Chunk
from tonguetwister.chunks.font_xtra_map import FontXtraMap
from tonguetwister.chunks.lingo_script import LingoScript
from tonguetwister.chunks.thumbnail import Thumbnail
from tonguetwister.chunks.video_works_score import VideoWorksScore
from tonguetwister.gui.components.bitmap_cast_member import BitmapCastMemberView
from tonguetwister.gui.components.chunk import DefaultRecordsChunkView, DefaultChunkView
from tonguetwister.gui.components.font_xtra_map import FontXtraMapView
from tonguetwister.gui.components.score import ScoreView
from tonguetwister.gui.components.script import ScriptPanel
from tonguetwister.gui.components.thumbnail import ThumbnailView

CHUNK_VIEW_MAP = {
    VideoWorksScore.__name__: ScoreView,
    LingoScript.__name__: ScriptPanel,
    BitmapCastMember.__name__: BitmapCastMemberView,
    Thumbnail.__name__: ThumbnailView,
    FontXtraMap.__name__: FontXtraMapView,
    RecordsChunk.__name__: DefaultRecordsChunkView,
    Chunk.__name__: DefaultChunkView
}
