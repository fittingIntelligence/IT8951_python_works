class poetree:
    def __init__(self, ui, kb, win, io):
        self.ui  = ui
        self.kb  = kb
        self.win = win
        self.io  = io
        
        self.cur_screen = None
        self.content = ''
        
    def partial_update_msg(self, a,b):
        self.ui.partial_update_msg(a,b)
        self.content = a
        
    def clear_screen(self):
        self.ui.clear_display()
        
    def key_watcher(self,e):
        key_sequence = self.kb.handle_key_press(self, e)
        self.partial_update_msg(''.join(key_sequence),self.content)
        self.content += key_sequence
    
    def key_down_watcher(self,e):
        print(self.kb.handle_key_down(self, e))
        
    def shutdown(self):
        pass