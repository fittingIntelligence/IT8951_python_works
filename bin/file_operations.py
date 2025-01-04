import os

class loadscreen:
    def __init__(self):
        self.booksroot = '/home/zero/git/books'
        self.selected_path = self.booksroot
        self.selected_file = ''
        self.itemlist = []
        self.position = 0
        self.prev_position = 0
        self.selectedItemList = []
        
    def list_files(self):
        self.itemlist = sorted(os.listdir(self.selected_path))
        
    def open(self):
        print('open load screen')
        self.selected = True

    def close(self):
        print('close load screen')
        self.selected = False
        
    def select_file(self):
        print('select file')
           
    def display_items(self):
        self.selectedItemList = ['..']
        for index, item in enumerate(self.itemlist):
            # if index == self.position:
            # self.selectedItemList.append(f"> {item}")
            # else:
            self.selectedItemList.append(f'  {item}')
                
    def move_up(self):
        if self.position > 0:
            self.prev_position = self.position
            self.position -= 1
            
    def move_down(self):
        if self.position < len(self.itemlist) - 1:
            self.prev_position = self.position            
            self.position += 1
            
    def select_item(self):
        print('Attempting selction')
        if self.selectedItemList[self.position] == '..':
            selection = f'{ "/".join( self.selected_path.split("/")[:-1] ) }'
            
        else:
            selection = f'{self.selected_path}/{self.selectedItemList[self.position].strip()}'
        
        is_directory = os.path.isdir(selection)
        is_file = os.path.isfile(selection)
        
        print(f'''
              selection {selection}
              is_directory {is_directory}
              is_file {is_file}
              ''')
        
        if is_directory:
            print(f'Changing path to {selection}')

            self.selected_path = selection
            self.list_files()
            self.display_items()

