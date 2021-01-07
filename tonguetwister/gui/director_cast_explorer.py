from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from tonguetwister.disassembler.chunk import EntryMapChunkParser, ChunkParser
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunk_view_map import CHUNK_VIEW_MAP
from tonguetwister.gui.components.score import ScoreNotationCanvas
from tonguetwister.gui.utils import scroll_to_top
from tonguetwister.gui.widgets.file_dialogs import FileDialogPopup
from tonguetwister.gui.widgets.listview import ListView, IndexedItem


Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top',  0)
Window.size = (1600, 900)


class DirectorCastExplorer(App):
    FONT_NAME = 'UbuntuMono-R.ttf'

    current_chunk = ObjectProperty(IndexedItem())
    previous_chunk = None

    def __init__(self, base_dir=str(Path.home()), filename=None):
        super().__init__()
        self._set_title()

        # Director data
        self.initial_filename = filename
        self.file_disassembler = None
        self._chunks = []

        # Actions
        self.file_dialog = FileDialogPopup(title='Select a Director 6 movie', base_dir=base_dir)
        self.file_dialog.bind(file_opened=self._load_file)

        # GUI Components
        self.menu = None
        self.view_wrapper = None
        self.default_view = None
        self.views = None

        # Commands
        self._keyboard = None
        self._set_keyboard()

    def _set_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _recapture_keyboard(self, _, touch):
        is_text_input = False

        def check_if_text_input_focused(widget):
            for child in widget.children:
                check_if_text_input_focused(child)

            if (isinstance(widget, TextInput) or isinstance(widget, ScoreNotationCanvas)) and widget.collide_point(*touch.pos):
                nonlocal is_text_input
                is_text_input = True
                widget.on_touch_down(touch)

        check_if_text_input_focused(self.root)

        if not is_text_input and self._keyboard is None:
            self._set_keyboard()

    def on_start(self):
        if self.initial_filename is not None:
            self._load_file(self, self.initial_filename)

    def build(self):
        root = BoxLayout(orientation='horizontal')
        root.add_widget(self._build_menu())
        root.add_widget(self._build_views())
        root.bind(on_touch_down=self._recapture_keyboard)

        return root

    def _build_menu(self):
        width = 300

        self.menu = ListView(self._chunks, self._build_chunk_menu_item, width=width, size_hint_x=None, size_hint_y=None)
        self.menu.bind(selected_element=self._update_chunk)

        scroll_view = ScrollView(size_hint_x=None, width=width)
        scroll_view.add_widget(self.menu)

        return scroll_view

    def _build_chunk_menu_item(self, index, chunk, parent):
        text = chunk[1]
        if self.current_chunk.index == index:
            text = f'[b]{text}[/b]'

        return Label(text=text, halign='left', text_size=(parent.width, None), markup=True)

    def _build_views(self):
        self.default_view = TextInput(font_name=self.FONT_NAME, readonly=True)
        self.views = {key: view_class(font_name=self.FONT_NAME) for key, view_class in CHUNK_VIEW_MAP.items()}

        self.view_wrapper = BoxLayout()
        self.view_wrapper.add_widget(self.default_view)

        return self.view_wrapper

    def _on_keyboard_down(self, _, keycode, __, modifiers):
        current = self.menu.selected_element.index

        if keycode[1] == 'up':
            self.menu.select_item(max(0, current - 1))
        elif keycode[1] == 'down':
            self.menu.select_item(min(len(self._chunks) - 1, current + 1))
        elif 'ctrl' in modifiers and keycode[1] == 'o':
            self._open_file_chooser()

    def _update_chunk(self, _, indexed_item):
        self.previous_chunk = self.current_chunk
        self.current_chunk = indexed_item

    def _open_file_chooser(self):
        if not self.file_dialog.is_opened:
            self.file_dialog.open()

    def _load_file(self, _, filename):
        self._set_title(filename)

        # Parse director file
        self.file_disassembler = FileDisassembler(silent=True)
        self.file_disassembler.load_file(filename)
        self.file_disassembler.unpack()

        # Populate GUI
        self._set_chunks()
        self._load_chunks_into_menu()

    def _set_title(self, filename=None):
        self.title = 'Director cast explorer'
        if filename is not None:
            self.title += f': {filename}'

    def _set_chunks(self):
        self._chunks = []
        type_counts = {}
        for (address, chunk) in self.file_disassembler.chunks:
            chunk_name = chunk.__class__.__name__
            chunk_count = type_counts.get(chunk_name, 0)
            type_counts[chunk_name] = chunk_count + 1

            self._chunks.append((chunk_count, f'{chunk_name} #{chunk_count} (addr: 0x{chunk.resource.chunk_address:X})', chunk))

    def _load_chunks_into_menu(self):
        self.menu.clear_list_items()
        for chunk in self._chunks:
            self.menu.add_list_item(chunk)

        Clock.schedule_once(lambda _: self.menu.select_item(0))

    def on_current_chunk(self, _, chunk):
        if chunk == self.previous_chunk:
            return

        if self.current_chunk.item is not None:
            chunk = self.current_chunk.item[2]

        if isinstance(chunk, ChunkParser):
            if chunk.__class__.__name__ in self.views:
                key = chunk.__class__.__name__
            elif isinstance(chunk, EntryMapChunkParser):
                key = EntryMapChunkParser.__name__
            else:
                key = ChunkParser.__name__

            view = self.views[key]
            view.load(self.file_disassembler, chunk)
        else:
            view = self.default_view
            view.text = repr(chunk)
            scroll_to_top(view)

        self.view_wrapper.clear_widgets()
        self.view_wrapper.add_widget(view)
