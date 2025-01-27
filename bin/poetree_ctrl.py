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
        
    def shutdown(self):
        pass