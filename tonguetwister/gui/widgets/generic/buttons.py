from kivy.uix.button import Button

from tonguetwister.gui.widgets.generic.props import FixedSize


class ArrowButton(Button, FixedSize):
    def __init__(self, on_click=None, **kwargs):
        super().__init__(width=50, height=30, **kwargs)
        self.on_click = on_click

    def on_press(self):
        if self.on_click is not None:
            self.on_click()


class LeftButton(ArrowButton):
    def __init__(self, **kwargs):
        super().__init__(text='<--', **kwargs)


class RightButton(ArrowButton):
    def __init__(self, **kwargs):
        super().__init__(text='-->', **kwargs)
