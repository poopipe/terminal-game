'''https://www.nerdfonts.com/cheat-sheet'''


import sys 
import os
import time
import threading 

# pynput handles input - I'd like to do this myself but its
# a pain in the arse
from pynput import keyboard

from console_animation.lib.engine import Screen

run = True
player_coords = (12,7)

def on_press(key): 
    global run
    global player_coords
    
    if key == keyboard.Key.esc:
        print('quittin')
        # Stop listener
        run = False
    try:
        if key.char == ('w'):
            player_coords = move_player((0,-1))
        if key.char == ('a'):
            player_coords = move_player((-1,0))
        if key.char == ('s'):
            player_coords = move_player((0,1))
        if key.char == ('d'):
            player_coords = move_player((1,0))
    except Exception as e:
        pass
    
    #try:
    #    print(f'pressed {key.char}')
    #except AttributeError:
    #    print(f'special key {key}')

def on_release(key):
    # print(f'{key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def get_player_pos(screen:Screen, player_coords:tuple[int,int]) -> int:
    ''' we want player to move up/down/left/right
        so we need to take an on screen position
        (col, row) and map that to a location in the 
        frame buffer (long string)
    '''

    n = player_coords[1] * screen.width
    diff = screen.width - player_coords[0]

    n = n - diff
    return n

def move_player(delta):
    x = player_coords[0] + delta[0]
    y = player_coords[1] + delta[1]

    return (x,y)


def main_loop():
    fps = 60 
    frame_index = 0
    count = 0
    screen = Screen()
    print(screen)

    while run:
        # bail after n iterations in case i
        # fuck something up
        #if count > 20:
        #    sys.exit(0)
        
        #player_coords = (12 + count, count)
        player_pos = get_player_pos(screen, player_coords)

        buffer = screen.fill()
        buffer = buffer[:player_pos] + '\uee25' + buffer[player_pos + 1:]

        screen.render_frame(buffer)
        
        print('\uee25', count, player_pos, player_coords)

        count = count + 1
        
        time.sleep(1 / fps)


if __name__ == '__main__':



    # non blocking keyboard listener
    listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
    listener.start()

    thread = threading.Thread(target=main_loop)
    thread.start()

