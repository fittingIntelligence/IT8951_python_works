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
        fontsize=36
        self.font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)
        
    def display_image_8bpp(display, img_path='images/poetpre.png'):
        print('Displaying "{}"...'.format(img_path))
        display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
        img = Image.open(img_path)
        dims = (display.width, display.height)
        img.thumbnail(dims)
        paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
        display.frame_buf.paste(img, paste_coords)
        display.draw_full(constants.DisplayModes.GC16)

    def __str__(self):
        return f"Stack: {self.current_screen} - {self.current_file}"       
