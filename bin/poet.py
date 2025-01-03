#
# Poet Writer
# Copyright Fitting Intelligence PTY Ltd

from pathlib import Path
import argparse
from eink import eink
import keyboard
import signal


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

ui_control.clear_display()
ui_control.display_image_8bpp()
ui_control.print_system_info()

ui_control.partial_update_msg('XXXxxXXX','')
ui_control.backspace(0, 0, 'XXXxx', 'XXXxxXXX')
ui_control.backspace(0, 0, 'XXX', 'XXXxxXXX')
ui_control.sys_msg('System message', '')

# keyboard.on_press(ui.handle_key_down, suppress=False) #handles modifiers and shortcuts
# keyboard.on_release(ui.handle_key_press, suppress=True)
# signal.signal(signal.SIGINT, ui.handle_interrupt)


# exit_cleanup = False

# try:
#     while True:
#         needs_display_update = ui.needs_display_update
#         prev_content, input_content = input_content, ui.input_content
#         display_updating = ui.display_updating
#         keypressed = ui.keypressed
#         v_clear_display = ui.v_clear_display
        
#         content_changed = prev_content != input_content
#         content_smaller = len(input_content) < len(prev_content)
        
#         threshold = 1
        
#         if exit_cleanup:
#             break
                
#         if needs_display_update and not display_updating:
#             print('path1')
#             ui_control.partial_update_msg(input_content, prev_content)         
            
#         if v_clear_display or content_smaller:
#             print ('content smaller')
#             ui_control.backspace(0, 0, input_content, prev_content)

#             # partial_update_msg(display, input_content, '', font) 
#             ui.v_clear_display = False
            
#         elif content_changed:
#             print('path2')
#             update_dtl = (display, input_content, prev_content)
            
#             ui_control.partial_update_msg(input_content, prev_content)
#             ui.keypressed = False
#             print(update_dtl)
            
        

#         #time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs

        
# except KeyboardInterrupt:
#     pass
