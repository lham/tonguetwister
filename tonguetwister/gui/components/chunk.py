import os
from collections import OrderedDict

from kivy.uix.textinput import TextInput

from tonguetwister.gui.utils import scroll_to_top
from tonguetwister.lib.helper import splat_ordered_dict, splat_list


class DefaultChunkView(TextInput):
    key_width = 25
    indent = '    '
    separator = f'{os.linesep}{indent}'

    def __init__(self, parser_results, **kwargs):
        super().__init__(**kwargs)
        self.parser_results = parser_results

    def load(self, chunk):
        self.text = (
            f'Chunk type: {chunk.__class__.__name__}'
            + self._section_string('Header')
            + self._splat_dict(chunk.header)
            + self._section_string('Body')
            + self._splat_dict(chunk.body)
            + self._section_string('Footer')
            + self._splat_dict(chunk.footer)
        )
        scroll_to_top(self)

    @staticmethod
    def _section_string(title):
        return (
            f'\n\n'
            f'============================\n'
            f'{title}:\n'
            f'============================\n\n'
        )

    def _splat_dict(self, d):
        if d is None or len(d) == 0:
            return f'{self.indent}None'

        if isinstance(d, OrderedDict):
            return self.indent + splat_ordered_dict(d, self.separator, self.key_width)
        elif isinstance(d, (list, tuple)):
            return self.indent + splat_list(d, self.separator, self.key_width)


class DefaultRecordsChunkView(DefaultChunkView):
    def load(self, chunk):
        self.text = (
            f'Chunk type: {chunk.__class__.__name__}'
            + self._section_string('Header')
            + self._splat_dict(chunk.header)
            + self._section_string('Body')
            + self._splat_dict(chunk.body)
            + self._section_string('Records')
            + self._display_records(chunk.records)
            + self._section_string('Footer')
            + self._splat_dict(chunk.footer)
        )
        scroll_to_top(self)

    def _display_records(self, records, depth=0):
        return ((depth + 1) * self.indent) \
               + self.separator.join([self._display_record(r, depth + 1, i) for i, r in enumerate(records)])

    def _display_record(self, record, depth, index):
        return (
            f'{depth * self.indent}[{index:3d}] {record.__class__.__name__}: '
            f'{{{splat_ordered_dict(record.data)}}}'
        )
