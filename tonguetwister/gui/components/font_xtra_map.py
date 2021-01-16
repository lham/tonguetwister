from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput

from tonguetwister.disassembler.chunks.font_xtra_map import FontXtraMap
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunkviews.default import RawChunkView
from tonguetwister.gui.widgets.generic.props import MonoFont
from tonguetwister.gui.utils import scroll_to_top


class FontXtraMapView(BoxLayout):
    current_function_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 0

        self.add_widget(self._build_tabbed_panel())

    def _build_tabbed_panel(self):
        self.text_area_reconstructed = TextInput(font_name=MonoFont.font_name)
        self.text_area_chunk = RawChunkView()

        tab1 = TabbedPanelItem(text='Reconstructed')
        tab1.add_widget(self.text_area_reconstructed)
        tab2 = TabbedPanelItem(text='Raw chunk info')
        tab2.add_widget(self.text_area_chunk)

        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=150, tab_height=30)
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)

        return tabbed_panel

    def load(self, file_disassembler: FileDisassembler, chunk: FontXtraMap):
        self.text_area_reconstructed.text = chunk.font_map
        self.text_area_chunk.load(file_disassembler, chunk)
        scroll_to_top(self.text_area_reconstructed)
