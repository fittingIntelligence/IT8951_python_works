import keyboard
import time
import keymaps


class keyboard_overrides:
    def __init__(self):
        self.shift_active = False
        self.control_active = False
        self.capslock_active = False
        
    def insert_character(self, character):        
        if self.cursor_index <= len(self.input_content):
            self.input_content = self.input_content[:self.cursor_index] + character + self.input_content[self.cursor_index:]
            self.cursor_position += 1  
        self.needs_input_update = True

    def delete_character(self):
        cursor_index = self.cursor_position
        
        if cursor_index > 0:
            self.input_content = self.input_content[:cursor_index - 1] + self.input_content[cursor_index:]
            self.cursor_position -= 1  
            self.needs_input_update = True

    def handle_key_down(self, e): 
        if e.name == 'shift':
            self.shift_active = True
        elif e.name == 'ctrl': 
            self.control_active = True

    def handle_key_press(self, e):
        print(f'key pressed {e} - line chars: {len(self.input_content)} - screen {self.window}')
        try:
            if self.shift_active:
                return keymaps.shift_mapping.get(e.name)
            elif self.capslock_active:
                return  keymaps.shift_mapping.get(e.name)
            else:
                return e.name
        except Exception as error:
            print(error)

            
    def handle_interrupt(signal, frame):
        keyboard.unhook_all()
        exit(0)
