from kivy.uix.widget import Widget


class MonoFont:
    font_name = 'UbuntuMono-R.ttf'


class FixedSize(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)

    def on_minimum_size(self, _, size):
        self.size = size


class FixedHeight(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, **kwargs)

    def on_minimum_height(self, _, height):
        self.height = height


class FixedWidth(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint_x=None, **kwargs)

    def on_minimum_width(self, _, width):
        self.width = width
