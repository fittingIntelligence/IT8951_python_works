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
        
        self.startuptime = datetime.now().isoformat()
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
                                '<activate writer screen>',
                                ]):
                if key_pressed == 'caps lock':
                    self.clear_screen()
                    self.content=''
                    
                elif key_pressed == '<activate shutdown>':
                    self.shutdown()
                
                elif key_pressed == '<activate file load screen>':
                    self.loadscreen()
                    
                elif key_pressed == '<activate writer screen>':
                    self.writerscreen()
                    
                elif self.cur_screen=='loadscreen':
                        
                    if key_pressed == 'down':
                        self.io.move_down()
                        left, top, right, bottom = self.selection_visual()
                        self.ui.clear_coords(80, 100, 90, 600)
                        self.ui.fill_coords(left , top, right, bottom)
                                    
                    elif key_pressed == 'up': 
                        self.io.move_up()
                        left, top, right, bottom = self.selection_visual()
                        self.ui.clear_coords(80, 100, 90, 600)
                        self.ui.fill_coords(left , top, right, bottom)            
                        
                    elif key_pressed == "enter":
                        print('Selecting item')
                        self.io.select_item()
                        self.io.position = 0
                        left, top, right, bottom = self.selection_visual()
                        self.ui.partial_update_msg( '\n'.join(self.io.selectedItemList)  ,'')
                        self.ui.fill_coords(left , top, right, bottom)                        
                        
                        # input_content = self.io.current_file_contents
                        # self.ui.display_image_8bpp(self.backgrounds['gs'])
                        # self.ui.write_text(80, 40, self.io.cleanPath, 30, 0, 0, 1800, 1400)
                        # self.ui.write_text(100, 100, input_content, 30, 0, 0, 1800, 1400)
                        # ko.window = ['write','ready']


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
        line = self.io.position + 1
        font_height = self.ui.font_height_per_line -4
        left   = 80
        top    = 110 + (line * font_height)
        right  = 90
        bottom = 110 + (line + 1 )* font_height
        return [left, top, right, bottom]
        
    def loadscreen(self):
        self.ui.display_image_8bpp(self.backgrounds['gs'])
        self.ui.write_text(80, 40, 'Load a file', 30, 0, 0, 1800, 1400)
        self.io.list_files()
        self.io.display_items()
        left, top, right, bottom = self.selection_visual()
        self.ui.partial_update_msg( '\n'.join(self.io.selectedItemList)  ,'')
        self.ui.fill_coords(left , top, right, bottom)
        self.cur_screen = 'loadscreen'

    def writerscreen(self):
        self.ui.display_image_8bpp(self.backgrounds['gs'])
        self.ui.write_text(80, 40, 'Writing Screen', 30, 0, 0, 1800, 1400)
        self.ui.write_text(1000, 1360, f'System started {self.startuptime}', 24, 0, 0, 1800, 1400)
        self.unwritten_content = self.content.split('|')
        self.content=''
        self.partial_update_msg_1()
        self.cur_screen = 'writerscreen'
        