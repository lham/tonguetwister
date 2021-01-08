from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class VerticalStackLayout(GridLayout):
    def __init__(self,
                 cols=1,
                 size_hint_y=None,
                 row_default_height=20,
                 row_force_default=True,
                 spacing=(0, 0),
                 **kwargs):
        super().__init__(
            cols=cols,
            size_hint_y=size_hint_y,
            row_default_height=row_default_height,
            row_force_default=row_force_default,
            spacing=spacing,
            **kwargs
        )

    def on_minimum_height(self, _, height):
        self.height = height


class FixedWidthLabel(Label):
    def __init__(self, text, width, halign, size_hint_x=None, valign='middle', **kwargs):
        super().__init__(text=text, width=width, halign=halign, size_hint_x=size_hint_x, valign=valign, **kwargs)

    def on_size(self, _, size):
        self.text_size = size
