from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from tonguetwister.gui.widgets.generic.props import FixedHeight, FixedWidth, FixedSize


class VerticalStackLayout(FixedHeight, GridLayout):
    cols = 1

    def __init__(self, spacing=(0, 0), **kwargs):
        super().__init__(spacing=spacing, **kwargs)


class HorizontalStackLayout(FixedWidth, GridLayout):
    rows = 1

    def __init__(self, spacing=(0, 0), **kwargs):
        super().__init__(spacing=spacing, **kwargs)


class FixedStackLayout(FixedSize, GridLayout):
    cols = 1

    def __init__(self, spacing=(0, 0), **kwargs):
        super().__init__(spacing=spacing, **kwargs)


class VerticalBoxLayout(BoxLayout):
    orientation = 'vertical'


class HorizontalBoxLayout(BoxLayout):
    orientation = 'horizontal'


class SideScrollView(ScrollView):
    scroll_type = ['bars']
    bar_width = 10


class ScrollContainer(GridLayout):
    cols = 1

    def __init__(self, **kwargs):
        super().__init__(size_hint_x=None, **kwargs)

        self.scroll_view = SideScrollView()
        self.add_widget(self.scroll_view)

    def add_scrolled_widget(self, widget):
        self.scroll_view.add_widget(widget)
        widget.bind(width=self.on_scrolled_widget_width)

    def on_scrolled_widget_width(self, _, width):
        self.width = width + self.scroll_view.bar_width + 1
