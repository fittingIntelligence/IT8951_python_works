# functions defined in this file
__all__ = [
    'handle_key_press',
]

import keyboard
import signal

def handle_key_press(e):
    global cursor_position
    global typing_last_time
    global display_start_line
    global needs_display_update
    global needs_input_update
    global shift_active
    global exit_cleanup
    global input_content
    global previous_lines
    global display_updating
    global input_catchup
    global control_active
    global console_message
    global scrollindex
    
    #save via ctrl + s
    if e.name== "s" and control_active:
        timestamp = time.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename = os.path.join(os.path.dirname(__file__), 'data', f'zw_{timestamp}.txt')
        save_previous_lines(filename, previous_lines)
        
        console_message = f"[Saved]"
        update_display()
        time.sleep(1)
        console_message = ""
        update_display()

    #new file (clear) via ctrl + n
    if e.name== "n" and control_active: #ctrl+n
        #save the cache first
        timestamp = time.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename = os.path.join(os.path.dirname(__file__), 'data', f'zw_{timestamp}.txt')
        save_previous_lines(filename, previous_lines)
        
        #create a blank doc
        previous_lines.clear()
        input_content = ""

        console_message = f"[New]"
        update_display()
        time.sleep(1)
        console_message = ""
        update_display()

    if e.name== "down" or e.name== "right":
       #move scrollindex down
       scrollindex = scrollindex - 1
       if scrollindex < 1:
            scrollindex = 1
       #--
       console_message = (f'[{round(len(previous_lines)/lines_on_screen)-scrollindex+1}/{round(len(previous_lines)/lines_on_screen)}]')
       update_display()
       console_message = ""

    if e.name== "up" or e.name== "left":
       #move scrollindex up
       scrollindex = scrollindex + 1
       if scrollindex > round(len(previous_lines)/lines_on_screen+1):
            scrollindex = round(len(previous_lines)/lines_on_screen+1)
       #--
       console_message = (f'[{round(len(previous_lines)/lines_on_screen)-scrollindex+1}/{round(len(previous_lines)/lines_on_screen)}]')
       update_display()
       console_message = ""

    #powerdown - could add an autosleep if you want to save battery
    if e.name == "esc" and control_active: #ctrl+esc
        #run powerdown script
        display_draw.rectangle((0, 0, 400, 300), fill=255)  # Clear display
        display_draw.text((55, 150), "ZeroWriter Powered Down.", font=font24, fill=0)
        partial_buffer = epd.getbuffer(display_image)
        epd.display(partial_buffer)
        time.sleep(3)
        subprocess.run(['sudo', 'poweroff', '-f'])
        
        needs_display_update = True
        needs_input_update = True
        input_catchup = True
        
        
    if e.name == "tab": 
        #just using two spaces for tab, kind of cheating, whatever.
        insert_character(" ")
        insert_character(" ")
        
        # Check if adding the character exceeds the line length limit
        if cursor_position > chars_per_line:
            previous_lines.append(input_content)                
            # Update input_content to contain the remaining characters
            input_content = ""
            needs_display_update = True #trigger a display refresh
        # Update cursor_position to the length of the remaining input_content
        cursor_position = len(input_content)
        
        needs_input_update = True
        input_catchup = True
        
    if e.name == "backspace":
        delete_character()
        needs_input_update = True
        input_catchup = True
            
    elif e.name == "space": #space bar
        insert_character(" ")
        
        # Check if adding the character exceeds the line length limit
        if cursor_position > chars_per_line:
            previous_lines.append(input_content)                
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
        control_active = False 

    if e.name == 'shift': #if shift is released
        shift_active = False

    elif len(e.name) == 1 and control_active == False:  # letter and number input
        
        if shift_active:
            char = keymaps.shift_mapping.get(e.name)
            input_content += char
        else:
            input_content += e.name
            
        cursor_position += 1
        needs_input_update = True

        # Check if adding the character exceeds the line length limit
        if cursor_position > chars_per_line:
            # Find the last space character before the line length limit
            last_space = input_content.rfind(' ', 0, chars_per_line)
            sentence = input_content[:last_space]
            # Append the sentence to the previous lines
            previous_lines.append(sentence)                

            # Update input_content to contain the remaining characters
            input_content = input_content[last_space + 1:]
            needs_display_update=True
            
        # Update cursor_position to the length of the remaining input_content
        cursor_position = len(input_content)                

    typing_last_time = time.time()
    input_catchup==True
    needs_input_update = True
    
def handle_interrupt(signal, frame):
    keyboard.unhook_all()
    # epd.init()
    # epd.Clear()
    exit(0)

#Startup Stuff ---
# keyboard.on_press(handle_key_down, suppress=False) #handles modifiers and shortcuts
keyboard.on_release(handle_key_press, suppress=True)
signal.signal(signal.SIGINT, handle_interrupt)