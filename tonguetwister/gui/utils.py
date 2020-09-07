import os
import re

from kivy.cache import Cache
from kivy.clock import Clock

from tonguetwister.lingo_decompiler import Decompiler


def update_text_area(text_area, lines, line_numbers=True, to_top=True):
    if line_numbers:
        text_area.text = os.linesep.join([f'{i:3d} {line}' for i, line in enumerate(lines)])
    else:
        text_area.text = os.linesep.join(lines)

    if to_top:
        scroll_to_top(text_area)


def scroll_to_top(text_area):
    Clock.schedule_once(lambda _: setattr(text_area, 'cursor', (0, 0)))


Cache.register('decompiled', limit=1000)


def load_script_function(script_index, function_index, namelist, script):
    decompiler = Cache.get('decompiled', f'script-{script_index}-{function_index}')

    if decompiler is None:
        decompiler = _decompile_script_function(script, namelist, function_index)
        Cache.append('decompiled', f'script-{script_index}-{function_index}', decompiler)

    return decompiler


def _decompile_script_function(script, namelist, function_index):
    function = script.functions[function_index]

    decompiler = Decompiler(catch_exceptions=True)
    decompiler.to_pseudo_code(function, namelist, script)

    return decompiler


def highlight_word_in_text_area(text_area):
    # noinspection PyProtectedMember
    current_line = text_area._lines[text_area.cursor_row]
    text_before_cursor = current_line[:text_area.cursor_col]
    text_after_cursor = current_line[text_area.cursor_col:]

    pattern = re.compile(r'[^A-Za-z0-9_]')

    start = [m.end(0) for m in re.finditer(pattern, text_before_cursor)]
    start = len(text_before_cursor) - (start[-1] if len(start) > 0 else 0)

    end = re.search(pattern, text_after_cursor)
    end = end.start() if end is not None else len(text_after_cursor)

    index_start = text_area.cursor_index() - start
    index_stop = text_area.cursor_index() + end

    result = text_area.text[index_start:index_stop]
    if len(result) > 0:
        Clock.schedule_once(lambda _: text_area.select_text(index_start, index_stop), 0)
