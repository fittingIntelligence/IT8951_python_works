# functions defined in this file
__all__ = [
    'print_system_info',
    'clear_display',
    'display_image_8bpp',
    'partial_update',
    'partial_update_msg'
]

from PIL import Image, ImageDraw, ImageFont

from sys import path
path += ['../../']
from IT8951 import constants

def print_system_info(display):
    epd = display.epd
    
    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()

def clear_display(display):
    print('Clearing display...')
    display.clear()

def display_image_8bpp(display, img_path='images/poetpre.png'):
    print('Displaying "{}"...'.format(img_path))
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    img = Image.open(img_path)
    
    # TODO: this should be built-in
    dims = (display.width, display.height)

    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)
    display.draw_full(constants.DisplayModes.GC16)

def partial_update(display):
    print('Starting partial update...')

    # clear image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    print('  writing full...')
    _place_text(display.frame_buf, 'partial', x_offset=-display.width//4)
    display.draw_full(constants.DisplayModes.GC16)

    # TODO: should use 1bpp for partial text update
    print('  writing partial...')
    _place_text(display.frame_buf, 'update', x_offset=+display.width//4)
    display.draw_partial(constants.DisplayModes.DU)
    
def partial_update_msg(display, updatetext):
    # TODO: should use 1bpp for partial text update
    print('  writing partial...')
    _place_text(display.frame_buf, updatetext, x_offset=0, y_offset=10)
    display.draw_partial(constants.DisplayModes.DU)
    

# this function is just a helper for the others
def _place_text(img, text, x_offset=0, y_offset=0):
    '''
    Put some centered text at a location on the image.
    '''
    fontsize = 40

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)
    except OSError:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)

    img_width, img_height = img.size
    text_width = font.getlength(text)
    text_height = fontsize

    draw_x = 100+x_offset
    draw_y = 100+y_offset

    draw.text((draw_x, draw_y), text, font=font)
