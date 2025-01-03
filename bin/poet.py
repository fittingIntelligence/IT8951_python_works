#
# Poet Writer
# Copyright Fitting Intelligence PTY Ltd

from pathlib import Path
import argparse
from eink import eink
from key_overrides import keyboard_overrides
import file_operations
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
# ui_control.display_image_8bpp()
# ui_control.print_system_info()

ui_control.partial_update_msg('...','')
# ui_control.backspace(0, 0, 'XXXxx', 'XXXxxXXX')
# ui_control.backspace(0, 0, 'XXX', 'XXXxxXXX')
# ui_control.sys_msg(ui_control.system_info,'')


ls = file_operations.loadscreen()
ko = keyboard_overrides()

keyboard.on_press(ko.handle_key_down, suppress=False) #handles modifiers and shortcuts
keyboard.on_release(ko.handle_key_press, suppress=True)
signal.signal(signal.SIGINT, ko.handle_interrupt)

exit_cleanup = False
input_content = ''

try:
    while True:
        needs_display_update = ko.needs_display_update
        prev_content, input_content = input_content, ko.input_content
        display_updating = ko.display_updating
        keypressed = ko.keypressed
        v_clear_display = ko.v_clear_display
        current_window = ko.window
        
        content_changed = prev_content != input_content
        content_smaller = len(input_content) < len(prev_content)
        
        threshold = 1
        
        if exit_cleanup:
            break
        
        if current_window == ['loadscreen','open']:
            ui_control.clear_display()
            ui_control.partial_update_msg('load screen activated','')
            ls.list_files()
            ls.display_items()
            ui_control.partial_update_msg( '\n' + '\n'.join(ls.selectedItemList)  ,'')
            ko.window = ['loadscreen','wait']

        if current_window == ['loadscreen','down']:
            ui_control.clear_display()
            ui_control.partial_update_msg('load screen activated','')
            ls.move_down()
            ls.display_items()
            ui_control.partial_update_msg( '\n' + '\n'.join(ls.selectedItemList)  ,'')
            ko.window = ['loadscreen','wait']
            
        if current_window == ['loadscreen','up']:
            ui_control.clear_display()
            ui_control.partial_update_msg('load screen activated','')
            ls.move_up()
            ls.display_items()
            ui_control.partial_update_msg( '\n' + '\n'.join(ls.selectedItemList)  ,'')
            ko.window = ['loadscreen','wait']
                
        if needs_display_update and not display_updating:
            print('path1')
            ui_control.partial_update_msg(input_content, prev_content)         
            
        if v_clear_display or content_smaller:
            print ('content smaller')
            ui_control.backspace(0, 0, input_content, prev_content)

        elif content_changed:
            print('path2')
            update_dtl = (input_content, prev_content)
            
            ui_control.partial_update_msg(input_content, prev_content)
            ko.keypressed = False
            print(update_dtl)

        #time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs

        
except KeyboardInterrupt:
    pass
