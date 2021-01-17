from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from tonguetwister.gui.widgets.generic.props import MonoFont


class MonoReadOnlyTextInput(TextInput):
    readonly = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = MonoFont.font_name

    def scroll_to_top(self):
        Clock.schedule_once(lambda _: setattr(self, 'cursor', (0, 0)))
