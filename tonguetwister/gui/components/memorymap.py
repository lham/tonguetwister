from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from tonguetwister.disassembler.chunks.memory_map import MemoryMap
from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunkview import ChunkView
from tonguetwister.gui.components.chunk import DefaultRecordsChunkView
from tonguetwister.gui.widgets.defaultwidgets import VerticalStackLayout, FixedWidthLabel


class MemoryMapView(ChunkView):
    def __init__(self, **kwargs):
        self.hovered = None
        self.wrapper = None

        super().__init__(**kwargs)

    def tabs(self):
        return [
            ('Reconstructed', self.build_reconstructed_view),
        ]

    def build_raw_view(self):
        return DefaultRecordsChunkView(font_name=self.font_name)

    def build_reconstructed_view(self):
        self.wrapper = VerticalStackLayout()

        return self.wrapper

    def load(self, disassembler: FileDisassembler, chunk: MemoryMap):
        super().load(disassembler, chunk)
        self._load_reconstructed_view(chunk)

    def _load_reconstructed_view(self, chunk: MemoryMap):
        self.wrapper.clear_widgets()

        for index, entry in enumerate(chunk.entries):
            widget = Entry(index, entry, self.font_name)
            widget.bind(hovered=self._on_hovered)
            widget.bind(on_touch_down=self._on_click)

            self.wrapper.add_widget(widget)

    def _on_hovered(self, entry_widget, hovered):
        if hovered:
            if self.hovered is not None:
                self.hovered.set_highlighted(False)
            self.hovered = entry_widget
            self.hovered.set_highlighted(True)

        elif self.hovered == entry_widget:
            self.hovered.set_highlighted(False)
            self.hovered = None

    def _on_click(self, entry_widget, touch):
        if entry_widget.collide_point(*touch.pos) and entry_widget.active:
            self.select_resource_id = entry_widget.resource_id


class Entry(BoxLayout):
    COLOR_ACTIVE = (1, 1, 1, 1)
    COLOR_INACTIVE = (1, 1, 1, 0.5)
    COLOR_HIGHLIGHT = (1, 1, 0.2, 1)

    hovered = BooleanProperty(False)

    def __init__(self, resource_id, entry, font_name, **kwargs):
        super().__init__(**kwargs)
        self.font_name = font_name
        self.resource_id = resource_id
        self.entry = entry
        self.chunk_type = ChunkType(entry.four_cc)
        self.active = (self.chunk_type != ChunkType.Free and self.chunk_type != ChunkType.Junk)
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        self.orientation = 'horizontal'
        self.spacing = 10

        Window.bind(mouse_pos=self.on_mouse_pos)

        self._build_entry()

    def _build_entry(self):
        text = f'{self.resource_id} ->'
        label = FixedWidthLabel(text, 60, 'right', font_name=self.font_name, color=self.color)
        self.add_widget(label)

        text = f'0x{self.entry.chunk_address:08x}:'
        label = FixedWidthLabel(text, 100, 'left', font_name=self.font_name, color=self.color)
        self.add_widget(label)

        text = f'[{self.chunk_type}] = {self.chunk_type.name}'
        label = FixedWidthLabel(text, 220, 'left', font_name=self.font_name, color=self.color)
        self.add_widget(label)

        text = f'(Size: {self.entry.chunk_length} bytes)'
        label = FixedWidthLabel(text, 200, 'left', font_name=self.font_name, color=self.color)
        self.add_widget(label)

    def on_mouse_pos(self, _, mouse_pos):
        if not self.get_root_window():
            return  # Not displayed

        if self.collide_point(*mouse_pos):
            self.hovered = True
        elif self.hovered:
            self.hovered = False

    def set_highlighted(self, highlighted):
        for widget in self.children:
            if highlighted and self.active:
                widget.color = self.COLOR_HIGHLIGHT
            else:
                widget.color = self.color
