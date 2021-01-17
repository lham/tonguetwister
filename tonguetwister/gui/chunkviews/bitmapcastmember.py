from tonguetwister.disassembler.chunks.castmembers.bitmap import BitmapCastMember
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.chunkview import ChunkView
from tonguetwister.gui.widgets.bitmap_image import BitmapImage
from tonguetwister.gui.widgets.generic.layouts import VerticalStackLayout
from tonguetwister.gui.widgets.labelcollection import LabelCollection
from tonguetwister.gui.widgets.palette import PaletteDisplay
from tonguetwister.lib.helper import flatten


class BitmapCastMemberView(ChunkView):
    def __init__(self, *args, **kwargs):
        self.labels = None
        self.image = None
        self.image_wrapper = None
        self.palette = None
        super().__init__(*args, **kwargs)

    def tabs(self):
        return [
            ('Reconstructed', self.build_reconstructed_view),
        ]

    def build_reconstructed_view(self):
        layout = VerticalStackLayout(spacing=(0, 10))
        layout.add_widget(self.build_labels())
        layout.add_widget(self.build_image())
        layout.add_widget(self.build_palette())

        return layout

    def build_image(self):
        self.image = BitmapImage(resizeable=True)
        self.image_wrapper = VerticalStackLayout()
        self.image_wrapper.add_widget(self.image)

        return self.image_wrapper

    def build_labels(self):
        self.labels = LabelCollection(rows=3, cols=2, col_widths=[(140, 100), 100], labels=[
            {'key': 'name', 'title': 'Cast member name'},
            {'key': 'bit_depth', 'title': 'Bit depth'},

            {'key': 'size', 'title': 'Image size'},
            {'key': 'palette', 'title': 'Palette'},

            {'key': 'linked', 'title': 'Linked'},
            {}
        ])

        return self.labels

    def build_palette(self):
        self.palette = VerticalStackLayout()

        return self.palette

    def load(self, disassembler: FileDisassembler, bitmap: BitmapCastMember):
        super().load(disassembler, bitmap)
        self.load_labels(bitmap)
        self.load_image(disassembler, bitmap)
        self.load_palette(bitmap)

    def load_labels(self, bitmap: BitmapCastMember):
        self.labels.load({
            'name': bitmap.name,
            'size': f'{bitmap.width}x{bitmap.height} px',
            'bit_depth': f'{bitmap.bit_depth}-bit',
            'palette': bitmap.palette_name,
            'linked': bitmap.external_file if bitmap.is_linked else 'False'
        })

    def load_image(self, disassembler, bitmap):
        self.image_wrapper.clear_widgets()
        if bitmap.is_linked:
            return

        image_data_chunk = disassembler.get_linked_resource(bitmap, ChunkType.BitmapData)
        image_data = bytes(flatten(bitmap.image_data(image_data_chunk)))

        if len(image_data) > 0:
            self.image.display(bitmap.width, bitmap.height, image_data, color_format='argb')
            self.image_wrapper.add_widget(self.image)

    def load_palette(self, bitmap):
        self.palette.clear_widgets()
        if bitmap.is_linked:
            return

        if bitmap.bit_depth <= 8:
            self.palette.add_widget(PaletteDisplay(bitmap.palette))
