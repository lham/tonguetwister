from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class LoadFileDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, base_dir=None, **kwargs):
        super().__init__(**kwargs)
        self.base_dir = base_dir
        self.file_chooser = None
        self._build()

    def _build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self._build_file_chooser())
        self.layout.add_widget(self._build_button_row())

        self.add_widget(self.layout)

    def _build_button_row(self):
        button_cancel = Button(text='Cancel')
        button_cancel.bind(on_release=self.cancel)
        button_load = Button(text='Load')
        button_load.bind(on_release=self._on_load)

        button_row = BoxLayout(size_hint_y=None, height=30)
        button_row.add_widget(button_cancel)
        button_row.add_widget(button_load)

        return button_row

    def _build_file_chooser(self):
        self.file_chooser = FileChooserListView()

        if self.base_dir is not None:
            self.file_chooser.path = self.base_dir

        return self.file_chooser

    def _on_load(self, _):
        files = self.file_chooser.selection

        if len(files) == 1:
            self.load(files[0])
        else:
            popup = Popup(
                title='Error',
                content=Label(text='Please select a file to load'),
                size_hint=(None, None),
                size=(300, 150)
            )
            popup.open()

    def on_size(self, _, size):
        self.layout.size = size

    def on_pos(self, _, pos):
        self.layout.pos = pos


class FileDialogPopup(Widget):
    file_opened = StringProperty('')
    is_opened = BooleanProperty(False)

    def __init__(self, title='Load file', base_dir=None, size=(600, 400), **kwargs):
        super().__init__(**kwargs)
        self.popup = Popup(
            title=title,
            content=LoadFileDialog(base_dir=base_dir, load=self._load, cancel=lambda _: self.close()),
            size_hint=(None, None),
            size=size,
            auto_dismiss=False
        )

    def _load(self, filename):
        self.file_opened = filename
        self.close()

    def open(self):
        self.popup.open()
        self.is_opened = True

    def close(self):
        self.popup.dismiss()
        self.is_opened = False
