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
ui_control.display_image_8bpp()
ui_control.print_system_info()

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
current_window = ''


# def split_string(text, chars_per_row=80):
#     return '\n'.join(text[i:i+chars_per_row] for i in range(0, len(text), chars_per_row))


# def sampletext():
#     lipsum = '''
# Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque malesuada mauris a leo fringilla,  eu tristique justo porttitor. Donec rutrum mattis mauris a molestie. Proin condimentum rutrum accumsan. 

# Etiam condimentum tellus magna, nec interdum nunc pellentesque ac. Sed sit amet massa ipsum. In a semper lectus. Vestibulum vitae sodales tellus, sit amet aliquam diam. Suspendisse sit amet ipsum vel tortor auctor dictum. Donec ipsum dui, sodales vitae luctus vitae, varius quis purus. Cras pulvinar orci sit met neque volutpat pharetra. 

# Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
#     '''
#     result = split_string(lipsum)
#     ui_control.clear_display()
#     ui_control.partial_update_msg( result  ,'')

# sampletext()


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
        
        threshold = 1
        
        if exit_cleanup:
            break
        
        if prev_window != current_window:
            print(current_window)
        
        if current_window == ['loadscreen','open']:
            ui_control.clear_display()
            ls.list_files()
            ls.display_items()
            ui_control.partial_update_msg( '\n'.join(ls.selectedItemList)  ,'')
            ui_control.partial_update_msg( '\n' * ls.position +  '|'  ,'')
            ko.window = ['loadscreen','wait']

        if current_window == ['loadscreen','down'] :
            ls.move_down()
            ui_control.clear_coords(100, 100 + (ls.prev_position * ui_control.font_height_per_line), 110, 600)
            ui_control.fill_coords( 100, 100 + (ls.prev_position * ui_control.font_height_per_line), 110,100 + (ls.position * ui_control.font_height_per_line))
            
            # ui_control.partial_update_msg( '\n' * ls.position +  '|'  ,'')
            ko.window = ['loadscreen','wait']
            
        if current_window == ['loadscreen','up']:
            ls.move_up()
            ui_control.clear_coords(100, 100 + (ls.prev_position * ui_control.font_height_per_line), 110, 600)
            ui_control.fill_coords( 100, 100 + (ls.prev_position * ui_control.font_height_per_line), 110,100 + (ls.position * ui_control.font_height_per_line))
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
