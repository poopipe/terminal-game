'''https://www.nerdfonts.com/cheat-sheet'''


import sys 
import os
import time
import threading 

# pynput handles input - I'd like to do this myself but its
# a pain in the arse
from pynput import keyboard

from console_animation.lib.engine import Game, Screen
from console_animation.lib.types import VecT
from console_animation.lib.types import Entity




if __name__ == '__main__':
    game = Game()
    game.add_entity('bastard', '\ueaaf', VecT(40, -12))
    game.init()



