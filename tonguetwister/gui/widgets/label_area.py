from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class LabelArea(GridLayout):
    def __init__(self, field_names: dict, key_width=200, item_height=20, **kwargs):
        super().__init__(**kwargs)
        self._field_titles = field_names
        self._key_width = key_width

        self.cols = 2
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.row_default_height = item_height
        self.row_force_default = True
        self.spacing = (10, 0)

        self._value_fields = {}
        self._build()

    def _build(self):
        for key, title in self._field_titles.items():
            title_label = Label(
                text=f'{title}:',
                width=self._key_width,
                size_hint_x=None,
                halign='right',
                valign='middle',
            )
            title_label.bind(size=title_label.setter('text_size'))
            self.add_widget(title_label)

            value_label = Label(halign='left', valign='middle')
            value_label.bind(size=value_label.setter('text_size'))
            self.add_widget(value_label)
            self._value_fields[key] = value_label

    def load(self, field_values: dict):
        for key, value in field_values.items():
            if key in self._value_fields:
                self._value_fields[key].text = value
            else:
                print(f'WARNING: Trying to set value {value} for field {key} but that field does not exist')
