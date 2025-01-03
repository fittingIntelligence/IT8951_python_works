import os

class loadscreen:
    def __init__(self):
        self.bookdir = '/home/zero/git/books'
        self.selected_path = self.bookdir
        self.selected_file = ''
        self.itemlist = []
        self.position = 0
        self.selectedItemList = []
        
    def list_files(self):
        self.itemlist = os.listdir(self.selected_path)
        
    def open(self):
        print('open load screen')
        self.selected = True

    def close(self):
        print('close load screen')
        self.selected = False
        
    def select_file(self):
        print('select file')
           
    def display_items(self):
        self.selectedItemList = []
        for index, item in enumerate(self.itemlist):
            # if index == self.position:
            self.selectedItemList.append(f"> {item}")
            # else:
            self.selectedItemList.append(f"  {item}")
                
    def move_up(self):
        if self.position > 0:
            self.position -= 1
            
    def move_down(self):
        if self.position < len(self.itemlist) - 1:
            self.position += 1
        
        
