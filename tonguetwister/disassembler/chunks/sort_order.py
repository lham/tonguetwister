from collections import OrderedDict

from tonguetwister.disassembler.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class SortOrder(RecordsChunk):
    """
    This is an array of INT32s, each of which form the number property of a Cast Member.
    Each INT32 is really made up of two INT16s: the two most significant bytes of each
    INT32 represent the Cast’s index, and the two least significant represent the Cast
    Member’s index. The number property allows Director to match Cast Members to slots
    in the Cast window, regardless of where the Cast Member resources actually are in memory.

    This is where the minimum and maximum member number come in! Remember how the Cast’s
    index is represented by an INT16? This explains why the maximum number of Cast Members
    per Cast is 32000 — I’m certain it’s just 32768 rounded down. The minimum member number
    (minMember property) also shows something interesting about Director. For example, if
    the first ten members of a Cast are blank, Director can avoid having 10 null slots in
    the Cast Mapping Pointers where the empty Cast Members would be. Instead, Director actually
    treats the 11th member as the first one internally, and adds the minMember to it to pose
    the illusion to the author that it is the 11th.
    -- https://medium.com/@nosamu/a-tour-of-the-adobe-director-file-format-e375d1e063c0
    """

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['?n_record_slots_total'] = stream.uint32()
        header['?n_record_slots_used'] = stream.uint32()
        header['u3'] = stream.uint16()
        header['?record_length'] = stream.uint16()

        return header

    @classmethod
    def parse_records(cls, stream: ByteBlockIO, header):
        return [CastMemberEntry.parse(stream, header, i) for i in range(header['?n_record_slots_total'])]


class CastMemberEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['cast_lib'] = stream.uint16()
        data['cast_slot'] = stream.uint16()

        return data
