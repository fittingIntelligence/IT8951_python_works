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
        self.current_file_contents = ''
        self.selected = False
        self.cleanPath = '/'
        
        
        
    def list_files(self):
        self.itemlist =  sorted(os.listdir(self.selected_path))
        
    def open(self):
        print('open load screen')
        self.selected = True

    def close(self):
        print('close load screen')
        self.selected = False
        
    def select_file(self, selection):
        self.selected_file = selection
        print (f'use {self.selected_file} for writing to')
        self.read_file_whole(self.selected_file)
        self.close()

    def read_file_whole(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                print(content)
                self.current_file_contents = content
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except IOError:
            print(f"Error: There was an issue reading the file '{filename}'.")
        
           
    def display_items(self):
        self.open()
        pwd = self.selected_path.replace(self.booksroot,"")
        if len(pwd) == 0:
            self.selectedItemList = [f'-']
        else:
            self.selectedItemList = [f'.. ({ self.selected_path.replace(self.booksroot,"") })']
        for index, item in enumerate(self.itemlist):
            self.selectedItemList.append(f'  {item}')
                
    def move_up(self):
        if self.position > 0:
            self.prev_position = self.position
            self.position -= 1
            
    def move_down(self):
        if self.position < len(self.selectedItemList) - 1:
            self.prev_position = self.position            
            self.position += 1
            
    def select_item(self):
        print('Attempting selction')
        if self.position == 0 and self.selected_path != self.booksroot:
            selection = f'{ "/".join( self.selected_path.split("/")[:-1] ) }'
            
        elif self.selectedItemList[self.position] != '..':
            selection = f'{self.selected_path}/{self.selectedItemList[self.position].strip()}'
        
        else:
            selection = self.selected_path
        
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
            self.cleanPath = selection.replace(self.booksroot,'')
            self.list_files()
            self.display_items()
            
        elif is_file:
            self.select_file(selection)

