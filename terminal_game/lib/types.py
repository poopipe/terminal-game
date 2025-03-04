from __future__ import annotations
import math

class VecT:
    ''' vec2[int] '''
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, v:VecT) -> VecT:
        x = self.x + v.x
        y = self.y + v.y
        return VecT(x, y)

    def __sub__(self, v:VecT) -> VecT:
        x = self.x - v.x
        y = self.y - v.y
        return VecT(x, y)

    def __mul__(self, v:VecT) -> VecT:
        x = self.x * v.x
        y = self.y * v.y
        return VecT(x, y)
    
    def __truediv__(self, v:VecT) -> VecT:
        ''' can only be ints so we floordiv for truediv '''
        x = self.x // v.x
        y = self.y // v.y
        return VecT(x, y)

    def __floordiv__(self, v:VecT) -> VecT:
        x = self.x // v.x
        y = self.y // v.y
        return VecT(x, y)

    def __eq__(self, v:object) -> bool:
        if not isinstance(v, VecT):
            return False
        if self.x == v.x and self.y == v.y:
            return True
        return False
    
    def __lt__(self, v:object) -> bool:
        if not isinstance(v, VecT):
            return False
        if self.x < v.x and self.y < v.y:
            return True
        return False 

    def __le__(self, v:object) -> bool:
        if not isinstance(v, VecT):
            return False
        if self.x <=v.x and self.y <=v.y:
            return True
        return False
    
    def __gt__(self, v:object) -> bool:
        if not isinstance(v, VecT):
            return False
        if self.x > v.x and self.y > v.y:
            return True
        return False
    
    def __ge__(self, v:object) -> bool:
        if not isinstance(v, VecT):
            return False
        if self.x >= v.x and self.y >= v.y:
            return True
        return False

    def __str__(self) -> str:
        return f'VecT ({self.x}, {self.y})'


class Entity:
    def __init__(self, name, glyph, game):
        self.name = name
        self.game = game
        self.alive = True
        self.position:VecT = VecT(0, 0)
        self.glyph = glyph
        self.colliders = []

    def move(self, delta:VecT):
        new_position = self.position + delta
        if new_position.x >= 0 and new_position.x < self.game.screen.width:
            self.position.x = new_position.x
        if new_position.y >= 1 and new_position.y <= self.game.screen.height:
            self.position.y = new_position.y

    def get_buffer_index(self) -> int:
        ''' get index in buffer string for supplied position '''
        i = math.floor(self.position.y) * self.game.screen.width
        i = i - (self.game.screen.width - self.position.x)
        return i

    def collide(self, entity:Entity):
        ''' handle collision with other entity '''
        pass

    def behave(self):
        ''' do whatever this entity does - probably at every frame '''
        pass
    
    def die(self):
        '''  '''
        pass

if __name__ == '__main__':

    v = VecT(4, 5)
    vv = VecT(2, 4)

    print(v + vv)
