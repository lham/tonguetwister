from typing import Optional

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.chunkview import ChunkView, ResourceLink
from tonguetwister.gui.widgets.generic.labels import FixedSizeLabel, FixedSizeLinkLabel
from tonguetwister.gui.widgets.generic.layouts import VerticalStackLayout, SideScrollView
from tonguetwister.gui.widgets.generic.props import FixedSize


class EntryView(GridLayout, FixedSize):
    label_class = FixedSizeLabel
    link_label_class = FixedSizeLinkLabel

    resource_link = ObjectProperty(None, allownone=True)

    spacing = (10, 0)
    rows = 1
    cols = 1
    col_widths = [300]
    row_height = 20

    def __init__(self, index, entry, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.entry = entry

        self.build()

    def build(self):
        if self.rows == 1:
            self.build_row(self.label_kwargs())
        else:
            for row in self.label_kwargs():
                self.build_row(row)

    def build_row(self, label_kwarg_list):
        for label_kwargs in label_kwarg_list:
            self.add_label(**label_kwargs)

    def label_kwargs(self):
        return [
            {'text': str(self.entry)}
        ]

    def add_label(self, text='', link_target=None, **kwargs):
        width = self.col_widths[len(self.children) % len(self.col_widths)]

        if link_target is not None:
            label = self.link_label_class(text, width, self.row_height, link_target=link_target, **kwargs)
        else:
            label = self.label_class(text, width, self.row_height, **kwargs)

        self.add_widget(label)


class EntryListView(ChunkView):
    entry_class = EntryView

    def __init__(self, *args, **kwargs):
        self.reconstructed_layout = None
        super().__init__(*args, **kwargs)

    def tabs(self):
        return [
            ('Reconstructed', self.build_reconstructed_view),
        ]

    def build_reconstructed_view(self):
        self.reconstructed_layout = self.build_reconstructed_view_layout()

        scroll_view = SideScrollView()
        scroll_view.add_widget(self.reconstructed_layout)

        return scroll_view

    # noinspection PyMethodMayBeStatic
    def build_reconstructed_view_layout(self):
        return VerticalStackLayout()

    def load(self, disassembler: FileDisassembler, chunk):
        super().load(disassembler, chunk)
        self.load_entries_view(self.reconstructed_layout, self.create_entry_view, chunk)

    def load_entries_view(self, layout, create_entry_view, chunk):
        layout.clear_widgets()

        for index, entry in enumerate(chunk.entries):
            widget = create_entry_view(index, entry)
            widget.bind(resource_link=self.on_child_resource_link)

            layout.add_widget(widget)

    def create_entry_view(self, index, entry):
        return self.entry_class(index, entry)

    def on_child_resource_link(self, widget: entry_class, resource_link: Optional[ResourceLink]):
        if resource_link is None:
            return
        widget.resource_link = None

        self.resource_link = resource_link
