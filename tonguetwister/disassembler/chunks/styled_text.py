from tonguetwister.disassembler.chunk import EntryMapChunkParser, InternalChunkEntryParser
from tonguetwister.lib.byte_block_io import ByteBlockIO


class StyledText(EntryMapChunkParser):
    section = ['header', 'body', 'records']

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['header_length'] = stream.uint32()
        header['text_length'] = stream.uint32()
        header['style_length'] = stream.uint32()

        return header

    @classmethod
    def parse_body(cls, stream: ByteBlockIO, header):
        body = {}
        body['text'] = stream.string_raw(header['text_length'])

        return body

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        n_styles = stream.uint16()
        return [TextStyle.parse(stream) for _ in range(n_styles)]


class TextStyle(InternalChunkEntryParser):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['u0'] = stream.uint16()
        data['offset'] = stream.uint32()
        data['u1'] = stream.uint16()
        data['u2'] = stream.uint16()
        data['u3'] = stream.uint32()
        r = stream.uint16()
        g = stream.uint16()
        b = stream.uint16()
        data['rgb'] = (r, g, b)

        return data

    @property
    def rgb(self):
        return self.data['rgb']
