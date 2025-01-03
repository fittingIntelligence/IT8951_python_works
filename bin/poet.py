#
# Poet Writer
# Copyright Fitting Intelligence PTY Ltd

from pathlib import Path
import argparse
from eink import eink

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
current_screen='home'
current_file='file_001.txt'

print('Initializing EPD...')
ui_control = eink(current_screen, current_file, args)
epd = ui_control.display.epd
print('VCOM set to', epd.get_vcom())

# ui_control.clear_display()
# ui_control.display_image_8bpp()

ui_control.partial_update_msg('XXXxxXXX','')
ui_control.backspace(0, 0, 'XXXxx', 'XXXxxXXX')


