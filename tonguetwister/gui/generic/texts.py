from kivy.uix.textinput import TextInput

from tonguetwister.gui.generic.props import MonoFont
from tonguetwister.gui.utils import scroll_to_top


class MonoReadOnlyTextInput(TextInput):
    readonly = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = MonoFont.font_name

    def scroll_to_top(self):
        scroll_to_top(self)
