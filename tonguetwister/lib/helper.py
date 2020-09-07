import os
import traceback

from tonguetwister.lib.byte_block_io import ByteBlockIO


def grouper(ws, size, newline=False, indent=1):
    hex_str = ''.join(f'{ord(b):02x}' for b in ws.decode(ByteBlockIO.ENCODING))
    newline_str = '\n' if newline else ''
    indent_str = ' ' * indent

    groups = [hex_str[i:i+size] for i in range(0, len(hex_str), size)]

    return f'{newline_str}{indent_str}'.join(groups)


def splat_ordered_dict(ordered_dict, sep=', ', key_width=1):
    return sep.join(f'{k:.<{key_width}s}: {v}' for k, v in ordered_dict.items())


def exception_as_lines(ex):
    lines = [
        s.strip(os.linesep).split(os.linesep)
        for s in traceback.format_exception(type(ex), ex, ex.__traceback__)
    ]

    return [item for sublist in lines for item in sublist]  # Flatten the list
