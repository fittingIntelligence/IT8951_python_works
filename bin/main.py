#
# Poet Writer
# Based on ZeroWriter, but overhauled almost completely

import time
import keyboard
import keymaps
from PIL import Image, ImageDraw, ImageFont
# from waveshare_epd import new4in2part
import textwrap
import subprocess
import signal
import os
from pathlib import Path

import argparse

from test_functions import *

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

args = parse_args()

from IT8951.display import AutoEPDDisplay

print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=args.mirror, spi_hz=24000000)

epd = display.epd

print('VCOM set to', epd.get_vcom())


text = '''
Welcome my love,
this is a fun gift for you

love and kisses, B
'''

clear_display(display)
partial_update(display)
display_image_8bpp(display)
partial_update_msg(display, text)

