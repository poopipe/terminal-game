import sys 
import os

class Screen:
    def __init__(self ):
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
        s_len = self.width * (self.height - 2)
        return ''.join(' ' for x in range(s_len))

    def render_frame(self, frame):
        self.clear()
        print(frame)

class Engine:
    def __init__(self):
        self.width = 120
        self.height = 80
        self.screen = Screen()

    def clear(self):
        print(f'\033[{self.height}]A\033[2K', end='')
        self.screen.clear()



if __name__ == '__main__':
    s = Screen()
    s.render_frame(s.fill())

