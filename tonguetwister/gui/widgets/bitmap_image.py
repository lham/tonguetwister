from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class BitmapImage(Widget):
    MIN_ZOOM = 1
    MAX_ZOOM = 32

    scale = NumericProperty(1.0)

    def __init__(self, resizeable=False, color_format='rgb', **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.size_hint_y = None

        self._color_format = color_format
        self._image_width = None
        self._image_height = None
        self._data = None
        self._context = None

        self._resizeable = resizeable
        self._scaled_width = None
        self._scaled_height = None
        self._scaled_data = None

    def display(self, width, height, data, color_format=None):
        self._image_width = width
        self._image_height = height
        self._data = data
        self._color_format = color_format if color_format is not None else self._color_format

        if self._resizeable:
            self.unbind(scale=lambda *_: self._update_by_scale())

        self.scale = 1.0
        self._update_by_scale()

        if self._resizeable:
            self.bind(scale=lambda *_: self._update_by_scale())

    def _update_by_scale(self):
        self._scaled_width = self._image_width * int(self.scale)
        self._scaled_height = self._image_height * int(self.scale)
        self._scaled_data = self._compute_scaled_data()
        self.size = (self._scaled_width, self._scaled_height)

        self._create_context()
        Clock.schedule_once(self._update_context, 0)

    def _create_context(self):
        self._context = Texture.create(size=(self._scaled_width, self._scaled_height))

    def _update_context(self, _):
        self._context.blit_buffer(self._scaled_data, colorfmt=self._color_format, bufferfmt='ubyte')
        self._draw_context()
        self.bind(size=self._draw_context, pos=self._draw_context)

    def _draw_context(self, *_):
        with self.canvas:
            self.canvas.clear()
            Rectangle(texture=self._context, pos=self.pos, size=(self._scaled_width, self._scaled_height))

    def on_touch_down(self, touch):
        if not self._resizeable:
            return False

        if touch.is_mouse_scrolling and self.collide_point(*touch.pos):
            if touch.button == 'scrolldown':
                self.scale = min(self.scale * 2, self.MAX_ZOOM)
            elif touch.button == 'scrollup':
                self.scale = max(self.scale * 0.5, self.MIN_ZOOM)

    def _compute_scaled_data(self):
        if not self._resizeable:
            return self._data

        # Convert byte string into a color tuple list
        step_size = len(self._color_format)
        color_tuples = [tuple(self._data[i:i+step_size]) for i in range(0, len(self._data), step_size)]

        # Resize: first duplicate each row, then duplicate each color tuple. Duplicate "scale" times.
        duplications = range(int(self.scale))

        rows = [tuple(color_tuples[i:i+self._image_width]) for i in range(0, len(color_tuples), self._image_width)]
        rows = [row for row in rows for _ in duplications]

        color_tuples = [color_tuple for row in rows for color_tuple in row]
        color_tuples = [color_tuple for color_tuple in color_tuples for _ in duplications]

        # Convert back to byte array
        return bytes([color_byte for color_tuple in color_tuples for color_byte in color_tuple])
