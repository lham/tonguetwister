from tonguetwister.lib.byte_block_io import ByteBlockIO


def grouper(ws, size, newline=False, indent=1):
    hex_str = ''.join(f'{ord(b):02x}' for b in ws.decode(ByteBlockIO.ENCODING))
    newline_str = '\n' if newline else ''
    indent_str = ' ' * indent

    groups = [hex_str[i:i+size] for i in range(0, len(hex_str), size)]

    return f'{newline_str}{indent_str}'.join(groups)


def splat_ordered_dict(ordered_dict):
    return ', '.join(f'{k}: {v}' for k, v in ordered_dict.items())
