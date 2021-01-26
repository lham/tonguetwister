from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.gui.chunkview import ResourceLink
from tonguetwister.gui.widgets.entrylistview import EntryListView, EntryView


class SortOrderEntryView(EntryView):
    rows = 1
    cols = 3
    col_widths = [230, 20, 210]

    def __init__(self, index, entry, disassembler):
        self.disassembler = disassembler
        super().__init__(index, entry)

    def label_kwargs(self):
        return [
            {'text': f'CastMember reference id {self.index:4d}', 'halign': 'right'},
            {'text': '->', 'halign': 'center'},
            {
                'text': f'Cast no. {self.entry.cast_number:2d}, slot no. {self.entry.cast_member_slot_number:3d}',
                'link_target': self.set_resource_link
            }
        ]

    def set_resource_link(self):
        all_casts = self.disassembler.lookup_movie_resource(ChunkType.MovieCastLibraries)
        cast = all_casts[self.entry.cast_number - 1]
        cast_member_entry_index = self.entry.cast_member_slot_number - cast.cast_member_id_first

        cast_assoc = self.disassembler.get_linked_resource_by_id(cast.cast_resource_id, ChunkType.CastAssocTable)
        cast_assoc_entry = cast_assoc[cast_member_entry_index]

        self.resource_link = ResourceLink(cast_assoc_entry.resource_id)


class SortOrderView(EntryListView):
    def create_entry_view(self, index, entry):
        return SortOrderEntryView(index, entry, self.disassembler)
