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


def buffer_h_centered(s:str, v_offset=4, frame_buffer:None|str = None) -> str:
    ''' place s at horizontal centre and v_offset of frame buffer '''
    terminal_size = os.get_terminal_size()
    buffer_len = terminal_size.columns * (terminal_size.lines - 3)
    if not frame_buffer:
        frame_buffer =''.join(' ' for x in range(buffer_len))
    lines = list_str(s)
    width, height = get_line_bounds(lines)
    offset = get_offset_centered(width, height, terminal_size.columns, terminal_size.lines)
    offset = VecT(offset.x, v_offset)
    return add_pattern_to_buffer(s, frame_buffer, offset)


def buffer_centered(s:str, frame_buffer:None|str = None) -> str:
    ''' place s in center of frame buffer '''
    terminal_size = os.get_terminal_size()
    buffer_len = terminal_size.columns * (terminal_size.lines - 3)
    if not frame_buffer:
        frame_buffer =''.join(' ' for x in range(buffer_len))
    lines = list_str(s)
    width, height = get_line_bounds(lines)
    offset = get_offset_centered(width, height, terminal_size.columns, terminal_size.lines)
    return add_pattern_to_buffer(s, frame_buffer, offset)


def get_offset_centered(pattern_width:int, pattern_height:int, buffer_width:int, buffer_height:int) -> VecT:
    ''' get offset required to place s in centre of framebuffer '''
    origin = VecT(
        buffer_width// 2,
        buffer_height // 2
    )

    offset = VecT(
        pattern_width // 2,
        pattern_height // 2
    )
    return origin - offset


def list_str(s:str)-> list[str]:
    # process string
    # strip leading newline if present
    if s[0] == ['\n']:
        s = s[1:]
    return s.split('\n')

def get_line_bounds(lines:list[str])->tuple[int, int]:
    ''' return width (len of longest item in lines) and height (len of lines) '''
    width = 0
    for l in lines:
        width = len(l) if len(l) > width else width
    return width, len(lines)

def add_pattern_to_buffer(s:str, frame_buffer:str, offset:VecT) -> str:
    ''' position s at offset in frame_buffer and return buffer '''
    terminal_size = os.get_terminal_size()
    buffer_len = terminal_size.columns * (terminal_size.lines - 3)
    # process string
    lines = list_str(s)
    for i in range(len(lines)):
        for c in range(len(lines[i])):
            p = VecT(c, i + 1) + offset 
            idx = get_buffer_index(p, terminal_size.columns)
            # dont draw if position in line is past terminal_size.columns
            if p.x < terminal_size.columns and p.y < terminal_size.lines - 3:
                frame_buffer = frame_buffer[:idx] + lines[i][c] + frame_buffer[idx + 1:]

    return frame_buffer[:buffer_len]

