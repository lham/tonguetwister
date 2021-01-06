import logging
from collections import Sequence

from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper

logger = logging.getLogger('tonguetwister.disassembler.chunk')
logger.setLevel(logging.DEBUG)


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

        raise AttributeError(f'"{item}" not found in any of the public attrs')

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


class Chunk(ByteBlockParser):
    sections = ['data']
    public_data_attrs = []

    def __init__(self, address, four_cc, **sections):
        super().__init__(**sections)

        self.address = address
        self.four_cc = four_cc

    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        return cls(address, four_cc, **cls._parse_byte_block_stream(stream))


class EntryMapChunk(Chunk, Sequence):
    sections = ['header', 'entries']
    public_header_attrs = []

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, i):
        return self._entries[i]

    @property
    def entries(self):
        return self._entries


class InternalChunkEntry(ByteBlockParser):
    sections = ['data']
    public_data_attrs = []

    @classmethod
    def parse(cls, stream: ByteBlockIO, *args, **kwargs):
        return cls(**cls._parse_byte_block_stream(stream, *args, **kwargs))


class UndefinedChunk(Chunk):
    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        logger.warning(f'Chunk parser not implemented for [{four_cc}]')

        return super().parse(stream, stream, address)

    @staticmethod
    def parse_data(stream: ByteBlockIO):
        data = {}
        data['all_str'] = stream.read_bytes()
        data['all_hex'] = grouper(data['all_str'], 4)

        return data
