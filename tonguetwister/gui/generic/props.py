from kivy.uix.widget import Widget


class MonoFont:
    font_name = 'UbuntuMono-R.ttf'


class FixedSize(Widget):
    def __init__(self, size_hint=(None, None), **kwargs):
        super().__init__(size_hint=size_hint, **kwargs)

    def on_minimum_size(self, _, size):
        self.size = size


class FixedHeight(Widget):
    def __init__(self, size_hint_y=None, **kwargs):
        super().__init__(size_hint_y=size_hint_y, **kwargs)

    def on_minimum_height(self, _, height):
        self.height = height


class FixedWidth(Widget):
    def __init__(self, size_hint_x=None, **kwargs):
        super().__init__(size_hint_x=size_hint_x, **kwargs)

    def on_minimum_width(self, _, width):
        self.width = width
