from collections import Sequence

from tonguetwister.lib.stream import ByteBlockIO
from tonguetwister.lib.helper import grouper


class ByteBlockParser:
    endianess = ByteBlockIO.BIG_ENDIAN
    sections = []

    def __init__(self, **sections):
        for name, values in sections.items():
            setattr(self, f'_{name}', values)

    def __getattr__(self, item):
        for name in self.sections:
            if item in getattr(self, f'public_{name}_attrs', []):
                return getattr(self, f'_{name}')[item]

        return self.__getattribute__(item)

    @classmethod
    def _parse_byte_block_stream(cls, stream: ByteBlockIO, *args, **kwargs):
        stream.set_endianess(cls.endianess)

        parsed = {}
        for section in cls.sections:
            parsed[section] = cls._parse_section(stream, section, parsed, *args, **kwargs)

        return parsed

    @classmethod
    def _parse_section(cls, stream, section, parsed, *args, **kwargs):
        section_function_name = f'parse_{section}'

        if not hasattr(cls, section_function_name):
            raise RuntimeError(f'Chunk {cls.__name__} must define section parser named {section_function_name}')
        else:
            return getattr(cls, section_function_name)(stream, *args, **{**kwargs, **parsed})


class ChunkParser(ByteBlockParser):
    sections = ['data']
    public_data_attrs = []

    def __init__(self, **sections):
        super().__init__(**sections)
        self.resource = None

    @classmethod
    def parse(cls, stream: ByteBlockIO):
        return cls(**cls._parse_byte_block_stream(stream))


class EntryMapChunkParser(ChunkParser, Sequence):
    sections = ['header', 'entries']
    public_header_attrs = []

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, i):
        return self._entries[i]

    @property
    def entries(self):
        return self._entries


class InternalChunkEntryParser(ByteBlockParser):
    sections = ['data']
    public_data_attrs = []

    @classmethod
    def parse(cls, stream: ByteBlockIO, *args, **kwargs):
        return cls(**cls._parse_byte_block_stream(stream, *args, **kwargs))


class UnknownChunkParser(ChunkParser):
    @staticmethod
    def parse_data(stream: ByteBlockIO):
        data = {}
        data['all_str'] = stream.read_bytes()
        data['all_hex'] = grouper(data['all_str'], 4)

        return data
