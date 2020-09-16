import os

# TODO: Change to using kivy.config?
#os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ["KIVY_NO_ARGS"] = '1'

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from tonguetwister.chunks.chunk import RecordsChunk, Chunk
from tonguetwister.chunks.lingo_script import LingoScript
from tonguetwister.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.components.bitmap_cast_member import BitmapCastMemberView
from tonguetwister.gui.components.castmember import CastMemberView
from tonguetwister.gui.components.chunk import DefaultRecordsChunkView, DefaultChunkView
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

    def __init__(self, file_disassembler: FileDisassembler):
        super().__init__()

        self.file_disassembler = file_disassembler
        self._chunks = []
        self._set_chunks()

        # GUI Components
        self.menu = None
        self.view = None
        self.script_view = None
        self.cast_member_view = None
        self.bitmap_cast_member_view = None
        self.records_chunk_view = None
        self.chunk_view = None
        self.plain_view = None

        # Commands
        self._keyboard = None
        self._set_keyboard()

    def _set_chunks(self):
        type_counts = {}
        for (address, chunk) in self.file_disassembler.chunks:
            chunk_name = chunk.__class__.__name__
            chunk_count = type_counts.get(chunk_name, 0)
            type_counts[chunk_name] = chunk_count + 1

            self._chunks.append((chunk_count, f'{chunk_name} #{chunk_count} (addr: 0x{chunk.address:X})', chunk))

    def _set_keyboard(self):
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

        self.script_view = ScriptPanel(self.file_disassembler)
        self.cast_member_view = CastMemberView(self.file_disassembler, font_name=self.FONT_NAME)
        self.bitmap_cast_member_view = BitmapCastMemberView(self.file_disassembler, font_name=self.FONT_NAME)

        # Default viewers
        self.records_chunk_view = DefaultRecordsChunkView(self.file_disassembler, font_name=self.FONT_NAME)
        self.chunk_view = DefaultChunkView(self.file_disassembler, font_name=self.FONT_NAME)
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

    def _on_keyboard_down(self, _, keycode, __, ___):
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
        elif isinstance(chunk, BitmapCastMember):
            self.view.add_widget(self.bitmap_cast_member_view)
            self.bitmap_cast_member_view.load(chunk)
        elif isinstance(chunk, RecordsChunk):
            self.view.add_widget(self.records_chunk_view)
            self.records_chunk_view.load(chunk)
        elif isinstance(chunk, Chunk):
            self.view.add_widget(self.chunk_view)
            self.chunk_view.load(chunk)
        else:
            self.view.add_widget(self.plain_view)
            self.plain_view.text = repr(chunk)
            scroll_to_top(self.plain_view)
