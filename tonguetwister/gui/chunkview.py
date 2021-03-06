from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunkviews.default import RawChunkView


class ResourceLink:
    def __init__(self, resource_id, chunk_type=None):
        self.resource_id = resource_id
        self.chunk_type = chunk_type

    def is_linked_resource(self):
        return self.chunk_type is not None

    def get_linked_resource_id(self, disassembler: FileDisassembler):
        if not self.is_linked_resource():
            return self.resource_id

        resource = disassembler.get_linked_resource_by_id(
            self.resource_id,
            self.chunk_type,
            as_chunk=False
        )

        if resource is not None:
            return resource.resource_id
        else:
            return None


class ChunkView(BoxLayout):
    resource_link = ObjectProperty(None, allownone=True)

    def __init__(self, tab_width=170, tab_height=30, **kwargs):
        super().__init__(**kwargs)
        self.tab_width = tab_width
        self.tab_height = tab_height
        self.disassembler = None

        self.raw_view = None
        self.add_widget(self.build())

    def build(self):
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=self.tab_width, tab_height=self.tab_height)

        for title, build_view in self.tabs():
            tab = TabbedPanelItem(text=title)
            tab.add_widget(self.with_margin(build_view()))
            tabbed_panel.add_widget(tab)

        self.raw_view = RawChunkView()
        tab = TabbedPanelItem(text='Raw parse info')
        tab.add_widget(self.with_margin(self.raw_view))
        tabbed_panel.add_widget(tab)

        return tabbed_panel

    @staticmethod
    def with_margin(view):
        wrapper = BoxLayout(padding=(10, 10, 10, 10))
        wrapper.add_widget(view)

        return wrapper

    def tabs(self):
        return []

    def load(self, disassembler: FileDisassembler, chunk: ChunkParser):
        self.disassembler = disassembler
        self.raw_view.load(disassembler, chunk)
        self.raw_view.scroll_to_top()
