from __future__ import annotations
from .entities import *
from terminal_game.lib import entities

class Pattern:
    def __init__(self, game):
        self.game = game
        self.rate = 10      # how many frames pass before we do something
        self.entities = self.generate_pattern()

    def generate_pattern(self) -> list[Entity]:
        return []



class LineVerticalPattern(Pattern):
    def __init__(self, game, side_length):
        self.side_length = side_length
        super().__init__(game)
        self.rate = 30

    def generate_pattern(self)-> list[Entity]:
        entities = []
        for y in range(self.side_length):
                e = LandMine(f'mine{y}', self.game)
                e.position = VecT(0,y)
                entities.append(e)
                e = LandMine(f'mine{y}', self.game)
                e.position = VecT(1,y)
                entities.append(e)
                
        return entities

