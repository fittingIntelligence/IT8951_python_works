from PIL import Image, ImageDraw, ImageFont
from sys import path
path += ['../../']
from IT8951 import constants
from IT8951.display import AutoEPDDisplay

# class screens:
#     def __init__(self, top, left, bottom, right, background):
        
#         self.cursor_x = 0
#         self.cursor_y = 0
#         self.top = top
#         self.left = left
#         self.bottom = bottom
#         self.right = right
#         self.background = background

# class ein:
#     def __init__(self):
#         self.screens = {
#             'splash': screens(0,0,100,100,'images/poetpre.png'),
#             'write': screens(0,0,100,100,'images/generic_window.png'),
#             'load': screens(0,0,100,100,'images/generic_window.png'),
#             'save': screens(0,0,100,100,'images/generic_window.png'),
#             'off': screens(0,0,100,100,'images/shutdown.png'),
#         }
    

class eink:
    def __init__(self, args):
        self.display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=args.mirror, spi_hz=24000000)
        self.epd = self.display.epd        
        args.rotate='flip'
        self.fontsize=30
        self.font = self.set_font_size(self.fontsize)
        self.font_height_per_line = sum(self.font.getmetrics())
        
    def print_system_info(self):
        epd = self.display.epd
        system_info = f"""
        System info:
            display size: {epd.width}x{epd.height}
            img buffer address: {epd.img_buf_address}
            firmware version: {epd.firmware_version}
            LUT version: {epd.lut_version}
            Font Metrics: {self.font.getmetrics()}
            Font Name: {self.font.getname()}
            
        """
        self.system_info = system_info
        print(self.system_info)

    def clear_display(self):
        print('Clearing display...')
        self.display.clear()
        
    def set_font_size(self, fontsize):
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf', fontsize)
            return font
        except OSError:
            print ('Font error, falling back')
            font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)
            return font
        
    def display_image_8bpp(self, img_path='images/poetpre.png'):
        print('Displaying "{}"...'.format(img_path))
        display = self.display
        display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
        img = Image.open(img_path)
        dims = (display.width, display.height)
        img.thumbnail(dims)
        paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
        display.frame_buf.paste(img, paste_coords)
        display.draw_full(constants.DisplayModes.GC16)
        
    def _place_text(self, text, oldtext, x_offset=0, y_offset=0):
        img = self.display.frame_buf
        draw = ImageDraw.Draw(img)
        text_width = self.font.getlength(oldtext)
        draw_x = 100+x_offset + text_width
        draw_y = 100+y_offset + self.fontsize
        newtext = text.replace(oldtext, '')
        draw.text((draw_x, draw_y), newtext, font=self.font)
        
    def _place_text_coords(self, text, x, y):
        img = self.display.frame_buf
        draw = ImageDraw.Draw(img)
        draw_x = x
        draw_y = y
        draw.text((draw_x, draw_y), text, font=self.font)


    def backspace(self, draw_x, draw_y, text, oldtext):
        text_width_to_blank = int(self.font.getlength(oldtext))
        text_width = self.font.getlength(text)
        draw_x = int(100 + text_width)
        draw_y = int(100 + self.fontsize)
        box=(draw_x, draw_y, draw_x + text_width_to_blank, draw_y + (self.fontsize *2))
        print (box)
        self.display.frame_buf.paste(0xFF, box=box)
        self.display.draw_partial(constants.DisplayModes.DU)
        
    def clear_coords(self, left, top, right, bottom):
            box=(left, top, right, bottom)
            self.display.frame_buf.paste(0xFF, box=box)
            self.display.draw_partial(constants.DisplayModes.DU)
            
    def fill_coords(self, left, top, right, bottom):
            box=(left, top, right, bottom)
            self.display.frame_buf.paste(0x00, box=box)
            self.display.draw_partial(constants.DisplayModes.DU)
            
    def write_text(self, x, y, text, fontsize, left, top, right, bottom):
        try:
            prev_fontsize = self.fontsize
            self.font = self.set_font_size(fontsize)
            self._place_text_coords(text, x, y)
            self.display.draw_partial(constants.DisplayModes.DU)
            self.font = self.set_font_size(prev_fontsize)
            
        except:
            print(f'''failed _place_text_coords
                    {text}
                    {x}
                    {y}
                  ''')
        
        
    def partial_update_msg(self, updatetext, oldtext):
        print('  writing partial...')
        try:
            self._place_text(updatetext, oldtext, x_offset=0, y_offset=10)
            self.display.draw_partial(constants.DisplayModes.DU)
        except:
            print('failed Partial update msg')
        
    def sys_msg(self, updatetext, oldtext):
        print('  writing sys_msg...')
        try:
            self._place_text( updatetext, oldtext, x_offset=500, y_offset=900)
            self.display.draw_partial(constants.DisplayModes.DU)
        except:
            print('failed sys_msg')

    def paint_coords(self, color, left, top, right, bottom):
            box=(left, top, right, bottom)
            self.display.frame_buf.paste(color, box=box)
            self.display.draw_partial(constants.DisplayModes.GC16)

    def display_gradient(self):
        print('Displaying gradient...')
        for i in range(16):
            color = i*0x10
            box = (
                i*self.display.width//16,      # xmin
                0,                        # ymin
                (i+1)*self.display.width//16,  # xmax
                self.display.height            # ymax
            )

            self.display.frame_buf.paste(color, box=box)
        self.display.draw_full(constants.DisplayModes.GC16)

        # then add some black and white bars on top of it, to test updating with DU on top of GC16
        box = (0, self.display.height//5, self.display.width, 2*self.display.height//5)
        self.display.frame_buf.paste(0x00, box=box)

        box = (0, 3*self.display.height//5, self.display.width, 4*self.display.height//5)
        self.display.frame_buf.paste(0xF0, box=box)

        self.display.draw_partial(constants.DisplayModes.DU)


    def __str__(self):
        return f"Stack: {self.current_screen} - {self.current_file}"
    