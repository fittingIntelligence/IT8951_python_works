import keyboard
import time
import keymaps


class keyboard_overrides:
    def __init__(self):
        self.shift_active = False
        self.control_active = False
        self.capslock_active = False
        
    def insert_character(self, character):        
        return('insert')
    def delete_character(self):
        return('delete')
    
    def handle_key_down(self, e): 
        if e.name == 'shift':
            self.shift_active = True
        elif e.name == 'ctrl': 
            self.control_active = True

    def handle_key_press(self):
        print(f'key pressed {self.e}')
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
