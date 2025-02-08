# from collections import deque

class poetree:
    def __init__(self, ui, kb, win, io):
        self.ui  = ui
        self.kb  = kb
        self.win = win
        self.io  = io
        
        self.cur_screen = None
        self.content = ''
        self.unwritten_content = []
        
    def partial_update_msg(self, a,b):
        self.ui.partial_update_msg(a,b)
        self.content = ''.join([b,a])
        self.unwritten_content = ''
        
    def get_unwritten(self):
        return [''.join(self.unwritten_content), len(self.unwritten_content)]

    def partial_update_msg_1(self):
        unwritten_content, unwritten_len = self.get_unwritten()
        written_content = self.content        
        self.ui.partial_update_msg(unwritten_content,written_content)
        self.content = ''.join([written_content,unwritten_content])
        self.unwritten_content = self.unwritten_content[unwritten_len:]

    def clear_screen(self):
        self.ui.clear_display()
        
    def key_up_watcher(self,e):
        key_pressed = self.kb.handle_key_up(e)
        if key_pressed:
            print(key_pressed)
        
    def update_content_stream(self,e):
        self.unwritten_content.append(e)
    
    def key_down_watcher(self,e):
        key_pressed = self.kb.handle_key_down(e)
        if key_pressed:
            print(key_pressed)
            if key_pressed == 'caps lock':
                self.clear_screen()
                self.content=''
                
            elif key_pressed == '~':
                print(self.content)

            else: 
                self.update_content_stream(key_pressed)
            
        
        
    def shutdown(self):
        pass