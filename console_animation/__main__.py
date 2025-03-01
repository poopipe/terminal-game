'''https://www.nerdfonts.com/cheat-sheet'''
from console_animation.lib.engine import Game
from console_animation.lib.types import VecT
from console_animation.lib import entities




if __name__ == '__main__':
    game = Game()
    game.add_entity(entities.LandMine('mine_a', game), VecT(71, 11))
    game.player.position = VecT(30, 11)

    # TODO: change add entity function to take entity subtypes
    game.init()


