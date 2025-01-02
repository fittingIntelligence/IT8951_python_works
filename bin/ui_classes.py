from datetime import datetime

class Window:
    def __init__(self, width, height, title, x_position, y_position, bg_image=None):
        self.width = width
        self.height = height
        self.title = title
        self.x_position = x_position
        self.y_position = y_position
        self.content = ""
        self.prev_content = ""
        self.cursor_position = 0
        self.word_count = 0
        self.last_updated = datetime.now()
        self.bg_image = bg_image
    def update_content(self, new_content):
        self.prev_content = self.content
        self.content = new_content
        self.word_count = len(new_content.split())
        self.last_updated = datetime.now()
    def move_cursor(self, new_position):
        if 0 <= new_position <= len(self.content):
            self.cursor_position = new_position
    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
    def move(self, new_x, new_y):
        self.x_position = new_x
        self.y_position = new_y
    def set_bg_image(self, image_path):
        self.bg_image = image_path
    def __str__(self):
        return f"Window: {self.title} ({self.width}x{self.height}) at ({self.x_position}, {self.y_position})"
    
class Stack:
    def __init__(self, current_screen = '', current_file =None):
        self.current_screen = current_screen
        self.current_file = current_file
    def __str__(self):
        return f"Stack: {self.current_screen} - {self.current_file}"

class ObjectSelector:
    def __init__(self, itemlist):
        self.itemlist = itemlist
        self.position = 0
    def display_items(self):
        for index, item in enumerate(self.itemlist):
            if index == self.position:
                print(f"> {item}")
            else:
                print(f"  {item}")
    def move_up(self):
        if self.position > 0:
            self.position -= 1
    def move_down(self):
        if self.position < len(self.itemlist) - 1:
            self.position += 1


class Content:
    def __init__(self, width, height, x_position, y_position):
        self.width = width
        self.height=height
        self.x_position = x_position
        self.y_position = y_position
        self.v_scroll_idx = 0
        self.v_scroll_max = 20
        self.v_jump_at_rows_on_screen = 17
        self.v_rows_on_screen = 0
        self.content = ''
        self.prev_content = ''
        self.full_content_array = []
        self.cursor_x = 0
        self.cursor_y = 0
        
    def update_content(self, new_content):
        self.prev_content = self.content
        self.content = new_content
        self.full_content_array = new_content.split('\n')
        self.word_count = len(new_content.split())
        self.last_updated = datetime.now()
        
        

        
    def __str__(self):
        return f"Content"




# metadata = Stack('home', None)
loadWindow = Window(800,600,'Load a file', 0, 0)

file_list = ['file1.txt','file2.txt','file3.txt']

load_selector = ObjectSelector(file_list)

load_selector.display_items()
load_selector.move_down()
load_selector.display_items()
load_selector.move_down()
load_selector.display_items()
load_selector.move_up()
load_selector.display_items()
