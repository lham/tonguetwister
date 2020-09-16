from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.widget import Widget


class BitmapImage(Widget):
    def __init__(self, color_format='rgb', **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.size_hint_y = None

        self._color_format = color_format
        self._image_width = None
        self._image_height = None
        self._data = None
        self._context = None

    def display(self, width, height, data):
        self._image_width = width
        self._image_height = height
        self._data = data

        self._create_context()
        Clock.schedule_once(self._update_context, 0)

    def _create_context(self):
        self._context = Texture.create(size=(self._image_width, self._image_height))

    def _update_context(self, _):
        self._context.blit_buffer(self._data, colorfmt=self._color_format, bufferfmt='ubyte')
        self._draw_context()
        self.bind(size=self._draw_context, pos=self._draw_context)

    def _draw_context(self, *_):
        with self.canvas:
            self.canvas.clear()
            Rectangle(texture=self._context, pos=self.pos, size=(self._image_width, self._image_height))
