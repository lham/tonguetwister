from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.widgets.defaultwidgets import FixedWidthLabel
from tonguetwister.gui.widgets.arraymappingview import ArrayMappingView, ArrayMappingEntryView


class MemoryMapEntryView(ArrayMappingEntryView):
    def __init__(self, index, entry, font_name, **kwargs):
        self._resource_id = index
        self.chunk_type = ChunkType(entry.four_cc)

        super().__init__(index, entry, font_name, **kwargs)

    def is_active(self):
        return self.chunk_type != ChunkType.Free and self.chunk_type != ChunkType.Junk

    def resource_id(self):
        return self._resource_id

    def build_entry(self):
        text = f'{self._resource_id} ->'
        label = FixedWidthLabel(text, 60, 'right', font_name=self.font_name, color=self.color())
        self.add_widget(label)

        text = f'0x{self.entry.chunk_address:08x}:'
        label = FixedWidthLabel(text, 100, 'left', font_name=self.font_name, color=self.color())
        self.add_widget(label)

        text = f'[{self.chunk_type}] = {self.chunk_type.name}'
        label = FixedWidthLabel(text, 220, 'left', font_name=self.font_name, color=self.color())
        self.add_widget(label)

        text = f'(Size: {self.entry.chunk_length} bytes)'
        label = FixedWidthLabel(text, 200, 'left', font_name=self.font_name, color=self.color())
        self.add_widget(label)


class MemoryMapView(ArrayMappingView):
    entry_class = MemoryMapEntryView
