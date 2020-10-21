from tonguetwister.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.chunks.chunk import RecordsChunk, Chunk
from tonguetwister.chunks.lingo_script import LingoScript
from tonguetwister.chunks.thumbnail import Thumbnail
from tonguetwister.gui.components.bitmap_cast_member import BitmapCastMemberView
from tonguetwister.gui.components.chunk import DefaultRecordsChunkView, DefaultChunkView
from tonguetwister.gui.components.script import ScriptPanel
from tonguetwister.gui.components.thumbnail import ThumbnailView

CHUNK_VIEW_MAP = {
    LingoScript.__name__: ScriptPanel,
    BitmapCastMember.__name__: BitmapCastMemberView,
    Thumbnail.__name__: ThumbnailView,
    RecordsChunk.__name__: DefaultRecordsChunkView,
    Chunk.__name__: DefaultChunkView
}
