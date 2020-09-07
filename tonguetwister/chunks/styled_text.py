from collections import OrderedDict

from tonguetwister.chunks.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class StyledText(RecordsChunk):

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['header_length'] = stream.uint32()
        header['text_length'] = stream.uint32()
        header['style_length'] = stream.uint32()

        return header

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        body = OrderedDict()
        body['text'] = stream.string(header['text_length'])

        return body

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        n_styles = stream.uint16()
        return [TextStyle.parse(stream, header, i) for i in range(n_styles)]


class TextStyle(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
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
