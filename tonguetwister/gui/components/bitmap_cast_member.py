from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from tonguetwister.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.gui.components.chunk import DefaultChunkView
from tonguetwister.gui.widgets.bitmap_image import BitmapImage
from tonguetwister.gui.widgets.label_area import LabelArea
from tonguetwister.gui.widgets.palette import PaletteDisplay


class BitmapCastMemberView(BoxLayout):
    def __init__(self, file_disassembler, font_name, **kwargs):
        super().__init__(**kwargs)
        self.file_disassembler = file_disassembler
        self.font_name = font_name

        self.label_area = None
        self.image = None
        self.temp_palette = None

        self.add_widget(self._build_tabbed_panel())

    def _build_tabbed_panel(self):
        self.text_area = DefaultChunkView(self.file_disassembler, font_name=self.font_name)
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
        self.image = BitmapImage()

        layout = BoxLayout()
        layout.add_widget(self.image)

        return layout

    def _build_label_area(self):
        self.label_area = LabelArea({
            'name': 'Cast member name',
            'size': 'Image size',
            'bit_depth': 'Bit depth',
            'palette': 'Palette'
        })

        return self.label_area

    def load(self, bitmap: BitmapCastMember):
        self.text_area.load(bitmap)
        self._load_fields(bitmap)
        self._load_image(bitmap)

    def _load_fields(self, bitmap: BitmapCastMember):
        self.label_area.load({
            'name': bitmap.name,
            'size': f'{bitmap.width}x{bitmap.height} px',
            'bit_depth': f'{bitmap.bit_depth}-bit',
            'palette': bitmap.palette_name
        })

    def _load_image(self, bitmap_cast_member):
        mmap = self.file_disassembler.mmap
        key_map = self.file_disassembler.cast_key_map

        cast_id = mmap.find_record_id_by_address(bitmap_cast_member.address)
        resource_id = key_map.find_resource_chunk_mmap_id_by_cast_member_mmap_id(cast_id)
        resource = self.file_disassembler.find_chunk_by_mmap_id(resource_id)
        self.image.display(
            bitmap_cast_member.width,
            bitmap_cast_member.height,
            bitmap_cast_member.image_data(resource)
        )

        self.temp_palette.clear_widgets()
        self.temp_palette.add_widget(PaletteDisplay(bitmap_cast_member.palette))
