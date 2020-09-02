import os
import re

# TODO: Change to using kivy.config?
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ["KIVY_NO_ARGS"] = '1'

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.cache import Cache
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from tonguetwister.gui.utils import update_text_area
from tonguetwister.gui.widgets.listview import ListView
from tonguetwister.lingo_decompiler import Decompiler
from tonguetwister.lib.helper import exception_as_lines


Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top',  0)
Window.size = (1600, 900)
Cache.register('decompiled', limit=20)


class IndexedScript:
    def __init__(self, index=None, script=None):
        self.index = index
        self.script = script


class DirectorCastExplorer(App):
    INITIAL_SCRIPT_INDEX = 5
    INITIAL_FUNCTION_INDEX = 0

    current_script = ObjectProperty(IndexedScript())
    current_function_index = NumericProperty(INITIAL_FUNCTION_INDEX)

    def __init__(self, parser_results):
        super().__init__()
        self.parser_results = parser_results
        self.scripts = list(self.parser_results.lingo_scripts.items())
        self.current_script = IndexedScript(self.INITIAL_SCRIPT_INDEX, self.scripts[self.INITIAL_SCRIPT_INDEX])

    def build(self):
        root = BoxLayout(orientation='horizontal', spacing=10)
        root.add_widget(self._build_menu())
        root.add_widget(self._build_display_area())

        return root

    def _build_menu(self):
        menu = ListView(self.scripts, self._build_script_item, self.current_script.index, width=200, size_hint_x=None)
        menu.bind(selected_element=self._update_script)

        return menu

    def _build_display_area(self):
        layout = BoxLayout(orientation='vertical', spacing=0)
        layout.add_widget(self._build_script_action_bar())
        layout.add_widget(self._build_script_panel())

        return layout

    def _build_script_action_bar(self):
        next_function = Button(text='Next', width=50, size_hint_x=None)
        next_function.bind(on_press=lambda instance: self._update_function_index(1))
        prev_function = Button(text='Prev', width=50, size_hint_x=None)
        prev_function.bind(on_press=lambda instance: self._update_function_index(-1))
        self.function_index_label = Label(width=150, size_hint_x=None)
        self.function_name_label = Label()

        action_bar = StackLayout(orientation='rl-tb', height=30, size_hint_y=None)
        action_bar.add_widget(self.function_name_label)
        action_bar.add_widget(next_function)
        action_bar.add_widget(self.function_index_label)
        action_bar.add_widget(prev_function)

        return action_bar

    def _build_script_panel(self):
        tab1 = TabbedPanelItem(text='Generated Code')
        self.text_area_generated = TextInput(text='Select a script to inspect it', font_name='UbuntuMono-R.ttf')
        self.text_area_generated.bind(on_touch_down=self._on_text_area_touch_down)
        tab1.add_widget(self.text_area_generated)

        tab2 = TabbedPanelItem(text='Reconstructed Ops')
        self.text_area_reconstructed = TextInput(text='Select a script to inspect it', font_name='UbuntuMono-R.ttf')
        tab2.add_widget(self.text_area_reconstructed)

        tab3 = TabbedPanelItem(text='Named Ops')
        self.text_area_named = TextInput(text='Select a script to inspect it', font_name='UbuntuMono-R.ttf')
        tab3.add_widget(self.text_area_named)

        tab4 = TabbedPanelItem(text='Raw ops')
        self.text_area_raw = TextInput(text='Select a script to inspect it', font_name='UbuntuMono-R.ttf')
        tab4.add_widget(self.text_area_raw)

        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=150, tab_height=30)
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)
        tabbed_panel.add_widget(tab3)
        tabbed_panel.add_widget(tab4)

        return tabbed_panel

    def _build_script_item(self, index, script, parent):
        text = f'Script no {index} ({len(script[1].functions)} functions)'
        if self.current_script.index == index:
            text = f'[b]{text}[/b]'

        return Label(text=text, halign='left', valign='middle', text_size=(parent.width, None), markup=True)

    def _update_script(self, _, indexed_item):
        self.current_function_index = 0
        self.current_script = IndexedScript(indexed_item.index, indexed_item.item)

    def _update_function_index(self, amount):
        n_functions = len(self.current_script.script[1].functions)

        self.current_function_index = (self.current_function_index + amount) % n_functions
        self._render_script()

    def on_current_script(self, _, __):
        self._render_script()

    def _render_script(self):
        decompiler = self._get_current_script_function()
        Clock.schedule_once(lambda _: self._update_script_display(decompiler), 0)

    def _get_current_script_function(self):
        decompiler = self._get_decompiler_from_cache()
        if decompiler is None:
            decompiler = self._decompile_script_function(self.current_script.script[1])

        return decompiler

    def _decompile_script_function(self, script):
        namelist = self.parser_results.namelist
        function = script.functions[self.current_function_index]

        decompiler = Decompiler(catch_exceptions=True)
        decompiler.to_pseudo_code(function, namelist, script)

        self._store_decompiler_in_cache(decompiler)

        return decompiler

    def _store_decompiler_in_cache(self, decompiler):
        Cache.append('decompiled', f'script-{self.current_script.index}-{self.current_function_index}', decompiler)

    def _get_decompiler_from_cache(self):
        return Cache.get('decompiled', f'script-{self.current_script.index}-{self.current_function_index}')

    def _update_script_display(self, result):
        self.function_index_label.text = f'Function index: {self.current_function_index}'
        self.function_name_label.text = f'Function: {result.function_name}'

        generated_code_lines = exception_as_lines(result.exception) if result.has_exception() else result.generated_code

        update_text_area(self.text_area_raw, result.detokenized_operators, line_numbers=False)
        update_text_area(self.text_area_named, result.named_operators, line_numbers=False)
        update_text_area(self.text_area_reconstructed, result.reconstructed_operators)
        update_text_area(self.text_area_generated, generated_code_lines)

    def _on_text_area_touch_down(self, text_area, touch):
        if text_area.collide_point(*touch.pos) and not touch.is_double_tap:
            Clock.schedule_once(lambda _: self._highlight_word_in_text_area(text_area), 0)

    def _highlight_word_in_text_area(self, text_area):
        # noinspection PyProtectedMember
        current_line = text_area._lines[text_area.cursor_row]
        text_before_cursor = current_line[:text_area.cursor_col]
        text_after_cursor = current_line[text_area.cursor_col:]

        pattern = re.compile(r'[^A-Za-z0-9_]')

        start = [m.end(0) for m in re.finditer(pattern, text_before_cursor)]
        start = len(text_before_cursor) - (start[-1] if len(start) > 0 else 0)

        end = re.search(pattern, text_after_cursor)
        end = end.start() if end is not None else len(text_after_cursor)

        index_start = text_area.cursor_index() - start
        index_stop = text_area.cursor_index() + end

        result = text_area.text[index_start:index_stop]
        if len(result) > 0:
            Clock.schedule_once(lambda _: text_area.select_text(index_start, index_stop), 0)
