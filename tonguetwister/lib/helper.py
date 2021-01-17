import os
import traceback
from inspect import getframeinfo, stack

from tonguetwister.lib.stream import ByteBlockIO


def grouper(ws, size, newline=False, indent=1):
    hex_str = ''.join(f'{ord(b):02x}' for b in ws.decode(ByteBlockIO.ENCODING))
    newline_str = '\n' if newline else ''
    indent_str = ' ' * indent

    groups = [hex_str[i:i+size] for i in range(0, len(hex_str), size)]

    return f'{newline_str}{indent_str}'.join(groups)


def exception_as_lines(ex):
    return flatten([
        s.strip(os.linesep).split(os.linesep)
        for s in traceback.format_exception(type(ex), ex, ex.__traceback__)
    ])


def maybe_encode_bytes(string, skip_encoding):
    return string if skip_encoding else str.encode(string)


class UnexpectedDataValue(RuntimeError):
    pass


def assert_data_value(data_value, values):
    if not isinstance(values, (list, tuple)):
        values = [values]

    if data_value not in values:
        caller = getframeinfo(stack()[1][0])

        raise UnexpectedDataValue(
            f'data_value {data_value} was not found in {values} for {caller.filename, caller.lineno}'
        )


def twos_complement(value, size=8):
    if size == 8:
        return 0xff - value + 1
    elif size == 16:
        return 0xffff - value + 1
    elif size == 32:
        return 0xffffff - value + 1
    else:
        raise AttributeError('size must be 8, 16 or 32')


def flatten(lst):
    return [item for items in lst for item in items]


def chunk(lst, size):
    return [lst[index:index+size] for index in range(0, len(lst), size)]


def format_unknowns(items):
    return [f'{key}: {value}' for key, value in items if key.startswith('u') or key.startswith('?')]
