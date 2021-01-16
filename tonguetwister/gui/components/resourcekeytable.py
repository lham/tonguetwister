from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.chunkview import ResourceLink
from tonguetwister.gui.widgets.entrylistview import EntryListView, EntryView


class ResourceKeyTableEntryView(EntryView):
    rows = 1
    cols = 3
    col_sizes = [130, 20, 300]

    def __init__(self, index, entry, **kwargs):
        self.chunk_type = ChunkType(entry.child_four_cc)
        super().__init__(index, entry, **kwargs)

    def entry_kwarg_list(self):
        return [
            {'text': f'([{self.entry.parent_resource_id:4d}], {self.chunk_type})', 'halign': 'right'},
            {'text': '->', 'halign': 'center'},
            {
                'text': f'[{self.entry.child_resource_id:4d}]: {self.chunk_type.name}',
                'link_target': self.set_resource_link
            }
        ]

    def set_resource_link(self):
        self.resource_link = ResourceLink(self.entry.parent_resource_id, self.chunk_type)


class ResourceKeyTableView(EntryListView):
    entry_class = ResourceKeyTableEntryView
