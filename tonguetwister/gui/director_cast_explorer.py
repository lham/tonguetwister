import os

# TODO: Change to using kivy.config?
from kivy.properties import ObjectProperty

from tonguetwister.gui.components.script import ScriptPanel

os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ["KIVY_NO_ARGS"] = '1'

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.label import Label

from tonguetwister.gui.widgets.listview import ListView, IndexedItem

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top',  0)
Window.size = (1600, 900)


class DirectorCastExplorer(App):
    current_chunk = ObjectProperty(IndexedItem())

    def __init__(self, parser_results):
        super().__init__()
        self.parser_results = parser_results
        self.scripts = list(self.parser_results.lingo_scripts.items())

        self.menu = None
        self.script_view = None

    def on_start(self):
        self.menu.select_item(0)

    def build(self):
        root = BoxLayout(orientation='horizontal', spacing=10)

        self.menu = self._build_menu()
        root.add_widget(self.menu)

        self.script_view = ScriptPanel(self.parser_results)
        root.add_widget(self.script_view)

        return root

    def _build_menu(self):
        menu = ListView(self.scripts, self._build_chunk_menu_item, width=200, size_hint_x=None)
        menu.bind(selected_element=self._update_chunk)

        return menu

    def _build_chunk_menu_item(self, index, script, parent):
        text = f'Script no {index} ({len(script[1].functions)} functions)'
        if self.current_chunk.index == index:
            text = f'[b]{text}[/b]'

        return Label(text=text, halign='left', valign='middle', text_size=(parent.width, None), markup=True)

    def _update_chunk(self, _, indexed_item):
        self.current_chunk = indexed_item

    def on_current_chunk(self, _, __):
        self.script_view.load(self.current_chunk)
