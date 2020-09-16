from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.gridlayout import GridLayout

from tonguetwister.gui.widgets.bitmap_image import BitmapImage


class PaletteDisplay(GridLayout):
    def __init__(self, palette, swatch_width=40, swatch_height=20, spacing=1, **kwargs):
        super().__init__(**kwargs)
        self._palette = palette
        self._swatch_width = swatch_width
        self._swatch_height = swatch_height

        self.spacing = spacing
        self.cols = 16
        self.rows = 16
        self.col_default_width = swatch_width
        self.row_default_height = swatch_height
        self.col_force_default = True
        self.row_force_default = True
        self.padding = (spacing, spacing, spacing, spacing)

        self._swatches = [BitmapImage() for _ in self._palette]
        for widget in self._swatches:
            self.add_widget(widget)

        self.bind(size=self._update_rect, pos=self._update_rect)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        Clock.schedule_once(self._load, 0)

    def _load(self, _):
        for i, color in enumerate(self._palette):
            self._swatches[i].display(self._swatch_width, self._swatch_height, self._data(color))

    def _data(self, color):
        size = self._swatch_width * self._swatch_height
        return bytes([color_value for _ in range(size) for color_value in color])

    def _update_rect(self, _, __):
        spacing_x, spacing_y = self.spacing
        left, top, right, bottom = self.padding

        width = (self._swatch_width * self.cols) + spacing_x * (self.cols - 1) + (left + right)
        height = (self._swatch_height * self.rows) + spacing_y * (self.rows - 1) + (top + bottom)

        pos_x = self.pos[0]
        pos_y = self.pos[1] + self.size[1] - height

        self.rect.pos = (pos_x, pos_y)
        self.rect.size = (width, height)

