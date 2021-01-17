from tonguetwister.disassembler.chunks.thumbnail import Thumbnail
from tonguetwister.gui.chunkviews.bitmapcastmember import BitmapCastMemberView
from tonguetwister.gui.widgets.labelcollection import LabelCollection
from tonguetwister.lib.helper import flatten


class ThumbnailView(BitmapCastMemberView):
    def build_labels(self):
        self.labels = LabelCollection(col_widths=[100], labels=[
            {'key': 'size', 'title': 'Image size'},
        ])

        return self.labels

    def load_labels(self, thumbnail: Thumbnail):
        self.labels.load({
            'size': f'{thumbnail.width}x{thumbnail.height} px',
        })

    def load_image(self, _, thumbnail):
        self.image.display(
            thumbnail.width,
            thumbnail.height,
            bytes(flatten(thumbnail.image_data())),
            color_format='argb'
        )

    def load_palette(self, thumbnail):
        pass
