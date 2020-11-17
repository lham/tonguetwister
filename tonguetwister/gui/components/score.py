import os

from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from tonguetwister.chunks.video_works_score import VideoWorksScore, Sprite, EmptySprite
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.components.chunk import DefaultChunkView
from tonguetwister.gui.utils import scroll_to_top
from tonguetwister.gui.widgets.label_area import LabelArea


class ScoreView(BoxLayout):
    score: VideoWorksScore

    byte_change_notation_area_offset = NumericProperty(0)
    BYTE_CHANGE_NOTATION_AREA_WIDTH = 50

    def __init__(self, font_name, **kwargs):
        super().__init__(**kwargs)
        self.font_name = font_name

        self.add_widget(self._build_tabbed_panel())

    def _build_tabbed_panel(self):
        self.text_area = DefaultChunkView(font_name=self.font_name)

        tab1 = TabbedPanelItem(text='Score View')
        tab1.add_widget(self._build_reconstructed_area())
        tab2 = TabbedPanelItem(text='Byte Change Notation')
        tab2.add_widget(self._build_byte_change_notation_area())
        tab3 = TabbedPanelItem(text='Raw Chunk Info')
        tab3.add_widget(self.text_area)

        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=170, tab_height=30)
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)
        tabbed_panel.add_widget(tab3)

        return tabbed_panel

    def _build_reconstructed_area(self):
        self.score_wrapper = BoxLayout(orientation='vertical')
        self.raw_area_sprite = Label(
            font_name=self.font_name, halign='left', valign='top', height=240, size_hint_y=None)
        self.raw_area_sprite.bind(size=self.raw_area_sprite.setter('text_size'))
        self.raw_area_sprite_span = Label(
            font_name=self.font_name, halign='left', valign='top', height=240, size_hint_y=None)
        self.raw_area_sprite_span.bind(size=self.raw_area_sprite_span.setter('text_size'))
        self.info_area_sprite = LabelArea({
            'x': ('x', 1),
            'y': ('y', 1),
            'width': ('Width', 1),
            'height': ('Height', 1),
            'cast_member': ('Cast Member', 0),
            'start': ('Start', 0),
            'end': ('End', 0),
            'length': ('Length', 0),
            'ink': ('Ink', 2),
            'blend': ('Blend', 2),
            'editable': ('Editable', 3),
            'moveable': ('Moveable', 3),
            'tails': ('Trails', 3)
        }, key_width=100)
        self.info_area_sprite_span = LabelArea({
            'tween_path': ('Tween Path', 0),
            'tween_size': ('Tween Size', 0),
            'tween_blend': ('Tween Blend', 0),
            'tween_fg': ('Tween Foreground Color', 0),
            'tween_bg': ('Tween Background Color', 0),
            'tween_curvature': ('Curvature', 1),
            'tween_continuous': ('Continuous at Endpoints', 1),
            'tween_speed': ('Speed', 2),
            'tween_ease_in': ('Ease-In', 3),
            'tween_ease_out': ('Ease-Out', 3),
        })

        layout_raw = BoxLayout(orientation='horizontal')
        layout_raw.add_widget(self.raw_area_sprite)
        layout_raw.add_widget(self.raw_area_sprite_span)

        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(self.info_area_sprite)
        layout.add_widget(self.info_area_sprite_span)
        layout.add_widget(layout_raw)
        layout.add_widget(self.score_wrapper)

        return layout

    def _build_byte_change_notation_area(self):
        width = int(self.BYTE_CHANGE_NOTATION_AREA_WIDTH * 0.9)

        next_button = Button(text='->', width=50, size_hint_x=None)
        next_button.bind(on_press=lambda instance: self._update_byte_change_notation_area_offset(width))
        prev_button = Button(text='<-', width=50, size_hint_x=None)
        prev_button.bind(on_press=lambda instance: self._update_byte_change_notation_area_offset(-width))

        action_bar = StackLayout(orientation='rl-tb', height=30, size_hint_y=None)
        action_bar.add_widget(next_button)
        action_bar.add_widget(prev_button)

        self.byte_change_notation_area = TextInput(readonly=True, font_name=self.font_name)

        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(action_bar)
        layout.add_widget(self.byte_change_notation_area)

        return layout

    def _update_byte_change_notation_area_offset(self, diff):
        _min = 0
        _max = self.score.number_of_bytes_per_frame - self.BYTE_CHANGE_NOTATION_AREA_WIDTH + 1

        if self.byte_change_notation_area_offset + diff < _min:
            self.byte_change_notation_area_offset = _min
        elif self.byte_change_notation_area_offset + diff > _max:
            self.byte_change_notation_area_offset = _max
        else:
            self.byte_change_notation_area_offset += diff

    def load(self, file_disassembler: FileDisassembler, score: VideoWorksScore):
        self.score = score

        self.text_area.load(file_disassembler, score)
        self._load_byte_change_notation_area()
        self._show_load_score_text()

        Clock.schedule_once(lambda _: self._load_score(), 0.5)

    def _load_byte_change_notation_area(self):
        if self.byte_change_notation_area_offset == 0:
            self.on_byte_change_notation_area_offset(self, 0)
        else:
            self.byte_change_notation_area_offset = 0

    def on_byte_change_notation_area_offset(self, _, offset):
        length = self.BYTE_CHANGE_NOTATION_AREA_WIDTH
        self.byte_change_notation_area.text = self.score.text_representation_frames(offset, length, True)
        scroll_to_top(self.byte_change_notation_area)

    def _show_load_score_text(self):
        self.score_wrapper.clear_widgets()
        self.score_wrapper.add_widget(Label(text='Loading score notation...'))

    def _load_score(self):
        notation = ScoreNotation(self.score, self.font_name)
        notation.bind(selected=self._display_sprite_data)

        self.score_wrapper.clear_widgets()
        self.score_wrapper.add_widget(notation)

    def _display_sprite_data(self, _, sprite):
        if isinstance(sprite, Sprite):
            sprite_span = sprite.sprite_span

            self.info_area_sprite.load({
                'x': f'{sprite.x:d}',
                'y': f'{sprite.y:d}',
                'width': f'{sprite.width:d}',
                'height': f'{sprite.height:d}',
                'start': sprite_span.start + 1,
                'end': sprite_span.end + 1,
                'length': sprite_span.end - sprite_span.start + 1,
                'ink': sprite.ink,
                'blend': f'{int(round(sprite.blend*100))}%',
                'editable': sprite.editable,
                'moveable': sprite.moveable,
                'tails': sprite.trails,
                'cast_member': sprite.cast_member
            })

            self.info_area_sprite_span.load({
                'tween_path': sprite_span.tween_path,
                'tween_size': sprite_span.tween_size,
                'tween_blend': sprite_span.tween_blend,
                'tween_fg': sprite_span.tween_foreground_color,
                'tween_bg': sprite_span.tween_background_color,
                'tween_curvature': f'{int(round(sprite_span.tween_curvature*100))}%',
                'tween_continuous': sprite_span.tween_is_continuous_at_endpoints,
                'tween_speed': sprite_span.tween_speed,
                'tween_ease_in': f'{sprite_span.tween_ease_in}%',
                'tween_ease_out': f'{sprite_span.tween_ease_out}%',
            })
            # noinspection PyProtectedMember
            self.raw_area_sprite.text = os.linesep\
                .join(f'{k}: {v}' for k, v in sprite._data.items() if k.startswith('u') or k.startswith('?'))
            # noinspection PyProtectedMember
            self.raw_area_sprite_span.text = os.linesep\
                .join(f'{k}: {v}' for k, v in sprite_span._data.items() if k.startswith('u') or k.startswith('?'))
        else:
            self.info_area_sprite.load({
                'x': '',
                'y': '',
                'width': '',
                'height': '',
                'start': '',
                'end': '',
                'length': '',
                'ink': '',
                'blend': '',
                'editable': '',
                'moveable': '',
                'tails': '',
                'cast_member': ''
            })
            self.info_area_sprite_span.load({
                'tween_path': '',
                'tween_size': '',
                'tween_blend': '',
                'tween_fg': '',
                'tween_bg': '',
                'tween_curvature': '',
                'tween_continuous': '',
                'tween_speed': '',
                'tween_ease_in': '',
                'tween_ease_out': '',
            })
            self.raw_area_sprite.text = ''
            self.raw_area_sprite_span.text = ''


class ScoreNotation(BoxLayout):
    selected = ObjectProperty(EmptySprite())

    def __init__(self, score: VideoWorksScore, font_name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        notation = ScoreNotationCanvas(score, font_name)
        notation.bind(selected=lambda _, box: setattr(self, 'selected', box.sprite))

        layout = AnchorLayout(anchor_x='left', anchor_y='top', size=notation.size, size_hint=[None, None])
        layout.add_widget(notation)

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)


class ScoreNotationCanvas(FocusBehavior, Widget):
    SPRITE_BOX_WIDTH = 12
    SPRITE_BOX_HEIGHT = 18

    CHANNEL_LABEL_WIDTH = 70
    FRAME_LABEL_HEIGHT = 15

    COLOR_WHITE = (1, 1, 1, 1)
    COLOR_BLACK = (0.2, 0.2, 0.2, 1)
    COLOR_SHADED_DARK = (0.5, 0.5, 0.5, 1)
    COLOR_SHADED_LIGHT = (0.8, 0.8, 0.8, 1)
    COLOR_SELECTED = (0.73, 0.34, 0.49, 1)
    COLOR_SPRITE = (0.49, 0.73, 0.34, 1)
    COLOR_SPRITE_SPAN = COLOR_WHITE
    COLOR_SPRITE_KEYFRAME = (0.34, 0.49, 0.73)

    selected = ObjectProperty(None)

    def __init__(self, score: VideoWorksScore, font_name, **kwargs):
        super().__init__(**kwargs)
        self.score = score
        self.font_name = font_name

        self.n_frames = score.number_of_frames
        self.n_channels = score.highest_channel_used + 1
        self.spacing = 1

        self.size_hint = (None, None)
        self.width = self.n_frames * (self.SPRITE_BOX_WIDTH + self.spacing) + self.CHANNEL_LABEL_WIDTH
        self.height = self.n_channels * (self.SPRITE_BOX_HEIGHT + self.spacing) + self.FRAME_LABEL_HEIGHT
        self.bind(size=self.update_coordinates_and_render, pos=self.update_coordinates_and_render)

        self.sprite_box_list_store = []
        self.sprite_box_dict_store = {}
        self.construct_sprite_boxes()
        self.update_coordinates_and_render()

    def construct_sprite_boxes(self):
        for frame_no in range(self.n_frames):
            for channel_no in range(self.n_channels):
                box = SpriteBox(frame_no, channel_no, self.score.sprite_at(frame_no, channel_no))
                self.sprite_box_list_store.append(box)
                self.sprite_box_dict_store[(frame_no, channel_no)] = box

    def update_coordinates_and_render(self, *_):
        for box in self.sprite_box_list_store:
            box.update_pos(self.spacing, self.size, self.sprite_box_offset())

        self.render()

    def sprite_box_offset(self):
        x_pos, y_pos = self.pos

        return [x_pos + self.CHANNEL_LABEL_WIDTH + self.spacing, y_pos - self.FRAME_LABEL_HEIGHT - self.spacing]

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.selected is None:
            return

        frame_no = self.selected.frame_no
        channel_no = self.selected.channel_no

        if keycode[1] == 'up':
            channel_no = (channel_no - 1) % self.n_channels
        elif keycode[1] == 'down':
            channel_no = (channel_no + 1) % self.n_channels
        elif keycode[1] == 'left':
            frame_no = (frame_no - 1) % self.n_frames
        elif keycode[1] == 'right':
            frame_no = (frame_no + 1) % self.n_frames

        self.selected = self.sprite_box_dict_store[(frame_no, channel_no)]

    def render(self, *_):
        self.canvas.clear()
        with self.canvas:
            for box in self.sprite_box_list_store:
                self.render_sprite_box(box)
                if box.sprite_span is not None:
                    self.render_sprite_span_border(box)
                    self.render_keyframes(box)

            self.render_channel_labels()
            self.render_frame_labels()

            # Draw selected box
            if self.selected is not None:
                Color(*self.COLOR_SELECTED)
                Rectangle(
                    pos=[self.selected.pos[0] + 2, self.selected.pos[1] + 2],
                    size=[self.selected.size[0] - 4, self.selected.size[1] - 4]
                )

    def render_sprite_box(self, box):
        Color(*self.get_sprite_box_background_color(box))
        Rectangle(pos=box.pos, size=box.size)

    def render_sprite_span_border(self, box):
        Color(*self.COLOR_SPRITE_SPAN)
        x, y = box.pos
        width, height = box.size

        bl_x = tl_x = x
        bl_y = br_y = y + 2
        br_x = tr_x = x + width + self.spacing
        tl_y = tr_y = y + height - 2

        if box.sprite_span.start == box.frame_no:
            Line(points=[br_x, br_y, bl_x + 2, bl_y, tl_x + 2, tl_y, tr_x, tr_y], width=1, joint='miter')
        elif box.sprite_span.end == box.frame_no:
            Line(
                points=[bl_x, bl_y, br_x - self.spacing - 2, br_y, tr_x - self.spacing - 2, tr_y, tl_x, tl_y],
                width=1,
                joint='miter'
            )
        else:
            Line(points=[bl_x, bl_y, br_x, br_y], width=1)
            Line(points=[tl_x, tl_y, tr_x, tr_y], width=1)

    def render_keyframes(self, box):
        Color(*self.COLOR_BLACK)
        for keyframe_no in box.sprite_span.keyframes:
            if keyframe_no == box.frame_no:
                Line(circle=([
                    box.pos[0] + self.SPRITE_BOX_WIDTH / 2,
                    box.pos[1] + self.SPRITE_BOX_HEIGHT / 2,
                    self.SPRITE_BOX_WIDTH / 4
                ]))

    def render_frame_labels(self):
        x_offset, y_offset = self.sprite_box_offset()

        # Backdrop frame labels
        Color(*self.COLOR_BLACK)
        Rectangle(
            pos=[x_offset, y_offset + self.size[1] + 1],
            size=[(self.SPRITE_BOX_WIDTH + self.spacing) * self.n_frames - self.spacing, self.FRAME_LABEL_HEIGHT - 1]
        )

        Color(*self.COLOR_SHADED_LIGHT)
        Rectangle(
            pos=[x_offset, y_offset + self.size[1] + 2],
            size=[(self.SPRITE_BOX_WIDTH + self.spacing) * self.n_frames - self.spacing, self.FRAME_LABEL_HEIGHT - 4]
        )

        for frame_no in range(self.n_frames):
            x_pos = x_offset + (self.SPRITE_BOX_WIDTH + self.spacing) * frame_no
            y_pos = y_offset + self.size[1]

            Color(*self.COLOR_SHADED_LIGHT)
            if self.selected is not None and self.selected.frame_no == frame_no:
                Color(*[*self.COLOR_SHADED_LIGHT[0:3], 0.5])

            Rectangle(pos=[x_pos, y_pos], size=[self.SPRITE_BOX_WIDTH, self.FRAME_LABEL_HEIGHT - 1])

        # Frame label numbers
        for frame_no in range(self.n_frames):
            is_first = frame_no == 0
            is_fifth = (frame_no + 1) % 5 == 0
            is_selected = self.selected is not None and self.selected.frame_no == frame_no

            if not is_first and not is_fifth and not is_selected:
                continue

            x_pos = x_offset + (self.SPRITE_BOX_WIDTH + self.spacing) * frame_no
            y_pos = y_offset + self.size[1]

            label = CoreLabel(text=f'{frame_no + 1}', font_size=12, font_name=self.font_name)
            label.refresh()

            Color(*self.COLOR_BLACK)
            text_pos = [x_pos + (self.SPRITE_BOX_WIDTH - label.texture.size[0]) / 2, y_pos + 1]
            Rectangle(pos=text_pos, size=label.texture.size, texture=label.texture)

    def render_channel_labels(self):
        x_offset, y_offset = self.sprite_box_offset()

        for channel_no in range(self.n_channels):
            label = CoreLabel(text=self.get_channel_name(channel_no), font_size=12, font_name=self.font_name)
            label.refresh()

            row_offset = (self.SPRITE_BOX_HEIGHT + self.spacing) * channel_no
            y_pos = y_offset + self.size[1] - row_offset - self.SPRITE_BOX_HEIGHT - self.spacing

            Color(*self.COLOR_SHADED_LIGHT)
            if self.selected is not None and self.selected.channel_no == channel_no:
                Color(*[*self.COLOR_SHADED_LIGHT[0:3], 0.5])

            Rectangle(pos=[self.pos[0], y_pos], size=[self.CHANNEL_LABEL_WIDTH, self.SPRITE_BOX_HEIGHT])

            Color(*self.COLOR_BLACK)
            text_pos = [
                x_offset - self.spacing - label.texture.size[0] - 5,
                y_pos + (self.SPRITE_BOX_HEIGHT - label.texture.size[1])/2
            ]
            Rectangle(pos=text_pos, size=label.texture.size, texture=label.texture)

    def get_sprite_box_background_color(self, box):
        if box.is_sprite:
            return self.COLOR_SPRITE
        elif box.frame_no == 0 or (box.frame_no + 1) % 5 == 0:
            return self.COLOR_SHADED_LIGHT
        else:
            return self.COLOR_WHITE

    @staticmethod
    def get_channel_name(channel_no):
        if channel_no == 0:
            return 'Tempo'
        elif channel_no == 1:
            return 'Palette'
        elif channel_no == 2:
            return 'Transition'
        elif channel_no == 3:
            return 'Sound 1'
        elif channel_no == 4:
            return 'Sound 2'
        elif channel_no == 5:
            return 'Script'
        else:
            return f'Ch. {channel_no - 5}'

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return

        for box in self.sprite_box_list_store:
            if box.collide_point(*touch.pos):
                self.selected = box
                break

        return super().on_touch_down(touch)

    def on_selected(self, *_):
        self.render()


class SpriteBox:
    def __init__(self, frame_no, channel_no, sprite):
        self.frame_no = frame_no
        self.channel_no = channel_no
        self.sprite = sprite
        self.sprite_span = sprite.sprite_span

        self.x = 0
        self.y = 0
        self.width = ScoreNotationCanvas.SPRITE_BOX_WIDTH
        self.height = ScoreNotationCanvas.SPRITE_BOX_HEIGHT

    def update_pos(self, spacing, parent_size, offset_pos):
        self.x = self.frame_no * (self.width + spacing) + offset_pos[0]
        self.y = parent_size[1] - self.channel_no * (self.height + spacing) + offset_pos[1] - self.height - spacing

    @property
    def pos(self):
        return self.x, self.y

    @property
    def size(self):
        return self.width, self.height

    @property
    def is_sprite(self):
        return isinstance(self.sprite, Sprite)

    def collide_point(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
