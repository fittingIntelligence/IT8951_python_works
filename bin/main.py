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
display_image_8bpp(display,'images/poetpre.png')
partial_update_msg(display, text, font)

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
        
        if exit_cleanup:
            break
                
        if ui.needs_display_update and not ui.display_updating:
            text = ui.input_content
            update_display(text)
            ui.needs_display_update=False
            ui.typing_last_time = time.time()
            
        elif (time.time()- ui.typing_last_time)<(.5): #if not doing a full refresh, do partials
            #the screen enters a high refresh mode when there has been keyboard input
            if not ui.updating_input_area and ui.scrollindex==1:
                text = ui.input_content
                print(text)
                # update_display(text)
        #time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs
        else:
            ct = time.time()
            pt = ui.typing_last_time
            diff = ct - pt
            
            print([ct, pt, diff, diff < .5])
            
            time.sleep(0.05)
        
except KeyboardInterrupt:
    pass


