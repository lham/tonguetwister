from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.components.chunk import DefaultChunkView
from tonguetwister.gui.utils import scroll_to_top


class ChunkView(BoxLayout):
    select_resource_id = NumericProperty(None, allownone=True)

    def __init__(self, font_name, **kwargs):
        super().__init__(**kwargs)
        self.font_name = font_name
        self.raw_view = None
        self.add_widget(self.build())

    def build(self):
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=170, tab_height=30)

        for title, build_view in self.tabs():
            tab = TabbedPanelItem(text=title)
            tab.add_widget(build_view())
            tabbed_panel.add_widget(tab)

        self.raw_view = self.build_raw_view()
        tab = TabbedPanelItem(text='Raw parse info')
        tab.add_widget(self.raw_view)
        tabbed_panel.add_widget(tab)

        return tabbed_panel

    def tabs(self):
        return []

    def build_raw_view(self):
        return DefaultChunkView(font_name=self.font_name)

    def load(self, disassembler: FileDisassembler, chunk: ChunkParser):
        self.raw_view.load(disassembler, chunk)
        scroll_to_top(self.raw_view)
