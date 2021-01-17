from kivy.uix.gridlayout import GridLayout

from tonguetwister.gui.widgets.generic.labels import FixedSizeLabel
from tonguetwister.gui.widgets.generic.props import FixedSize


class KeyedLabel(FixedSizeLabel):
    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key


class LabelCollection(GridLayout, FixedSize):
    row_height = 20
    spacing = (10, 0)

    def __init__(self, rows=1, cols=1, col_widths=None, labels=None, **kwargs):
        super().__init__(rows=rows, cols=cols*2, **kwargs)

        self.col_widths = col_widths if col_widths is not None else [100]
        self.labels = labels if labels is not None else [{'key': '', 'title': ''}]
        self.keys = [label['key'] for label in self.labels if 'key' in label]

        self.build()

    def build(self):
        for label in self.labels:
            self.add_label(**label)

    def add_label(self, key=None, title=None):
        title_width, value_width = self.get_width()

        text = f'{title}:' if title is not None else ''
        label = KeyedLabel(text=text, width=title_width, height=self.row_height, halign='right')
        self.add_widget(label)

        label = KeyedLabel(text='', width=value_width, height=self.row_height, key=key)
        self.add_widget(label)

    def get_width(self):
        width = self.col_widths[len(self.children) // 2 % len(self.col_widths)]
        if isinstance(width, (tuple, list)):
            return width
        else:
            return width, width

    def load(self, labels):
        for key, value in labels.items():
            if key not in self.keys:
                raise AttributeError(f'{key} not found in labels definition {self.keys}')

            self.load_key(key, value)

    def load_key(self, key, value):
        label = self.find_label(key)
        label.text = str(value)

    def find_label(self, key):
        for label in self.children:
            if label.key == key:
                return label
