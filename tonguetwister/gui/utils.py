import os

from kivy.clock import Clock


def update_text_area(text_area, lines, line_numbers=True, scroll_to_top=True):
    if line_numbers:
        text_area.text = os.linesep.join([f'{i:3d} {line}' for i, line in enumerate(lines)])
    else:
        text_area.text = os.linesep.join(lines)

    if scroll_to_top:
        Clock.schedule_once(lambda _: setattr(text_area, 'cursor', (0, 0)))
