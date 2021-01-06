import logging
from collections import Sequence

from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper

logger = logging.getLogger('tonguetwister.disassembler.chunk')
logger.setLevel(logging.DEBUG)


class Chunk:
    endianess = ByteBlockIO.BIG_ENDIAN

    sections = ['data']
    _data: dict

    def __init__(self, address, four_cc, **sections):
        self.address = address
        self.four_cc = four_cc

        for name, values in sections.items():
            setattr(self, f'_{name}', values)

    @classmethod
    def parse(cls, stream: ByteBlockIO, address, four_cc):
        stream.set_endianess(cls.endianess)

        parsed = {}
        for section in cls.sections:
            parsed[section] = cls._parse_section(stream, section, parsed)

        return cls(address, four_cc, **parsed)

    @classmethod
    def _parse_section(cls, stream, section, parsed_sections):
        section_function_name = f'parse_{section}'

        if not hasattr(cls, section_function_name):
            raise RuntimeError(f'Chunk {cls.__name__} must define section parser named {section_function_name}')
        else:
            return getattr(cls, section_function_name)(stream, **parsed_sections)

    @classmethod
    def _update_endianess(cls, stream: ByteBlockIO):
        stream.set_endianess(cls.endianess)


class RecordsChunk(Chunk, Sequence):
    sections = ['header', 'records']
    _header: dict
    _records: dict

    def __len__(self):
        return len(self._records)

    def __getitem__(self, i):
        return self._records[i]


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
        logger.warning(f'Chunk parser not implemented for [{four_cc}]')

        return super().parse(stream, stream, address)

    @staticmethod
    def parse_data(stream: ByteBlockIO):
        data = {}
        data['all_str'] = stream.read_bytes()
        data['all_hex'] = grouper(data['all_str'], 4)

        return data
