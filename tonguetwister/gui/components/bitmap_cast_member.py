from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from tonguetwister.disassembler.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.disassembler.file_disassembler2 import FileDisassembler
from tonguetwister.gui.components.chunk import DefaultChunkView
from tonguetwister.gui.widgets.bitmap_image import BitmapImage
from tonguetwister.gui.widgets.label_area import LabelArea
from tonguetwister.gui.widgets.palette import PaletteDisplay
from tonguetwister.lib.helper import flatten


class BitmapCastMemberView(BoxLayout):
    def __init__(self, font_name, **kwargs):
        super().__init__(**kwargs)
        self.font_name = font_name

        self.label_area = None
        self.image = None
        self.image_wrapper = None
        self.temp_palette = None

        self.add_widget(self._build_tabbed_panel())

    def _build_tabbed_panel(self):
        self.text_area = DefaultChunkView(font_name=self.font_name)
        self.reconstructed_area = self._build_reconstructed_area()

        tab1 = TabbedPanelItem(text='Reconstructed Data')
        tab1.add_widget(self.reconstructed_area)
        tab2 = TabbedPanelItem(text='Raw Chunk Info')
        tab2.add_widget(self.text_area)

        tabbed_panel = TabbedPanel(do_default_tab=False, tab_width=150, tab_height=30)
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)

        return tabbed_panel

    def _build_reconstructed_area(self):
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(self._build_label_area())
        layout.add_widget(self._build_image_area())

        self.temp_palette = BoxLayout()
        layout.add_widget(self.temp_palette)

        return layout

    def _build_image_area(self):
        self.image = BitmapImage(resizeable=True)

        self.image_wrapper = BoxLayout()
        self.image_wrapper.add_widget(self.image)

        return self.image_wrapper

    def _build_label_area(self):
        self.label_area = LabelArea({
            'name': 'Cast member name',
            'size': 'Image size',
            'bit_depth': 'Bit depth',
            'palette': 'Palette',
            'linked': 'Linked'
        })

        return self.label_area

    def load(self, file_disassembler: FileDisassembler, bitmap: BitmapCastMember):
        self.text_area.load(file_disassembler, bitmap)
        self._load_fields(bitmap)
        self._load_image(file_disassembler, bitmap)

    def _load_fields(self, bitmap: BitmapCastMember):
        self.label_area.load({
            'name': bitmap.name,
            'size': f'{bitmap.width}x{bitmap.height} px',
            'bit_depth': f'{bitmap.bit_depth}-bit',
            'palette': bitmap.palette_name,
            'linked': bitmap.external_file if bitmap.is_linked else 'False'
        })

    def _load_image(self, file_disassembler, bitmap_cast_member):
        resource = file_disassembler.get_mapped_data_chunk(bitmap_cast_member, 'BITD')

        self._detach_image()
        if not bitmap_cast_member.is_linked:
            image_data = bytes(flatten(bitmap_cast_member.image_data(resource)))

            if len(image_data) > 0:
                self._attach_image()
                self.image.display(
                    bitmap_cast_member.width,
                    bitmap_cast_member.height,
                    image_data,
                    color_format='argb'
                )

            self.temp_palette.clear_widgets()
            if bitmap_cast_member.bit_depth <= 8:
                self.temp_palette.add_widget(PaletteDisplay(bitmap_cast_member.palette))

    def _attach_image(self):
        self.image_wrapper.add_widget(self.image)

    def _detach_image(self):
        self.image_wrapper.clear_widgets()
