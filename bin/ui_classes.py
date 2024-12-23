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
        self.current_screen = current_screen,
        self.current_file = current_file,
    def __str__(self):
        return f"Stack: {self.current_screen} - {self.current_file}"

metadata = Stack('home', None)

loadWindow = Window(800,600,'Load a file', 0, 0)

fileList = ['file1.txt','file2.txt','file3.txt']

def fileSelection(fileList, position):
    for idx, f in enumerate(fileList):
        if idx == position:
            print(f' - {f} -')
        else:
            print (f)

fileSelection(fileList, 1)