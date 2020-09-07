from collections import Sequence, OrderedDict

from tonguetwister.lib.byte_block_io import ByteBlockIO


# noinspection PyNoneFunctionAssignment
class Chunk:
    def __init__(self, header, body, footer):
        self.header = header
        self.body = body
        self.footer = footer

    @classmethod
    def parse(cls, stream: ByteBlockIO):
        cls._set_endianess(stream)

        header = cls._parse_header(stream)
        body = cls._parse_body(stream, header)
        footer = cls._parse_footer(stream, header)

        return cls(header, body, footer)

    @classmethod
    def _set_endianess(cls, stream: ByteBlockIO):
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


# noinspection PyNoneFunctionAssignment
class RecordsChunk(Chunk, Sequence):
    def __init__(self, header, body, records, footer):
        super().__init__(header, body, footer)
        self.records = records

    @classmethod
    def parse(cls, stream: ByteBlockIO):
        cls._set_endianess(stream)

        header = cls._parse_header(stream)
        body = cls._parse_body(stream, header)
        records = cls._parse_records(stream, header)
        footer = cls._parse_footer(stream, header)

        return cls(header, body, records, footer)

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
