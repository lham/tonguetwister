from collections import OrderedDict

from tonguetwister.disassembler.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class LingoNamelist(RecordsChunk):
    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['chunk_length'] = stream.uint32()
        header['chunk_length_2'] = stream.uint32()
        header['header_length'] = stream.uint16()
        header['n_records'] = stream.uint16()

        return header

    @classmethod
    def parse_records(cls, stream: ByteBlockIO, header):
        return [NameEntry.parse(stream) for _ in range(header['n_records'])]

    def __getitem__(self, i):
        return self.records[i]._data['text']


class NameEntry(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['text_length'] = stream.uint8()
        data['text'] = stream.string_raw(data['text_length'])

        return data
