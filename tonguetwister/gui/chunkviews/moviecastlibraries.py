from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.chunkview import ResourceLink
from tonguetwister.gui.generic.layouts import VerticalStackLayout
from tonguetwister.gui.widgets.entrylistview import EntryListView, EntryView


class MovieCastLibrariesEntryView(EntryView):
    rows = 2
    cols = 4
    col_widths = [200, 20, 300, 300]

    def label_kwargs(self):
        return [
            [
                {'text': self.entry.name},
                {'text': '->', 'halign': 'center'},
                {'text': self.entry.external_path} if self.entry.is_linked() else self.link(ChunkType.CastKeyTable),
                {'text': f'Cast member slots -- first: {self.entry.cast_member_id_first:2d}'}
            ],
            [
                {},
                {} if self.entry.is_linked() else {'text': '->', 'halign': 'center'},
                {} if self.entry.is_linked() else self.link(ChunkType.CastLibraryInfo),
                {'text': f'                     last:  {self.entry.cast_member_id_last:2d}'}
            ]
        ]

    def link(self, chunk_type):
        return {
            'text': f'[{self.entry.cast_resource_id:4d}]: {chunk_type.name}',
            'link_target': lambda: self.set_resource_link(chunk_type)
        }

    def set_resource_link(self, chunk_type):
        self.resource_link = ResourceLink(self.entry.cast_resource_id, chunk_type)


class MovieCastLibrariesView(EntryListView):
    entry_class = MovieCastLibrariesEntryView

    def build_reconstructed_view_layout(self):
        return VerticalStackLayout(spacing=(0, 20))
