from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class LingoNamelist(EntryMapChunkParser):
    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['chunk_length'] = stream.uint32()
        header['chunk_length_2'] = stream.uint32()
        header['header_length'] = stream.uint16()
        header['n_records'] = stream.uint16()

        return header

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        return [NameEntry.parse(stream) for _ in range(header['n_records'])]

    def __getitem__(self, i):
        return self.records[i].text


class NameEntry(InternalEntryParser):
    public_data_attrs = ['text']

    @classmethod
    def _parse(cls, stream: ByteBlockIO):
        data = {}
        data['text_length'] = stream.uint8()
        data['text'] = stream.string_raw(data['text_length'])

        return data
