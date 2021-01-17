from tonguetwister.disassembler.chunks.font_xtra_map import FontXtraMap
from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunkview import ChunkView
from tonguetwister.gui.widgets.generic.texts import MonoReadOnlyTextInput


class FontXtraMapView(ChunkView):

    def __init__(self, **kwargs):
        self.text_area = None
        super().__init__(**kwargs)

    def tabs(self):
        return [
            ('Reconstructed', self.build_reconstructed_view),
        ]

    def build_reconstructed_view(self):
        self.text_area = MonoReadOnlyTextInput()

        return self.text_area

    def load(self, disassembler: FileDisassembler, chunk: FontXtraMap):
        super().load(disassembler, chunk)
        self.text_area.text = chunk.font_map
        self.text_area.scroll_to_top()
