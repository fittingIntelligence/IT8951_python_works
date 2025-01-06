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
from datetime import datetime

# Get current datetime in ISO 8601 format
startup_datetime = datetime.now().isoformat()

ui_backgrounds = {
    'splash' : 'images/poetpre.png',
    'ls'     : 'images/load_screen.png',
    'gs'     : 'images/generic_window.png',
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
current_screen='home'
current_file='file_001.txt'

print('Initializing EPD...')
ui_control = eink(current_screen, current_file, args)
epd = ui_control.display.epd
print('VCOM set to', epd.get_vcom())

ui_control.clear_display()
ui_control.display_image_8bpp()
ui_control.print_system_info()

ui_control.partial_update_msg('...','..')
ui_control.sys_msg(ui_control.system_info,'')


ls = file_operations.loadscreen()
ko = keyboard_overrides()

keyboard.on_press(ko.handle_key_down, suppress=False) #handles modifiers and shortcuts
keyboard.on_release(ko.handle_key_press, suppress=True)
signal.signal(signal.SIGINT, ko.handle_interrupt)

exit_cleanup = False
input_content = ''
current_window = ''


def selection_visual():
    line = ls.position + 1
    font_height = ui_control.font_height_per_line -4
    left   = 80
    top    = 110 + (line * font_height)
    right  = 90
    bottom = 110 + (line + 1 )* font_height
    return [left, top, right, bottom]

def clear_window_content():
    left   = 80
    top    = 100
    right  = 1772
    bottom = 1304
    ui_control.clear_coords(left, top, right, bottom)
  

try:
    while True:
        needs_display_update = ko.needs_display_update
        prev_content, input_content = input_content, ko.input_content
        display_updating = ko.display_updating
        keypressed = ko.keypressed
        v_clear_display = ko.v_clear_display
        
        
        prev_window, current_window = current_window, ko.window
                
        content_changed = prev_content != input_content
        content_smaller = len(input_content) < len(prev_content)
        
        if content_changed:
            print ([input_content, ui_control.font])       
        
        threshold = 1
        
        if exit_cleanup:
            break
        
        if prev_window != current_window:
            print(current_window)
        
        if current_window[0] == 'loadscreen':
            if current_window[1] == 'open':
                ui_control.display_image_8bpp(ui_backgrounds['ls'])
                ls.list_files()
                ls.display_items()
                left, top, right, bottom = selection_visual()
                ui_control.partial_update_msg( '\n'.join(ls.selectedItemList)  ,'')
                ui_control.fill_coords(left , top, right, bottom)
                ko.window = ['loadscreen','wait']
                
            elif current_window[1] == 'down' :
                ls.move_down()
                left, top, right, bottom = selection_visual()
                ui_control.clear_coords(80, 100, 90, 600)
                ui_control.fill_coords(left , top, right, bottom)
                ko.window = ['loadscreen','wait']
                
            elif current_window[1] == 'up':
                ls.move_up()
                left, top, right, bottom = selection_visual()
                ui_control.clear_coords(80, 100, 90, 600)
                ui_control.fill_coords(left , top, right, bottom)            
                ko.window = ['loadscreen','wait']
                
            elif current_window[1] == 'selectItem' and ls.selected:
                print('Selecting item')
                ls.select_item()
                ls.position = 0
                clear_window_content()
                left, top, right, bottom = selection_visual()
                ui_control.partial_update_msg( '\n'.join(ls.selectedItemList)  ,'')
                ui_control.fill_coords(left , top, right, bottom)
                ko.window = ['loadscreen','wait']
                
            elif ls.selected==False and current_window[1] == 'selectItem':
                input_content = ls.current_file_contents
                ui_control.display_image_8bpp(ui_backgrounds['gs'])
                ui_control.partial_update_msg(input_content,'')
                ko.window = ['write','ready']
                
            
        elif current_window == ['write','open']:
            # ui_control.clear_display()
            ui_control.display_image_8bpp(ui_backgrounds['gs'])
            ui_control.write_text(1500, 10, startup_datetime, 12, 0, 0, 1800, 1400)
            ui_control.partial_update_msg('...','..')
            ko.window = ['write','ready']
                
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
