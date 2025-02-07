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
        print('key down')
        key_mod = e.name

        if e.name == 'shift':
            self.shift_active = True
        if e.name == 'ctrl': 
            self.control_active = True
        if self.shift_active or self.capslock_active:
            key_mod = keymaps.shift_mapping.get(e.name)
        
        if key_mod not in (['shift','ctrl']):
            return key_mod
            

    def handle_key_press(self,e):
        print('key up')
        if e.name == 'shift':
            self.shift_active = False
        if e.name == 'ctrl': 
            self.control_active = False


            
    def handle_interrupt(signal, frame):
        keyboard.unhook_all()
        exit(0)
