from __future__ import annotations
import copy
from .types import *
from .entities import *
from terminal_game.lib import entities

class Pattern:
    def __init__(self, game, base_entity):
        self.game:Game = game
        self.rate: int = 10      # how many frames pass before we do something
        self.base_entity:Entity = base_entity
        self.entities:list[Entity] = self.generate_pattern(self.base_entity)

    def generate_pattern(self, base_entity:Entity) -> list[Entity]:
        return []



class LineVerticalPattern(Pattern):
    def __init__(self, game, base_entity, side_length):

        self.side_length = side_length
        super().__init__(game, base_entity)
        self.entities = self.generate_pattern(self.base_entity)
        self.rate = 30

    def generate_pattern(self, base_entity)-> list[Entity]:
        entities = []
        entity_height = base_entity.sprite.bounds.y - 1
        entity_count = self.side_length // entity_height

        for y in range(entity_count):
            e = copy.copy(base_entity)
            e.position = VecT(0,y * entity_height)
            entities.append(e)

        return entities

