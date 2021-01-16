from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.chunkview import ResourceLink
from tonguetwister.gui.generic.labels import FixedSizeLinkLabel, FixedSizeLabel
from tonguetwister.gui.widgets.entrylistview import EntryListView, EntryView


class InactiveFixedSizeLabel(FixedSizeLabel):
    color = (1, 1, 1, 0.2)

    def __init__(self, *args, **kwargs):
        if 'link_target' in kwargs:
            kwargs.pop('link_target')

        super().__init__(*args, **kwargs)


class MemoryMapEntryView(EntryView):
    rows = 1
    cols = 6
    col_widths = [35, 20, 140, 20, 250, 200]

    def __init__(self, index, entry, **kwargs):
        self.chunk_type = ChunkType(entry.four_cc)
        super().__init__(index, entry, **kwargs)

    def is_active(self):
        return self.chunk_type != ChunkType.Free and self.chunk_type != ChunkType.Junk

    @property
    def label_class(self):
        return FixedSizeLabel if self.is_active() else InactiveFixedSizeLabel

    @property
    def link_label_class(self):
        return FixedSizeLinkLabel if self.is_active() else InactiveFixedSizeLabel

    def entry_kwarg_list(self):
        return [
            {'text': f'{self.index}', 'halign': 'right'},
            {'text': '--', 'halign': 'center'},
            {'text': f'0x{self.entry.chunk_address:08x} / {self.chunk_type}', 'halign': 'center'},
            {'text': '->', 'halign': 'center'},
            {
                'text': f'[{self.index:4d}]: {self.chunk_type.name}',
                'link_target': self.set_resource_link
            },
            {'text': f'(Size: {self.entry.chunk_length} bytes)'}
        ]

    def set_resource_link(self):
        self.resource_link = ResourceLink(self.index)


class MemoryMapView(EntryListView):
    entry_class = MemoryMapEntryView
