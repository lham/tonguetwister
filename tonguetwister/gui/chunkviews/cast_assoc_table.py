from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunkview import ResourceLink
from tonguetwister.gui.widgets.entrylistview import EntryListView, EntryView
from tonguetwister.gui.widgets.generic.labels import FixedSizeLabel, FixedSizeLinkLabel, InactiveFixedSizeLabel
from tonguetwister.gui.widgets.generic.layouts import SideScrollView, VerticalBoxLayout


class CastAssocTableEntryView(EntryView):
    rows = 1
    cols = 3
    col_widths = [50, 20, 50]

    def is_active(self):
        return self.entry.resource_id != 0

    @property
    def label_class(self):
        return FixedSizeLabel if self.is_active() else InactiveFixedSizeLabel

    @property
    def link_label_class(self):
        return FixedSizeLinkLabel if self.is_active() else InactiveFixedSizeLabel

    def label_kwargs(self):
        return [
            {'text': f'{self.index:4d}'},
            {'text': '->', 'halign': 'center'},
            {
                'text': f'[{self.entry.resource_id:4d}]',
                'link_target': self.set_resource_link
            }
        ]

    def set_resource_link(self):
        self.resource_link = ResourceLink(self.entry.resource_id)


class CastEntryView(CastAssocTableEntryView):
    col_widths = [250, 20, 300]

    def __init__(self, index, entry, slot_offset, disassembler):
        self.slot_offset = slot_offset
        self.disassembler = disassembler
        super().__init__(index, entry)

    @property
    def cast_member_name(self):
        if self.is_active():
            return f': {self.disassembler.get_resource_by_id(self.entry.resource_id).name}'

        return ''

    @property
    def chunk_type(self):
        if self.is_active():
            return f': {self.disassembler.get_resource_by_id(self.entry.resource_id).type_name}'

        return ''

    def label_kwargs(self):
        slot_id = self.index + self.slot_offset

        return [
            {'text': f'Slot {slot_id:4d}{self.cast_member_name}'},
            {'text': '->', 'halign': 'center'},
            {
                'text': f'[{self.entry.resource_id:4d}]{self.chunk_type}',
                'link_target': self.set_resource_link
            }
        ]


class CastAssocTableView(EntryListView):
    def __init__(self, *args, **kwargs):
        self.cast = None
        self.cast_title = None
        self.cast_members_layout = None
        super().__init__(*args, **kwargs)

    def tabs(self):
        return [
            ('Reconstructed Cast', self.build_cast_view),
            ('Reconstructed Table', self.build_reconstructed_view)
        ]

    def build_cast_view(self):
        self.cast_title = FixedSizeLabel('', 300, 20, font_size=20)
        self.cast_members_layout = self.build_reconstructed_view_layout()

        scroll_view = SideScrollView()
        scroll_view.add_widget(self.cast_members_layout)

        layout = VerticalBoxLayout(spacing=20)
        layout.add_widget(self.cast_title)
        layout.add_widget(scroll_view)

        return layout

    def load(self, disassembler: FileDisassembler, chunk):
        super().load(disassembler, chunk)

        self.cast = self.lookup_cast(chunk)
        self.cast_title.text = f'Cast: {self.cast.name}'
        self.load_entries_view(self.cast_members_layout, self.create_cast_entry_view, chunk)

    def create_entry_view(self, index, entry):
        return CastAssocTableEntryView(index, entry)

    def create_cast_entry_view(self, index, entry):
        return CastEntryView(index, entry, self.cast.cast_member_id_first, self.disassembler)

    def lookup_cast(self, chunk):
        parent_resource_id = self.disassembler.reverse_lookup_parent_resource_id(chunk)
        casts = self.disassembler.lookup_movie_resource(ChunkType.MovieCastLibraries)

        return casts.find_cast_by_resource_id(parent_resource_id)
