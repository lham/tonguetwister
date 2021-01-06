from collections import Sequence, OrderedDict

from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper


class Chunk:
    def __init__(self, address, four_cc, header, body, footer):
        self.address = address
        self.four_cc = four_cc
        self.header = header
        self.body = body
        self.footer = footer
        self.resource_id = None

    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        cls._set_big_endianess(stream)

        header = cls._parse_header(stream)
        body = cls._parse_body(stream, header)
        footer = cls._parse_footer(stream, header)

        return cls(address, four_cc, header, body, footer)

    @classmethod
    def _set_big_endianess(cls, stream: ByteBlockIO):
        stream.set_big_endian()

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        return OrderedDict()

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def _parse_footer(cls, steam: ByteBlockIO, header):
        return None


class RecordsChunk(Chunk, Sequence):
    def __init__(self, address, four_cc, header, body, records, footer):
        super().__init__(address, four_cc, header, body, footer)
        self.records = records

    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        cls._set_big_endianess(stream)

        header = cls._parse_header(stream)
        body = cls._parse_body(stream, header)
        records = cls._parse_records(stream, header)
        footer = cls._parse_footer(stream, header)

        return cls(address, four_cc, header, body, records, footer)

    @classmethod
    def _parse_records(cls, stream: ByteBlockIO, header):
        return None

    def __len__(self):
        return len(self.records)

    def __getitem__(self, i):
        return self.records[i]


class InternalChunkRecord:
    def __init__(self, data):
        self.data = data

    @classmethod
    def parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = cls._parse(stream, parent_header, index)

        return cls(data)

    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        return None


class UndefinedChunk(Chunk):
    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        print(f'Warning: Chunk parser for {four_cc} is not implemented')

        data = OrderedDict()
        data['all_str'] = stream.read_bytes()
        data['all_hex'] = grouper(data['all_str'], 4)

        return cls(address, four_cc, data, None, None)
