import logging
import os

from tonguetwister.disassembler.chunkparser import ChunkParser, InternalEntryParser
from tonguetwister.disassembler.resources import ChunkResource
from tonguetwister.gui.generic.texts import MonoReadOnlyTextInput

logger = logging.getLogger('tonguetwister.gui.chunkviews.default')
logger.setLevel(logging.DEBUG)


class RawChunkView(MonoReadOnlyTextInput):
    key_width = 40
    number_width = 6
    indent_string = ' ' * 4
    separator = f'{os.linesep}{indent_string}'

    def load(self, _, chunk: ChunkParser):
        text = self.title(chunk.resource)
        for section_name in chunk.sections:
            text += self.section_text(section_name, chunk)

        self.text = text
        self.scroll_to_top()

    @staticmethod
    def title(resource: ChunkResource):
        chunk_type = resource.chunk_type

        return f'{chunk_type.name} (FOUR CC: {chunk_type.four_cc}) at 0x{resource.chunk_address:08x}'

    def section_text(self, section_name, chunk):
        return self.section_title(section_name.capitalize()) + self.render_values(getattr(chunk, f'_{section_name}'))

    @staticmethod
    def section_title(title):
        return os.linesep.join([
            os.linesep,
            '============================',
            str(title),
            '============================',
            os.linesep
        ])

    def render_values(self, values, depth=1):
        lines = []

        if values is None:
            lines.append('None')
        elif isinstance(values, dict):
            for key, _value in values.items():
                lines.append(f'{str(key):.<{self.key_width}s}: {self.value_to_line(_value, depth)}')
        elif isinstance(values, (list, tuple)):
            for index, _value in enumerate(values):
                lines.append(f'[{index}]: {self.value_to_line(_value, depth, True)}')
        else:
            logger.warning(f'Not displaying chunk data due to bad type: {type(values)}')

        return self.join_with_indent(lines, depth)

    def value_to_line(self, value, depth, from_list=False):
        dots = '.' * self.key_width

        if isinstance(value, (dict, list, tuple)) and len(value) == 0:
            return ''
        if isinstance(value, (dict, list, tuple)):
            return os.linesep + self.render_values(value, depth + 1)
        elif isinstance(value, int) and from_list:
            return f'{dots}: {value:{self.number_width}d} (0x{value:08x})'
        elif isinstance(value, int):
            return f'{value:{self.number_width}d} (0x{value:08x})'
        elif from_list:
            return f'{dots}: {value}'
        else:
            return value

    def join_with_indent(self, lines, depth):
        return os.linesep.join([self.prefix_with_indent(line, depth) for line in lines])

    def prefix_with_indent(self, line, depth):
        return f'{self.indent_string * depth}{line}'


class RawEntriesChunkView(RawChunkView):
    def section_text(self, section_name, chunk):
        text = self.section_title(section_name.capitalize())
        values = getattr(chunk, f'_{section_name}')

        if section_name == 'entries':
            text += self.render_entries(values)
        else:
            text += self.render_values(values)

        return text

    def render_entries(self, entries, depth=0):
        lines = [self.render_entry(entry, depth, index) for index, entry in enumerate(entries)]

        return self.join_with_indent(lines, depth + 1)

    def render_entry(self, entry: InternalEntryParser, depth, index):
        long_depth = depth + 4

        title = f'[{index:4d}] {entry.__class__.__name__}:'
        value = self.render_values(getattr(entry, '_data'), long_depth)

        return self.prefix_with_indent(title, depth) + os.linesep + value
