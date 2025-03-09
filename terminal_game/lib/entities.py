from __future__ import annotations

from .types import Entity, VecT
from .sprites import Sprite
from . import sprites

class LandMine(Entity):
    def __init__(self, name, game):
        super().__init__(name, '█', game)
        self.sprite = Sprite(sprites.landmine)

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
        self.move_delta: VecT = VecT(0,0)

        self.jump_len:int = 3
        self.jump_remain:int = 0
        self.jump_cooldown:int = 30
        self.jump_cooldown_remain = 0
        self.jump_hangtime = 10
        self.jump_hangtime_remain = 0
        self.sprite = Sprite(sprites.player)

    def collide(self, entity):
        if isinstance(entity, LandMine):
            self.die()

    def jump(self):
        if self.jump_cooldown_remain <= 0:
            if self.jump_remain <=0:
                self.jump_cooldown_remain = self.jump_cooldown
                self.jump_remain = self.jump_len
                self.jump_hangtime_remain = self.jump_hangtime

    def move(self, delta:VecT):
        # gravity
        if self.game.frame_counter % 10 == 0:
            if self.jump_hangtime_remain <=0:
                self.move_delta += VecT(0, 1)
        new_position = self.position + self.move_delta

        if new_position.x >= 0 and new_position.x < self.game.screen.width:
            self.position.x = new_position.x
        if new_position.y >= 1 and new_position.y <= self.game.screen.height - 1:
            self.position.y = new_position.y
        self.move_delta = VecT(0, 0)


    def behave(self):
        if self.jump_remain > 0:
            self.move_delta += VecT(0,-2)
            self.jump_remain -= 1

        if self.jump_hangtime_remain > 0:
            self.jump_hangtime_remain -= 1

        if self.jump_cooldown_remain > 0:
            self.jump_cooldown_remain -= 1

        if self.position.y >= self.game.screen.height - 1:
            self.die()
            return None
        self.move(VecT(0, 0))


    def die(self):
        self.game.save_score(self.game.score)
        self.game.mode = 2  # death screen
        self.game.reset()





