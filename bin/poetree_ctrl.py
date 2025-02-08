# from collections import deque
import os
from datetime import datetime

class poetree:
    def __init__(self, ui, kb, win, io, backgrounds):
        self.ui  = ui
        self.kb  = kb
        self.win = win
        self.io  = io
        self.backgrounds = backgrounds
        
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
            if key_pressed in (['caps lock', 'right','down','left','up','~',
                                '<activate file load screen>','<activate file save>','<activate shutdown>',
                                ]):
                if key_pressed == 'caps lock':
                    self.clear_screen()
                    self.content=''
                    
                elif key_pressed == '<activate shutdown>':
                    self.shutdown()
                
                elif key_pressed == '<activate file load screen>':
                    self.loadscreen()

                elif key_pressed == '~':
                    print(self.content)
                    
                else:
                    print(key_pressed)

            else: 
                self.update_content_stream(key_pressed)
            
        
        
    def shutdown(self):
        self.ui.display_image_8bpp(self.backgrounds['sd'])
        self.ui.write_text(80, 40, f'Shutting down  - {datetime.now().isoformat()}', 30, 0, 0, 1800, 1400)

        self.ui.write_text(120, 120, """
                              Custom built for @poetpre (Instagram)
                              2025
                              
                              """, 30, 0, 0, 1800, 1400)
        
        # os.system("sudo shutdown now")

    def selection_visual(self):
        line = self.ls.position + 1
        font_height = self.ui.font_height_per_line -4
        left   = 80
        top    = 110 + (line * font_height)
        right  = 90
        bottom = 110 + (line + 1 )* font_height
        return [left, top, right, bottom]
        
    def loadscreen(self):
        self.ui.display_image_8bpp(self.ui_backgrounds['gs'])
        self.ui.write_text(80, 40, 'Load a file', 30, 0, 0, 1800, 1400)
        self.ls.list_files()
        self.ls.display_items()
        left, top, right, bottom = self.selection_visual()
        self.ui.partial_update_msg( '\n'.join(self.ls.selectedItemList)  ,'')
        self.ui.fill_coords(left , top, right, bottom)
