import os
import pprint

# TODO: Change to using kivy.config?
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ["KIVY_NO_ARGS"] = '1'

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from tonguetwister.chunks.cast_member import CastMember
from tonguetwister.chunks.lingo_script import LingoScript
from tonguetwister.gui.components.castmember import CastMemberView
from tonguetwister.gui.components.script import ScriptPanel
from tonguetwister.gui.utils import scroll_to_top
from tonguetwister.gui.widgets.listview import ListView, IndexedItem


Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top',  0)
Window.size = (1600, 900)


class DirectorCastExplorer(App):
    FONT_NAME = 'UbuntuMono-R.ttf'

    current_chunk = ObjectProperty(IndexedItem())
    previous_chunk = None

    def __init__(self, pr):
        super().__init__()
        self.parser_results = pr
        self.scripts = list(self.parser_results.lingo_scripts.items())

        # Add all items
        self._chunks = []

        self._chunks.append((0, f'[{pr.font_map.current_address:#6x}] Font Map #0', pr.font_map))
        self._chunks.append((0, f'[{pr.namelist.current_address:#6x}] Namelist #0', pr.namelist))
        self._chunks.append((0, f'[{pr.cast_library_info.current_address:#6x}] Cast Library Info #0', pr.cast_library_info))
        self._chunks.append((0, f'[{pr.cast_key_map.current_address:#6x}] Cast key map #0', pr.cast_key_map))
        self._chunks.append((0, f'[{pr.lingo_context.current_address:#6x}] Lingo Context #0', pr.lingo_context))
        self._chunks.append((0, f'[{pr.memory_map.current_address:#6x}] Memory Map #0', pr.memory_map))
        self._chunks.append((0, f'[{pr._imap.current_address:#6x}] _i Map #0', pr._imap))

        for i, (key, value) in enumerate(pr.styled_texts.items()):
            self._chunks.append((i, f'[{key:#6x}] Styled Text #{i}', value))

        for i, (key, value) in enumerate(pr.cast_members.items()):
            self._chunks.append((i, f'[{key:#6x}] Cast Member #{i}', value))

        for i, (key, value) in enumerate(pr.lingo_scripts.items()):
            self._chunks.append((i, f'[{key:#6x}] Lingo Script #{i} ({len(value.functions)} functions)', value))

        # GUI Components
        self.menu = None
        self.view = None
        self.script_view = None
        self.cast_member_view = None
        self.plain_view = None

        # Commands
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_start(self):
        self.menu.select_item(0)

    def build(self):
        root = BoxLayout(orientation='horizontal')

        menu = self._build_menu()
        root.add_widget(menu)

        self.view = BoxLayout()
        root.add_widget(self.view)

        self.script_view = ScriptPanel(self.parser_results)
        self.cast_member_view = CastMemberView(self.parser_results, font_name=self.FONT_NAME)
        self.plain_view = TextInput(font_name=self.FONT_NAME)

        self.view.add_widget(self.plain_view)

        return root

    def _build_menu(self):
        width = 300

        self.menu = ListView(self._chunks, self._build_chunk_menu_item, width=width, size_hint_x=None, size_hint_y=None)
        self.menu.bind(selected_element=self._update_chunk)
        self.menu.bind(minimum_height=self.menu.setter('height'))

        scroll_view = ScrollView(size_hint_x=None, width=width)
        scroll_view.add_widget(self.menu)

        return scroll_view

    def _build_chunk_menu_item(self, index, chunk, parent):
        text = chunk[1]
        if self.current_chunk.index == index:
            text = f'[b]{text}[/b]'

        return Label(text=text, halign='left', text_size=(parent.width, None), markup=True)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        current = self.menu.selected_element.index

        if keycode[1] == 'up':
            self.menu.select_item(max(0, current - 1))
        elif keycode[1] == 'down':
            self.menu.select_item(min(len(self._chunks) - 1, current + 1))

    def _update_chunk(self, _, indexed_item):
        self.previous_chunk = self.current_chunk
        self.current_chunk = indexed_item

    def on_current_chunk(self, _, chunk):
        if chunk == self.previous_chunk:
            return

        chunk = self.current_chunk.item[2]
        self.view.clear_widgets()

        if isinstance(chunk, LingoScript):
            self.view.add_widget(self.script_view)
            self.script_view.load(self.current_chunk.item[0], self.current_chunk.item[2])
        elif isinstance(chunk, CastMember):
            self.view.add_widget(self.cast_member_view)
            self.cast_member_view.load(chunk)
        else:
            self.view.add_widget(self.plain_view)
            self.plain_view.text = repr(chunk)
            scroll_to_top(self.plain_view)
