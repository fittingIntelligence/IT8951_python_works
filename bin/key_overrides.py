import keyboard
import time
import os
import keymaps

class keyboard_overrides:
    def __init__(self):
        self.shift_active = False
        self.control_active = False
        self.capslock_active = False
        self.cursor_position = 0
        self.needs_input_update = False
        self.chars_per_line = 100
        self.needs_display_update = False
        self.input_content = ''
        self.prev_content  = ''
        self.display_updating = False
        self.keypressed = False
        self.v_clear_display = False
        self.input_catchup = False
        self.cursor_index = 0
        
        
    def insert_character(self, character):
        cursor_index = self.cursor_position
        
        if self.cursor_index <= len(self.input_content):
            input_content = input_content[:cursor_index] + character + input_content[cursor_index:]
            self.cursor_position += 1  
        self.needs_input_update = True

    def delete_character(self):
        cursor_index = self.cursor_position
        
        if cursor_index > 0:
            self.input_content = self.input_content[:cursor_index - 1] + self.input_content[cursor_index:]
            self.cursor_position -= 1  
            self.needs_input_update = True

    def handle_key_down(self, e): #keys being held, ie modifier keys
        if e.name == 'shift':
            self.shift_active = True
        if e.name == 'ctrl': 
            self.control_active = True

    def handle_key_press(self, e):
        print(f'key pressed {e}')
        print(e.name)
        if e.name == "backspace":
            self.delete_character()
            needs_input_update = True
            input_catchup = True

        elif e.name == 'caps lock': 
            self.capslock_active = True if self.capslock_active == False else False
            print('caps lock')

                
        elif e.name == "space": #space bar
            self.insert_character(" ")
            
            # Check if adding the character exceeds the line length limit
            if cursor_position > self.chars_per_line:
                self.previous_lines.append(input_content)                
                input_content = ""
                needs_display_update = True
            # Update cursor_position to the length of the remaining input_content
            cursor_position = len(input_content)
            
            needs_input_update = True
            input_catchup = True
        
        elif e.name == "enter":
            if scrollindex>1:
                #if you were reviewing text, jump to scrollindex=1
                scrollindex = 1
                update_display()
            else:
                # Add the input to the previous_lines array
                previous_lines.append(input_content)
                input_content = "" #clears input content
                cursor_position=0
                #save the file when enter is pressed
                save_previous_lines(file_path, previous_lines)
                needs_display_update = True
                input_catchup = True
            
        if e.name == 'ctrl': #if control is released
            self.control_active = False 

        if e.name == 'shift': #if shift is released
            self.shift_active = False
            

        elif len(e.name) == 1 and self.control_active == False:  # letter and number input
            
            if self.shift_active:
                char = keymaps.shift_mapping.get(e.name)
                self.input_content += char
            elif self.capslock_active:
                char = keymaps.shift_mapping.get(e.name)
                self.input_content += char
                
            else:
                self.input_content += e.name
                
            self.cursor_position += 1
            self.needs_input_update = True

            # Check if adding the character exceeds the line length limit
            if self.cursor_position > self.chars_per_line:
                # Find the last space character before the line length limit
                last_space = self.input_content.rfind(' ', 0, self.chars_per_line)
                sentence = self.input_content[:last_space]
                # Append the sentence to the previous lines
                self.previous_lines.append(sentence)                

                # Update input_content to contain the remaining characters
                self.input_content = self.input_content[last_space + 1:]
                needs_display_update=True
                
            # Update cursor_position to the length of the remaining input_content
            self.cursor_position = len(self.input_content)                

        self.typing_last_time = time.time()
        self.input_catchup==True
        self.needs_input_update = True
        self.keypressed=True

            
    def handle_interrupt(signal, frame):
        keyboard.unhook_all()
        exit(0)
