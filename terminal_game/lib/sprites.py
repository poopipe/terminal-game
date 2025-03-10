from __future__ import annotations
from terminal_game.lib.types import VecT


class Sprite:
    def __init__(self, s:str):
        self.string:str = s
        self.buffer:list[str] = self._get_buffer(s)
        self.bounds:VecT = self._get_bounds()

    def _get_buffer(self, s:str) -> list[str]:
        if s[0] == ['\n']:
            s = s[1:]
        return s.split('\n')

    def _get_bounds(self):
        ''' return width (len of longest item in lines) and height (len of lines) '''
        width = 0
        for l in self.buffer:
            width = len(l) if len(l) > width else width
        return VecT(width, len(self.buffer))


player = """
▄▀▀▄
▀▄▄▀"""
landmine = """
▓██▓
▓██▓
▓██▓"""


