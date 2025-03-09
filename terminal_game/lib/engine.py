from __future__ import annotations
import os
import threading 
import time
from enum import Enum
import random
from textwrap import wrap 

from pynput import keyboard
import pywinctl

from terminal_game.lib import buffers

from .types import Entity, VecT
from .entities import Player
from .entities import LandMine
from .patterns import *
from . import buffers

class GameState(Enum):
    # NOTE: unused atm - intended to make handling 
    #       the various modes a bit easier 
    MENU = 0
    GAME = 1
    DEAD = 2


class Screen:
    def __init__(self):
        self.width = os.get_terminal_size().columns
        self.height = os.get_terminal_size().lines - 2      # keep 2 lines for status - bin later
        self.buffer_len = self.width * self.height

    def clear(self):
        print("\033c", end="\033[A")


    def fill(self, c:str = '-') -> str:
        ''' '''
        terminal_size = os.get_terminal_size()
        s_len = self.width * (self.height)
        return ''.join(c for x in range(s_len))

    def buffer(self):
        s_len = self.width * (self.height - 4)
        return ''.join(' ' for x in range(s_len))

    def render_frame(self, frame): 
        self.clear()
        s = frame[:self.buffer_len]
        print(s)




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
        self.window = pywinctl.getActiveWindow().getHandle()    # get window handle on creation

        # NOTE: debuggery
        self.player_world_bounds = VecT(0,0)
        self.debug_str = 'debugstr'

    def _get_input_listener(self) -> keyboard.Listener:
        return keyboard.Listener(on_press = self.on_press, on_release=self.on_release, suppress=False)

    def on_release(self, key):
        pass

    def on_press(self, key):
        # suppress input from other windows 
        if not pywinctl.getActiveWindow().getHandle() == self.window:
            return None

        # TODO: this is acting as a pause button atm
        if key == keyboard.Key.esc:
            self.mode = 0
        try:
            if self.mode == 1:
                if key.char == ('w'):
                    self.player.jump()
                #if key.char == ('a'):
                #    self.player.move_delta += VecT(-1,0)
                #if key.char == ('s'):
                #    self.player.move_delta += VecT(0,1)
                #if key.char == ('d'):
                #    self.player.move_delta += VecT(1,0)
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

    def save_score(self, score:int):
        #TODO: dont do this
        p = 'score.txt'
        previous_scores = []
        max_scores = 5
        if not os.path.exists(p):
            with open(p, 'w') as f:
                pass

        with open(p, 'r+') as f:
            previous_scores = f.read()
            scorelist = previous_scores.split('\n')
            scorelist = [int(x) for x in scorelist if not x == '']
            scorelist.append(score)
            scorelist = sorted(scorelist, reverse=True)
            if len(scorelist) >= max_scores:
                scorelist = scorelist[:max_scores]
            f.seek(0)
            f.truncate()
            f.writelines(f'{str(x)}\n' for x in scorelist)

    def add_entity(self, e:Entity, position:VecT):
        e.position = position
        self.entities.append(e)

    def check_player_collisions(self):
        # TODO: handle collisions with bounds of entity
        player_bounds = self.player.sprite.bounds + self.player.position

        collision_objects = []
        # do bounds for player and entity overlap
        for entity in self.entities:
            entity_bounds = entity.sprite.bounds + entity.position
            # NOTE: y coords increase down the screen
            # bounds.y is bottom
            # bounds.x is right

            # in reference to player
            is_fully_left = entity.position.x + 1 > player_bounds.x
            is_fully_right = entity_bounds.x - 1 < self.player.position.x
            is_fully_below = entity_bounds.y - 1 < self.player.position.y
            is_fully_above = entity.position.y + 1 > player_bounds.y 

            '''
            if is_fully_below:
                self.debug_str = 'below'
            elif is_fully_above:
                self.debug_str = 'above'
            elif is_fully_left:
                self.debug_str = 'left'
            elif is_fully_right:
                self.debug_str = 'right'
            else:
                self.debug_str = 'boop'
            '''
            if is_fully_right or is_fully_left or is_fully_above or is_fully_below:
                continue
            else:
                collision_objects.append(entity)
        for o in collision_objects:
            result = self.player.collide(o)

    def process_entities(self):
        # handle behaviours
        self.player.behave()
        [x.behave() for x in self.entities]

    def spawn_entities(self):
        if not self.frame_counter % 120 == 0:
            return None

        random_len = random.randint(3, self.screen.height - 8)
        line_pattern = LineVerticalPattern(self, LandMine('', self), random_len)
        line_entities = line_pattern.entities

        for e in line_entities:
            e.position = e.position + VecT(self.screen.width - 1, self.screen.height - line_pattern.side_length)
            self.add_entity(e, e.position)

    def menu_loop(self):
        # frame_buffer = self.screen.fill(' ')
        frame_buffer = buffers.buffer_centered(buffers.screen_menu)
        self.screen.render_frame(frame_buffer)
        print('\uee25', 'F to start', 'Q to quit')


    def death_loop(self):
        frame_buffer = buffers.buffer_h_centered(buffers.screen_death)
        frame_buffer = buffers.buffer_centered(buffers.get_string_from_file('score.txt'), frame_buffer=frame_buffer)
        self.screen.render_frame(frame_buffer)
        print('\uee25', 'F to return to menu')

    def game_loop(self):
        # clear it all out
        frame_buffer = self.screen.fill(' ')
        self.spawn_entities()
        self.process_entities()
        # check collisions
        self.check_player_collisions()
        # draw other entities
        for entity in self.entities:
            frame_buffer = buffers.add_pattern_to_buffer(entity.sprite.string, frame_buffer, entity.position)
        # draw the player
        frame_buffer = buffers.add_pattern_to_buffer(self.player.sprite.string, frame_buffer, self.player.position)
        # render the frame
        self.screen.render_frame(frame_buffer)
        #print('\uee25', self.score, self.player.position, self.player_world_bounds, self.debug_str)

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
        self.score = 0
        self.entities = []
        self.player.position = VecT(30, 1)

    def init(self):
        ''' 
        game and listener need to run in different threads 
        or listener will block the game 
        '''
        self.reset()
        self.input_listener.start()
        thread = threading.Thread(target = self.main_loop)
        thread.start()




