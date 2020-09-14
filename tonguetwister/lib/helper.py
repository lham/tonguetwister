import os
import traceback
from collections import OrderedDict
from inspect import getframeinfo, stack

from tonguetwister.lib.byte_block_io import ByteBlockIO


def grouper(ws, size, newline=False, indent=1):
    hex_str = ''.join(f'{ord(b):02x}' for b in ws.decode(ByteBlockIO.ENCODING))
    newline_str = '\n' if newline else ''
    indent_str = ' ' * indent

    groups = [hex_str[i:i+size] for i in range(0, len(hex_str), size)]

    return f'{newline_str}{indent_str}'.join(groups)


def splat_ordered_dict(ordered_dict, sep=', ', key_width=1):
    return sep.join(f'{k:.<{key_width}s}: {_handle_value(v, sep, key_width)}' for k, v in ordered_dict.items())


def splat_list(lst, sep=', ', key_width=1):
    return sep.join(f'{_handle_value(item, sep, key_width)}' for item in lst)


def _handle_value(value, sep, key_width):
    if isinstance(value, OrderedDict):
        return sep + (' ' * key_width) + splat_ordered_dict(value, sep=(sep + ' ' * key_width))
    elif isinstance(value, (list, tuple)):
        return splat_list(value, sep, key_width)
    else:
        return value


def exception_as_lines(ex):
    lines = [
        s.strip(os.linesep).split(os.linesep)
        for s in traceback.format_exception(type(ex), ex, ex.__traceback__)
    ]

    return [item for sublist in lines for item in sublist]  # Flatten the list


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
