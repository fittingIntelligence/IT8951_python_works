#
# Poet Writer
# Based on ZeroWriter, but overhauled almost completely
import time
import keyboard
from PIL import Image, ImageDraw, ImageFont
import textwrap
import subprocess
import signal
import os
from pathlib import Path
import argparse
from writer_functions import *
import ui 

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
fontsize=36

input_content ='Hello Kitten'





font = set_font_size(fontsize)

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
To my Kitten,

To your authoring adventures and beyond!

Love and kisses, 

Byron

2024-12-21
'''

clear_display(display)
# partial_update(display)
# display_image_8bpp(display,'images/poetpre.png')
# partial_update_msg(display, text, font)

# text = []
# for i in range(10):
#     text.append(str(i))
#     partial_update_msg(display, ' '.join(text), font)

# if __name__ == '__main__':
#     main()

def update_display(x):
    global text
    text += x
    partial_update_msg(display, text, font)

def local_key_press(e):
    ui.handle_key_press(e)
    input_content = ui.input_content
    update_display(input_content)

keyboard.on_release(ui.handle_key_press, suppress=False)
signal.signal(signal.SIGINT, ui.handle_interrupt)


exit_cleanup = False

try:
    while True:
        needs_display_update = ui.needs_display_update
        input_content = ui.input_content
        display_updating = ui.display_updating
        keypressed = ui.keypressed
        
        threshold = 1
        ct = time.time()
        pt = ui.typing_last_time
        diff = ct - pt
        within_threshold = diff <= threshold
        # print([ct, pt, diff, within_threshold, input_content, keypressed])
        time.sleep(0.05)
        
        if exit_cleanup:
            break
                
        if needs_display_update and not display_updating:
            print('path1')
            text = input_content
            update_display(text)
            ui.needs_display_update=False
            ui.typing_last_time = time.time()
            
        if keypressed:
            print('path2')
            text = input_content
            update_display(text)
            ui.keypressed = False

        #time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs

        
except KeyboardInterrupt:
    pass


