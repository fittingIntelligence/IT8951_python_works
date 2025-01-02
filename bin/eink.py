from PIL import Image, ImageDraw, ImageFont
from sys import path
path += ['../../']
from IT8951 import constants
from IT8951.display import AutoEPDDisplay


class eink:
    def __init__(self, current_screen, current_file, args):
        self.display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=args.mirror, spi_hz=24000000)
        self.epd = self.display.epd        
        self.current_screen = current_screen
        self.current_file = current_file
        args.rotate='flip'
        self.fontsize=36
        self.font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', self.fontsize)
        
    def print_system_info(self):
        epd = self.display.epd
        print('System info:')
        print('  display size: {}x{}'.format(epd.width, epd.height))
        print('  img buffer address: {:X}'.format(epd.img_buf_address))
        print('  firmware version: {}'.format(epd.firmware_version))
        print('  LUT version: {}'.format(epd.lut_version))
        print()

    def clear_display(self):
        print('Clearing display...')
        self.display.clear()
        
    def set_font_size(self, fontsize):
        try:
            self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)
        except OSError:
            self.font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)
        
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
        
    def partial_update_msg(self, updatetext, oldtext):
        # TODO: should use 1bpp for partial text update
        print('  writing partial...')
        self._place_text(self.display.frame_buf, updatetext, oldtext, self.font, x_offset=0, y_offset=10)
        self.display.draw_partial(constants.DisplayModes.DU)

    def _place_text(self, img, text, oldtext, x_offset=0, y_offset=0):
        draw = ImageDraw.Draw(img)
        text_width = self.font.getlength(oldtext)
        draw_x = 100+x_offset + text_width
        draw_y = 100+y_offset + self.fontsize
        newtext = text.replace(oldtext, '')
        draw.text((draw_x, draw_y), newtext, font=self.font)

    def backspace(self, draw_x, draw_y, text, oldtext, font, display):
        text_width_to_blank = int(font.getlength(oldtext))
        text_width = font.getlength(text)
        draw_x = int(100 + text_width)
        draw_y = int(100 + self.fontsize)
        box=(draw_x, draw_y, draw_x + text_width_to_blank, draw_y + (self.fontsize *2))
        print (box)
        display.frame_buf.paste(0xFF, box=box)
        display.draw_partial(constants.DisplayModes.DU)

    def __str__(self):
        return f"Stack: {self.current_screen} - {self.current_file}"       
