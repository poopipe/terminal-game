import sys 
import os
import threading 
import time

from .types import Entity, VecT
from pynput import keyboard

class Screen:
    def __init__(self):
        self.width = os.get_terminal_size().columns
        self.height = os.get_terminal_size().lines
        print(self.height)

    def clear(self):
        print("\033c", end="\033[A")

    def fill(self):
        ''' i think we want to make a string thats as long 
        as all the space we have available'''
        terminal_size = os.get_terminal_size()
        s_len = terminal_size.columns * (terminal_size.lines - 2)
        return ''.join('-' for x in range(s_len))

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
        self.player = Entity('player', '\uee25', self)
        self.input_listener = self._get_input_listener()

    def _get_input_listener(self) -> keyboard.Listener:
        return keyboard.Listener(on_press = self.on_press, on_release=self.on_release)

    def on_release(self, key):
        pass 

    def on_press(self, key): 
        if key == keyboard.Key.esc:
            print('quittin')
            self.run = False
        try:
            if key.char == ('w'):
                self.player.move(VecT(0,-1))
            if key.char == ('a'):
                self.player.move(VecT(-1,0))
            if key.char == ('s'):
                self.player.move(VecT(0,1))
            if key.char == ('d'):
                self.player.move(VecT(1,0))
        except Exception as e:
            pass

    def add_entity(self, name:str, glyph:str, position:VecT):
        e = Entity(name, glyph, self)
        e.position = position
        self.entities.append(e)

    
    def main_loop(self):
        while self.run:
            # clear it all out
            self.screen.clear()
            frame_buffer = self.screen.fill()

            # draw other entities

            for entity in self.entities:
                i = entity.get_buffer_index()
                frame_buffer = frame_buffer[:i] + entity.glyph + frame_buffer[i + 1:]


            # draw the player
            i = self.player.get_buffer_index() 
            frame_buffer = frame_buffer[:i] + self.player.glyph + frame_buffer[i + 1:]
            # render the frame
            self.screen.render_frame(frame_buffer)
            print('\uee25', self.player.position)

            time.sleep(1.0 / float(self.fps))

    def init(self):
        ''' do the beginning stuff '''
        self.input_listener.start()
        thread = threading.Thread(target = self.main_loop)
        thread.start()




