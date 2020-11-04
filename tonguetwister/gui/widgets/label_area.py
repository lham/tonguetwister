from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class LabelArea(BoxLayout):
    def __init__(self, fields: dict, key_width=200, item_height=20, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.bind(height=self.setter('minimum_height'))

        self.column_field_names = {}
        self.fields = {}

        for key, value in fields.items():
            if isinstance(value, (list, tuple)):
                title, column_id = self.fields[key] = value
            else:
                title, column_id = self.fields[key] = (value, 0)

            if column_id not in self.column_field_names:
                self.column_field_names[column_id] = {}
            self.column_field_names[column_id][key] = title

        self.areas = []
        for index, field_names in sorted(self.column_field_names.items(), key=lambda item: item[0]):
            area = LabelAreaColumn(field_names, key_width, item_height)
            self.areas.append(area)
            self.add_widget(area)

    def load(self, fields: dict):
        for key, value in fields.items():
            if key in self.fields:
                column_id = self.fields[key][1]
                self.areas[column_id].load(key, value)
            else:
                print(f'WARNING: Trying to set value {value} for field {key} but that field does not exist')


class LabelAreaColumn(GridLayout):
    def __init__(self, field_names: dict, key_width, item_height, **kwargs):
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
        for index, (key, title) in enumerate(self._field_titles.items()):
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

    def load(self, key, value):
        if key in self._value_fields:
            self._value_fields[key].text = str(value)
        else:
            print(f'WARNING: Trying to set value {value} for field {key} but that field does not exist')
