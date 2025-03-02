from ast import match_case
import os
import threading 
import time
from enum import Enum
import random

from .types import Entity, VecT
from .entities import Player
from .entities import LandMine
from pynput import keyboard

class GameState(Enum):
    MENU = 0
    GAME = 1


class Screen:
    def __init__(self):
        self.width = os.get_terminal_size().columns
        self.height = os.get_terminal_size().lines - 2      # keep 2 lines for status - bin later
        print(self.height)

    def clear(self):
        print("\033c", end="\033[A")

    def fill(self, c:str = '-')->str:
        ''' '''
        terminal_size = os.get_terminal_size()
        s_len = terminal_size.columns * (terminal_size.lines - 3)
        return ''.join(c for x in range(s_len))

    def buffer(self):
        s_len = self.width * (self.height - 4)
        return ''.join(' ' for x in range(s_len))

    def render_frame(self, frame):
        self.clear()
        print(frame)

class Game:
    def __init__(self):
        self.run = True
        self.fps = 60
        self.screen = Screen()
        self.entities = []
        self.player = Player('player', self)
        self.input_listener = self._get_input_listener()
        self.frame_counter = 0
        self.score = 0
        self.mode = 0   # menu/game/whatever - we need a way to behave differently when we're in menu/game etc

    def _get_input_listener(self) -> keyboard.Listener:
        return keyboard.Listener(on_press = self.on_press, on_release=self.on_release)

    def on_release(self, key):
        pass 

    def on_press(self, key):
        # TODO: this is acting as a pause button atm
        if key == keyboard.Key.esc:
            self.mode = 0
        try:
            if self.mode == 1:
                if key.char == ('w'):
                    self.player.move(VecT(0,-1))
                if key.char == ('a'):
                    self.player.move(VecT(-1,0))
                if key.char == ('s'):
                    self.player.move(VecT(0,1))
                if key.char == ('d'):
                    self.player.move(VecT(1,0))
            if self.mode == 0:
                if key.char == ('f'):
                    self.mode = 1
                if key.char == ('q'):
                    self.run = False
            if self.mode == 2:
                if key.char == ('f'):
                    self.mode = 0

        except Exception as e:
            pass

    def add_entity(self, e:Entity, position:VecT):
        e.position = position
        self.entities.append(e)

    def check_player_collisions(self):
        collision_objects = [x for x in self.entities if x.position == self.player.position]
        for o in collision_objects:
            self.entities.remove(o)
            result = self.player.collide(o)

    def process_entities(self):
        # handle behaviours
        [x.behave() for x in self.entities]

    def spawn_entities(self):
        # spawn rate here
        if not self.frame_counter % 20 == 0:
            return None
        # spawn chance here
        if len(self.entities) <= 10:
            chance = random.randint(0, 9)
            if chance >= 8:
                random_y = random.randint(1, self.screen.height-1)
                self.add_entity(LandMine('mine_a', self), VecT(self.screen.width, random_y))

    def menu_loop(self):
        self.screen.clear()
        frame_buffer = self.screen.fill('_')
        self.screen.render_frame(frame_buffer)
        print('\uee25', 'Press F to start')

    def death_loop(self):
        self.screen.clear()
        frame_buffer = self.screen.fill('x')
        self.screen.render_frame(frame_buffer)
        print('\uee25', 'DEAD, press F to return to menu')

    def game_loop(self):
        # clear it all out
        self.screen.clear()
        frame_buffer = self.screen.fill(' ')
        self.spawn_entities()
        self.process_entities()
        # check collisions
        self.check_player_collisions()

        # draw other entities
        for entity in self.entities:
            i = entity.get_buffer_index()
            frame_buffer = frame_buffer[:i] + entity.glyph + frame_buffer[i + 1:]

        # draw the player
        i = self.player.get_buffer_index() 
        frame_buffer = frame_buffer[:i] + self.player.glyph + frame_buffer[i + 1:]

        # render the frame
        self.screen.render_frame(frame_buffer)
        print('\uee25', self.score)

        # NOTE: Frame counter is used to time spawns
        self.frame_counter += 1

    def main_loop(self):
        while self.run:
            match self.mode:
                case 0: # Menu
                    self.menu_loop()
                case 1: # Game
                    self.game_loop()
                case 2: # Death
                    self.death_loop()
                case _:
                    self.menu_loop()
            time.sleep(1.0 / float(self.fps))
    
    def reset(self):
        self.frame_counter = 0
        self.entities = []
        self.player.position = VecT(30, 11)

    def init(self):
        ''' 
        game and listener need to run in different threads 
        or listener will block the game 
        '''
        self.reset()
        self.input_listener.start()
        thread = threading.Thread(target = self.main_loop)
        thread.start()




