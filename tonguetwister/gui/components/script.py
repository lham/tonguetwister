from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput

from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.components.chunk import DefaultRecordsChunkView
from tonguetwister.gui.generic.props import MonoFont
from tonguetwister.gui.utils import load_script_function, update_text_area, highlight_word_in_text_area
from tonguetwister.lib.helper import exception_as_lines


class ScriptPanel(BoxLayout):
    current_function_index = NumericProperty(0)

    # TODO: Remove inspection warning
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.namelist = None

        self.current_script = None
        self.current_script_index = 0

        self.orientation = 'vertical'
        self.spacing = 0

        self.add_widget(self._build_action_bar())
        self.add_widget(self._build_panel())

    def _build_action_bar(self):
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

    def _build_panel(self):
        self.text_area_generated = TextInput(font_name=MonoFont.font_name)
        self.text_area_reconstructed = TextInput(font_name=MonoFont.font_name)
        self.text_area_named = TextInput(font_name=MonoFont.font_name)
        self.text_area_raw = TextInput(font_name=MonoFont.font_name)
        self.text_area_chunk = DefaultRecordsChunkView(font_name=MonoFont.font_name)

        self.text_area_generated.bind(on_touch_down=self._on_text_area_touch_down)
        self.text_area_reconstructed.bind(on_touch_down=self._on_text_area_touch_down)
        self.text_area_named.bind(on_touch_down=self._on_text_area_touch_down)
        self.text_area_raw.bind(on_touch_down=self._on_text_area_touch_down)

        tab1 = TabbedPanelItem(text='Generated Code')
        tab1.add_widget(self.text_area_generated)
        tab2 = TabbedPanelItem(text='Reconstructed Ops')
        tab2.add_widget(self.text_area_reconstructed)
        tab3 = TabbedPanelItem(text='Named Ops')
        tab3.add_widget(self.text_area_named)
        tab4 = TabbedPanelItem(text='Raw ops')
        tab4.add_widget(self.text_area_raw)
        tab5 = TabbedPanelItem(text='Chunk info')
        tab5.add_widget(self.text_area_chunk)

        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=150, tab_height=30)
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)
        tabbed_panel.add_widget(tab3)
        tabbed_panel.add_widget(tab4)
        tabbed_panel.add_widget(tab5)

        return tabbed_panel

    def load(self, file_disassembler: FileDisassembler, index, script):
        self.namelist = file_disassembler.namelist

        self.current_function_index = 0
        self.current_script_index = index
        self.current_script = script
        self._render_script()
        self.text_area_chunk.load(script)

    def _update_function_index(self, amount):
        n_functions = len(self.current_script.functions)

        self.current_function_index = (self.current_function_index + amount) % n_functions
        self._render_script()

    def _render_script(self):
        decompiler = load_script_function(
            self.current_script_index,
            self.current_function_index,
            self.namelist,
            self.current_script
        )

        Clock.schedule_once(lambda _: self._update_script_display(decompiler), 0)

    def _update_script_display(self, result):
        self.function_index_label.text = f'Function index: {self.current_function_index}'
        self.function_name_label.text = f'Function: {result.function_name}'

        generated_code_lines = exception_as_lines(result.exception) if result.has_exception() else result.generated_code

        update_text_area(self.text_area_raw, result.detokenized_operators, line_numbers=False)
        update_text_area(self.text_area_named, result.named_operators, line_numbers=False)
        update_text_area(self.text_area_reconstructed, result.reconstructed_operators)
        update_text_area(self.text_area_generated, generated_code_lines)

    @staticmethod
    def _on_text_area_touch_down(text_area, touch):
        if text_area.collide_point(*touch.pos) and not touch.is_double_tap:
            Clock.schedule_once(lambda _: highlight_word_in_text_area(text_area), 0)

