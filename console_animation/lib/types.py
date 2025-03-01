
class VecT:
    ''' vec2[int] '''
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, v):
        x = self.x + v.x
        y = self.y + v.y
        return VecT(x, y)

    def __sub__(self, v):
        x = self.x - v.x
        y = self.y - v.y
        return VecT(x, y)

    def __mul__(self, v):
        x = self.x * v.x
        y = self.y * v.y
        return VecT(x, y)
    
    def __truediv__(self, v):
        ''' can only be ints so we floordiv for truediv '''
        x = self.x // v.x
        y = self.y // v.y
        return VecT(x, y)

    def __floordiv__(self, v):
        x = self.x // v.x
        y = self.y // v.y
        return VecT(x, y)

    def __str__(self):
        return f'VecT ({self.x}, {self.y})'


class Entity:
    def __init__(self, name, glyph, game):
        self.name = name
        self.game = game
        self.position:VecT = VecT(0, 0)
        self.glyph = glyph

    def move(self, delta:VecT):
        self.position = self.position + delta

    def get_buffer_index(self) -> int:
        ''' get index in buffer string for supplied position '''
        i = self.position.y * self. game.screen.width
        i = i - (self.game.screen.width - self.position.x)
        return i



if __name__ == '__main__':

    v = VecT(4, 5)
    vv = VecT(2, 4)

    print(v + vv)
