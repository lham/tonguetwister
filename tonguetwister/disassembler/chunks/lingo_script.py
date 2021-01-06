from collections import OrderedDict

from tonguetwister.disassembler.chunk import InternalChunkRecord, RecordsChunk
from tonguetwister.lib.byte_block_io import ByteBlockIO


class LingoScript(RecordsChunk):
    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['chunk_length'] = stream.uint32()
        header['chunk_length_2'] = stream.uint32()
        header['chunk_header_length'] = stream.uint16()
        header['script_id'] = stream.uint16()
        header['u3'] = stream.uint16()
        header['u4'] = stream.uint32()
        header['u5'] = stream.uint32()
        header['u6'] = stream.uint32()
        header['u7'] = stream.uint32()
        header['u8'] = stream.uint32()
        header['u10'] = stream.uint32()
        header['cast_member_assoc_id'] = stream.uint16()
        header['u11'] = stream.uint16()
        header['n_u9'] = stream.uint16()
        header['u9_offset'] = stream.uint32()
        header['u12'] = stream.uint32()
        header['n_properties'] = stream.uint16()
        header['properties_offset'] = stream.uint32()
        header['n_globals'] = stream.uint16()
        header['globals_offset'] = stream.uint32()
        header['n_functions'] = stream.uint16()
        header['function_headers_offset'] = stream.uint32()
        header['n_literals'] = stream.uint16()
        header['literal_headers_offset'] = stream.uint32()
        header['literals_body_length'] = stream.uint32()
        header['literals_body_offset'] = stream.uint32()

        return header

    @classmethod
    def parse_records(cls, stream: ByteBlockIO, header):
        records = []

        stream.seek(header['properties_offset'], 0)
        records.extend([LingoProperty.parse(stream, header, i) for i in range(header['n_properties'])])
        stream.seek(header['globals_offset'], 0)
        records.extend([LingoGlobal.parse(stream, header, i) for i in range(header['n_globals'])])
        records.extend([LingoFunction.parse(stream, header, i) for i in range(header['n_functions'])])
        records.extend([LingoLiteral.parse(stream, header, i) for i in range(header['n_literals'])])
        stream.seek(header['u9_offset'], 0)
        records.extend([LingoU9.parse(stream, header, i) for i in range(header['n_u9'])])

        return records

    @property
    def properties(self):
        return [record for record in self.records if isinstance(record, LingoProperty)]

    @property
    def globals(self):
        return [record for record in self.records if isinstance(record, LingoGlobal)]

    @property
    def functions(self):
        return [record for record in self.records if isinstance(record, LingoFunction)]

    @property
    def literals(self):
        return [record for record in self.records if isinstance(record, LingoLiteral)]

    @property
    def u9(self):
        return [record for record in self.records if isinstance(record, LingoU9)]


class LingoProperty(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['value'] = stream.uint16()

        return data


class LingoGlobal(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['value'] = stream.uint16()

        return data


class LingoFunction(InternalChunkRecord):
    header_length = 42

    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        offset = parent_header['function_headers_offset'] + index * cls.header_length

        data = OrderedDict()
        data['header'] = header = cls._parse_header(stream, offset)
        data['bytecode'] = cls._parse_bytecode(stream, header['record_offset'], header['record_length'])
        data['args'] = cls._parse_args(stream, header['args_offset'], header['n_args'])
        data['locals'] = cls._parse_locals(stream, header['locals_offset'], header['n_locals'])
        data['u3'] = cls._parse_u3(stream, header['u3_offset'], header['n_u3'])
        data['u7'] = cls._parse_u7(stream, header['u7_offset'], header['n_u7'])

        return data

    @classmethod
    def _parse_header(cls, stream, offset):
        stream.seek(offset, 0)
        header = OrderedDict()
        header['function_id'] = stream.uint16()
        header['u2'] = stream.uint16()
        header['record_length'] = stream.uint32()
        header['record_offset'] = stream.uint32()
        header['n_args'] = stream.uint16()
        header['args_offset'] = stream.uint32()
        header['n_locals'] = stream.uint16()
        header['locals_offset'] = stream.uint32()
        header['n_u3'] = stream.uint16()
        header['u3_offset'] = stream.uint32()
        header['u4'] = stream.uint16()
        header['u5'] = stream.uint16()
        header['u6'] = stream.uint16()
        header['n_u7'] = stream.uint16()
        header['u7_offset'] = stream.uint32()

        return header

    @classmethod
    def _parse_bytecode(cls, stream, offset, length):
        stream.seek(offset, 0)
        bytecode = stream.read_bytes(length)
        stream.read_pad(length % 2)
        return bytecode

    @classmethod
    def _parse_args(cls, stream, offset, n_args):
        stream.seek(offset, 0)
        return [stream.uint16() for _ in range(n_args)]

    @classmethod
    def _parse_locals(cls, stream, offset, n_locals):
        stream.seek(offset, 0)
        return [stream.uint16() for _ in range(n_locals)]

    @classmethod
    def _parse_u3(cls, stream, offset, n_u3):
        stream.seek(offset, 0)
        return [stream.uint16() for _ in range(n_u3)]

    @classmethod
    def _parse_u7(cls, stream, offset, n_u7):
        stream.seek(offset, 0)
        data = [stream.uint8() for _ in range(n_u7)]
        stream.read_pad(n_u7 % 2)
        return data

    @property
    def header(self):
        return self.data['header']

    @property
    def bytecode(self):
        return self.data['bytecode']

    @property
    def args(self):
        return self.data['args']

    @property
    def locals(self):
        return self.data['locals']

    @property
    def u3(self):
        return self.data['u3']

    @property
    def u7(self):
        return self.data['u7']

    @property
    def name_id(self):
        return self.header['function_id']


class LingoLiteral(InternalChunkRecord):
    TYPE_STRING = 1
    TYPE_INT = 4
    TYPE_DOUBLE = 9
    TYPES = ('', 'string', '', '', 'int', '', '', '', '', 'double')

    header_length = 8

    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        offset = parent_header['literal_headers_offset'] + index * cls.header_length

        data = OrderedDict()
        data['header'] = header = cls._parse_header(stream, offset)
        data['value'], data['length'] = cls._parse_body(stream, parent_header['literals_body_offset'], header)

        return data

    @classmethod
    def _parse_header(cls, stream, offset):
        stream.seek(offset, 0)
        header = OrderedDict()
        header['type'] = stream.uint32()
        header['offset'] = stream.uint32()

        return header

    @classmethod
    def _parse_body(cls, stream, offset, header):
        _type = header['type']

        if cls.TYPES[_type] == 'string':
            return cls._parse_string(stream, offset, header)
        elif cls.TYPES[_type] == 'int':
            return cls._parse_int(stream, offset, header)
        elif cls.TYPES[_type] == 'double':
            return cls._parse_double(stream, offset, header)
        else:
            raise RuntimeError(f'Literal type {_type} not implemented')

    @classmethod
    def _parse_string(cls, stream, offset, header):
        stream.seek(offset + header['offset'])

        length = stream.uint32()
        value = stream.string_raw(length - 1)  # No need to read null terminating byte in python
        stream.read_bytes(1)  # Clear the null terminating byte
        stream.read_pad(length % 2)

        return value, length

    @classmethod
    def _parse_int(cls, _, __, header):
        return header['offset'], 4

    @classmethod
    def _parse_double(cls, stream, offset, header):
        stream.seek(offset + header['offset'])
        length = stream.uint32()
        value = stream.double() if (length == 8) else stream.float()

        return value, length

    @property
    def type(self):
        return self.data['header']['type']

    @property
    def value(self):
        return self.data['value']


class LingoU9(InternalChunkRecord):
    @classmethod
    def _parse(cls, stream: ByteBlockIO, parent_header=None, index=None):
        data = OrderedDict()
        data['value'] = stream.uint16()

        return data
