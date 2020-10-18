from tonguetwister.chunks.thumbnail import Thumbnail
from tonguetwister.gui.components.bitmap_cast_member import BitmapCastMemberView
from tonguetwister.gui.widgets.label_area import LabelArea
from tonguetwister.lib.helper import flatten


class ThumbnailView(BitmapCastMemberView):
    def __init__(self, file_disassembler, font_name, **kwargs):
        super().__init__(file_disassembler, font_name, **kwargs)

    def _build_label_area(self):
        self.label_area = LabelArea({
            'size': 'Image size',
        })

        return self.label_area

    def load(self, bitmap: Thumbnail):
        self.text_area.load(bitmap)
        self._load_fields(bitmap)
        self._load_image(bitmap)

    def _load_fields(self, thumbnail: Thumbnail):
        self.label_area.load({
            'size': f'{thumbnail.width}x{thumbnail.height} px',
        })

    def _load_image(self, thumbnail):
        self.image.display(
            thumbnail.width,
            thumbnail.height,
            bytes(flatten(thumbnail.image_data())),
            color_format='argb'
        )
