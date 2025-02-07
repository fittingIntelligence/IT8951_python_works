from pathlib import Path
import argparse
from eink import eink
from modules.key_overrides_simple import keyboard_overrides
import file_operations
import keyboard
import signal
from datetime import datetime
from poetree_ctrl import poetree
import time

# Get current datetime in ISO 8601 format
startup_datetime = datetime.now().isoformat()

ui_backgrounds = {
    'splash'    : 'images/poetpre.png',
    'ls'        : 'images/load_screen.png',
    'gs'        : 'images/generic_window.png',
    'shutdown'  : 'images/shutdown.png',
}

def parse_args():
    p = argparse.ArgumentParser(description='Test EPD functionality')
    p.add_argument('-v', '--virtual', action='store_true',
                   help='display using a Tkinter window instead of the '
                        'actual e-paper device (for testing without a '
                        'physical device)')
    p.add_argument('-r', '--rotate', default=None, choices=['CW', 'CCW', 'flip'],
                   help='run the tests with the display rotated by the specified value')
    p.add_argument('-m', '--mirror', action='store_true',
                   help='Mirror the display (use this if text appears backwards)')
    return p.parse_args()

# def main():
args = parse_args()
args.rotate='flip'


p = poetree(
    ui  = eink(args),
    io  = file_operations.loadscreen(),
    win = file_operations.loadscreen(),
    kb  = keyboard_overrides(),
)

p.ui.clear_display()
# p.ui.display_image_8bpp()
p.ui.print_system_info()

# def sim_keypress(t):
#     for i in t:
#         yield i

# def press_key(t):
#     sk = sim_keypress(t)
#     for i in sk:
#         p.kb.input_content += i


def check_content_change():
    kb = p.input_content
    scrn = p.content
    return [kb,scrn]


# press_key('Hello there my friend')
# kb, scrn = check_content_change()
# if kb != scrn:
#     print ([kb,scrn])
#     p.ui.partial_update_msg(kb,scrn)
#     p.content = kb[:]
    
# def do_instructions():
#     for i in p.kb.instructions:
#         p[i]()
#         print(i)
        
#     pass

keyboard.on_press(p.key_down_watcher, suppress=False) #handles modifiers and shortcuts
keyboard.on_release(p.key_up_watcher, suppress=True)
signal.signal(signal.SIGINT, p.kb.handle_interrupt)

try:
    while True:
        time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs
        
        kb, scrn = check_content_change()
        if kb != scrn:
            print ([kb,scrn])
            p.partial_update_msg(kb,scrn)

        pass
except KeyboardInterrupt:
    pass
