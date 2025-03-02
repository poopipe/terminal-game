from __future__ import annotations

from .types import Entity, VecT


class LandMine(Entity):
    def __init__(self, name, game):
        super().__init__(name, 'x', game)

    def behave(self):
        if self.position.x <= 0:
            self.die()
        # we dont want to move every frame
        if self.game.frame_counter % 10 == 0:
            self.move(VecT(-1,0))

    def die(self):
        self.game.score += 10
        self.game.entities.remove(self)


class Player(Entity):
    def __init__(self, name, game):
        super().__init__(name, '\uee25', game)

    def collide(self, entity):
        print(f'player collided with{entity}')
        if isinstance(entity, LandMine):
           self.die()

    def behave(self):
        if self.game.frame_counter % 10 == 0:
            self.move(VecT(0, 1))

    def die(self):
        #self.game.entities.remove(self)
        #self.glyph = 'Q'
        self.game.mode = 2  # death screen
        self.game.reset()





