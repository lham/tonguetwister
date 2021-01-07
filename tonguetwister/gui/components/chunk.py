import os

from kivy.uix.textinput import TextInput

from tonguetwister.file_disassembler import FileDisassembler
from tonguetwister.gui.utils import scroll_to_top
from tonguetwister.lib.helper import splat_ordered_dict


class DefaultChunkView(TextInput):
    key_width = 40
    number_width = 6
    indent = '    '
    separator = f'{os.linesep}{indent}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readonly = True

    def load(self, file_disassembler: FileDisassembler, chunk):
        text = f'Chunk type: {chunk.__class__.__name__} (FOUR CC: {chunk.resource.chunk_type})'

        for name in chunk.sections:
            text += self._section_string(name.capitalize())
            text += self._format_value(getattr(chunk, f'_{name}'))

        self.text = text
        scroll_to_top(self)

    @staticmethod
    def _section_string(title):
        return os.linesep.join([
            os.linesep,
            '============================',
            str(title),
            '============================',
            os.linesep
        ])

    def _format_value(self, value, depth=1):
        lines = []
        indent = self.indent * depth

        if value is None:
            lines.append(indent + 'None')
        elif isinstance(value, dict):
            for key, _value in value.items():
                lines.append(f'{indent}{str(key):.<{self.key_width}s}: {self._value_to_line(_value, depth)}')
        elif isinstance(value, (list, tuple)):
            for i, _value in enumerate(value):
                lines.append(f'{indent}[{i}]: {self._value_to_line(_value, depth, True)}')
        else:
            print(f'WARNING: Not displaying chunk data due to bad type: {type(value)}')

        return os.linesep.join(lines)

    def _value_to_line(self, value, depth, from_list=False):
        if isinstance(value, (dict, list, tuple)) and len(value) == 0:
            return ''
        if isinstance(value, (dict, list, tuple)):
            return os.linesep + self._format_value(value, depth + 1)
        elif isinstance(value, int) and from_list:
            return f'{"." * self.key_width}: {value:{self.number_width}d} (0x{value:08x})'
        elif isinstance(value, int):
            return f'{value:{self.number_width}d} (0x{value:08x})'
        elif from_list:
            return f'{"." * self.key_width}: {value}'
        else:
            return value


class DefaultRecordsChunkView(DefaultChunkView):
    def load(self, file_disassembler: FileDisassembler, chunk):
        text = f'Chunk type: {chunk.__class__.__name__} (FOUR CC: {chunk.resource.chunk_type})'

        for name in chunk.sections:
            text += self._section_string(name.capitalize())
            if name == 'entries':
                text += self._display_records(getattr(chunk, f'_{name}'))
            else:
                text += self._format_value(getattr(chunk, f'_{name}'))

        self.text = text
        scroll_to_top(self)

    def _display_records(self, records, depth=0):
        return ((depth + 1) * self.indent) \
               + self.separator.join([self._display_record(r, depth + 1, i) for i, r in enumerate(records)])

    def _display_record(self, record, depth, index):
        sub_indent = (depth + 3) * self.indent
        separator = f'{os.linesep}{sub_indent}'

        return (
            f'{depth * self.indent}[{index:3d}] {record.__class__.__name__}: \n'
            f'{sub_indent}{splat_ordered_dict(record._data, separator, self.key_width)}'
        )
