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

    def handle_key_press(self,e):
        print(f'key pressed {e}')
        keys_pressed = []
        key_mod = e.name
        try:
            if self.shift_active or self.capslock_active:
                key_mod = keymaps.shift_mapping.get(e.name)

            return key_mod
                
        except Exception as error:
            print(error)

            
    def handle_interrupt(signal, frame):
        keyboard.unhook_all()
        exit(0)
