from kivy.uix.label import Label

from tonguetwister.gui.widgets.generic.effects import Highlight
from tonguetwister.gui.widgets.generic.props import MonoFont


class FixedSizeLabel(MonoFont, Label):
    size_hint = (None, None)

    def __init__(self, text, width, height, halign='left', **kwargs):
        super().__init__(text=text, width=width, height=height, halign=halign, **kwargs)

    def on_size(self, _, size):
        self.text_size = size


class FixedSizeLinkLabel(FixedSizeLabel, Highlight):
    underline = True

    def __init__(self, *args, link_target=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.link_target = link_target

    def on_touch_down(self, touch):
        if self.link_target is not None and self.collide_point(*touch.pos) and touch.button == 'left':
            self.link_target()
            return True
