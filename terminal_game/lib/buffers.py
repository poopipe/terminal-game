''' buffers '''
import os
import math

from terminal_game.lib.types import VecT

# TODO: move these later


screen_death = """
┌────────────────────────────────────────────┐
│░█░█░█▀█░█░█░░░█▀█░█▀▄░█▀▀░░░█▀▄░█▀▀░█▀█░█▀▄│
│░░█░░█░█░█░█░░░█▀█░█▀▄░█▀▀░░░█░█░█▀▀░█▀█░█░█│
│░░▀░░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░▀░▀░▀▀░│
└────────────────────────────────────────────┘"""

screen_menu = """
┌──────────────────────────────────────────┐
│░█▀▀░█░█░▀█▀░▀█▀░░░█▀▀░█░░░█▀█░█▀█░█▀█░█░█│
│░▀▀█░█▀█░░█░░░█░░░░█▀▀░█░░░█▀█░█▀▀░█▀▀░░█░│
│░▀▀▀░▀░▀░▀▀▀░░▀░░░░▀░░░▀▀▀░▀░▀░▀░░░▀░░░░▀░│
│░░░░░░░░░░░░░█▀▄░▀█▀░█▀▄░█▀▄░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░█▀▄░░█░░█▀▄░█░█░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░▀▀░░▀▀▀░▀░▀░▀▀░░░░░░░░░░░░░░░│
└──────────────────────────────────────────┘"""


def get_string_from_file(p):
    with open(p) as f:
        return f.read()


def get_buffer_index(pos:VecT, width) -> int:
    ''' get index in buffer string for supplied position '''
    i = math.floor(pos.y) * width
    i = i - (width - pos.x)
    return i


def buffer_centered(s:str) -> str:

    terminal_size = os.get_terminal_size()
    buffer_len = terminal_size.columns * (terminal_size.lines - 3)
    frame_buffer =''.join(' ' for x in range(buffer_len))

    # process string
    # strip leading newline if present
    if s[0] == ['\n']:
        s = s[1:]
    lines = s.split('\n')

    width = 0
    height = len(lines)
    for l in lines:
        width = len(l) if len(l) > width else width

    s_offset = VecT(
        width // 2,
        height // 2
    )

    origin = VecT(
        terminal_size.columns // 2,
        terminal_size.lines // 2
    )

    top_left = origin - s_offset

    for i in range(len(lines)):
        for c in range(len(lines[i])):
            p = VecT(c, i + 1) + top_left
            idx = get_buffer_index(p, terminal_size.columns)
            frame_buffer = frame_buffer[:idx] + lines[i][c] + frame_buffer[idx + 1:]

    return frame_buffer






if __name__ == '__main__':
    s = """
┌────────────────────────────────────────────┐
│░█░█░█▀█░█░█░░░█▀█░█▀▄░█▀▀░░░█▀▄░█▀▀░█▀█░█▀▄│
│░░█░░█░█░█░█░░░█▀█░█▀▄░█▀▀░░░█░█░█▀▀░█▀█░█░█│
│░░▀░░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░░░▀▀░░▀▀▀░▀░▀░▀▀░│
└────────────────────────────────────────────┘"""

    print(buffer_centered(s))


    

    
