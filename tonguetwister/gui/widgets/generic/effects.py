from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget


class Highlight(Widget):
    COLOR_NORMAL = (1, 1, 1, 1)
    COLOR_HIGHLIGHT = (1, 1, 0.2, 1)

    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    # noinspection PyMethodMayBeStatic
    def highlight_enabled(self):
        return True

    def on_mouse_pos(self, _, mouse_pos):
        if not self.get_root_window():
            return  # Not displayed

        if self.collide_point(*self.to_widget(*mouse_pos)):
            self.hovered = True
        elif self.hovered:
            self.hovered = False

    def on_hovered(self, _, hovered):
        for widget in self.children:
            self.highlight_widget(widget, hovered)

        if len(self.children) == 0:
            self.highlight_widget(self, hovered)

    def highlight_widget(self, widget, hovered):
        if hovered and self.highlight_enabled():
            widget.color = self.COLOR_HIGHLIGHT
        else:
            widget.color = self.COLOR_NORMAL
