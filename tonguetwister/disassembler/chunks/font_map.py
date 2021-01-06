from collections import OrderedDict

from tonguetwister.disassembler.chunk import RecordsChunk, InternalChunkRecord
from tonguetwister.lib.byte_block_io import ByteBlockIO


class FontMap(RecordsChunk):
    @classmethod
    def parse_header(cls, stream):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['records_length'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['u3'] = stream.uint32()
        header['n_font_records'] = stream.uint32()
        header['n_font_headers'] = stream.uint32()
        header['u4'] = stream.uint16()
        header['u5'] = stream.uint16()
        header['u6'] = stream.uint32()
        header['u7'] = stream.uint32()

        header['record_headers'] = record_headers = []
        for i in range(header['n_font_headers']):
            record_headers.append(OrderedDict())
            record_headers[i]['offset'] = stream.uint32()
            record_headers[i]['u1'] = stream.uint16()
            record_headers[i]['u2'] = stream.uint16()

        header['font_data'] = font_data = OrderedDict()
        font_data['u8'] = stream.uint32()
        font_data['u9'] = stream.uint32()
        font_data['font_data_length'] = stream.uint32()
        font_data['total_body_length'] = stream.uint32()
        font_data['offset_to_fonts'] = stream.uint16()

        return header

    @classmethod
    def parse_records(cls, stream: ByteBlockIO, header):
        offset = 60
        #records = [FontEntry.parse(stream, header, i) for i in range(header['n_font_records'])]
        #stream.seek(offset + header['font_data']['font_data_length'])

        records = []  # TODO: Figure this out!
        stream.read_bytes()  # Rest is unknown

        return records


class FontEntry(InternalChunkRecord):
    # noinspection PyTypeChecker
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['header'] = parent_header['record_headers'][index]

        if data['header']['offset'] >> 31 != 1:
            stream.seek(60 + data['header']['offset'])
            data['name_length'] = stream.uint32()
            data['name'] = stream.string_raw(data['name_length'])
            stream.read_pad(4 - ((4 + data['name_length']) % 4))  # 4-byte aligned padding
        else:
            data['name_length'] = 0
            data['name'] = '__UNDEFINED__'

        return data
