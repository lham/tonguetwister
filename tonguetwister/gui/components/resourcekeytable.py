from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.widgets.defaultwidgets import FixedWidthLabel
from tonguetwister.gui.widgets.arraymappingview import ArrayMappingView, ArrayMappingEntryView


class ResourceKeyTableEntryView(ArrayMappingEntryView):
    def __init__(self, index, entry, font_name, **kwargs):
        self.chunk_type = ChunkType(entry.child_four_cc)

        super().__init__(index, entry, font_name, **kwargs)

    def resource_id(self):
        return self.entry.child_resource_id

    def build_entry(self):
        text = f'({self.entry.parent_resource_id}, {self.chunk_type})'
        label = FixedWidthLabel(text, 130, 'right', font_name=self.font_name, color=self.color())
        self.add_widget(label)

        text = f'-> {self.entry.child_resource_id:4d}: {self.chunk_type.name}'
        label = FixedWidthLabel(text, 300, 'left', font_name=self.font_name, color=self.color())
        self.add_widget(label)


class ResourceKeyTableView(ArrayMappingView):
    entry_class = ResourceKeyTableEntryView
