# functions for interfacing the operations like image grabing, mouse clicking

import win32gui
import mss
from PIL import Image

# constants from measurements of the game
gb_pos = (15, 101)  # relative coordinates of the game board in the game window
gb_margin = 15  # game board margins at bottom corners, both left and right
tile_size = 16  # number of pixels of a tile in x or y direction
face_size = 20  # number of pixels of the face in x or y direction

# constants for the colors
color_white = (255, 255, 255)  # for some boundaries
color_light_grey = (192, 192, 192)  # for most background
color_dark_grey = (128, 128, 128)  # for some boundaries, number 8
color_yellow = (255, 255, 0)  # for the yellow face
color_black = (0, 0, 0)  # for the mines, number 7
color_blue = (0, 0, 255)  # for number 1
color_dark_green = (0, 128, 0)  # for number 2
color_red = (255, 0, 0)  # for number 3, number board
color_dark_blue = (0, 0, 128)  # for number 4
color_dark_red = (128, 0, 0)  # for number 5, number board
color_cyan = (0, 128, 128)  # for number 6

# get the game window information
hwnd = win32gui.FindWindow(None, 'Minesweeper X')  # get window handle
rect = win32gui.GetWindowRect(hwnd)  # get game window positions
# left and top positions of the window, reference coordinates for all
w_pos = (rect[0], rect[1])
w_size = (rect[2]-rect[0], rect[3]-rect[1])  # pixel size of the window
# decide face position in relative coordinates
face_pos = (w_size[0]/2-10, 64)
# prepare face pixel pos for face screenshot
face_pixel_pos = {'left': w_pos[0] + face_pos[0],
                  'top': w_pos[1] + face_pos[1],
                  'width': face_size,
                  'height': face_size}
# the position of the middle of the face for clicking
face_click_pos = (face_pos[0]+face_size/2, face_pos[1]+face_size/2)
# for screenshots
sct = mss.mss()

# get game board size, tiles in x and y directions
def get_board_size():
    # make sure game board size can be calculated from the pixels
    if ((w_size[0]-gb_pos[0]-gb_margin)%tile_size != 0 or
        (w_size[1]-gb_pos[1]-gb_margin)%tile_size != 0):
        print("game board size calculation from pixel size of the window failed")
        return (0, 0)  # act as error
    # calculate game board size, tiles in x and y directions
    gb_size = ((w_size[0]-gb_pos[0]-gb_margin)/tile_size,
               (w_size[1]-gb_pos[1]-gb_margin)/tile_size)    
    return gb_size

# read tile, from possibilities include numbers(1~8), empty, or untouched
# there are other possibilities for the tile like flag, mine, red mine, or red cross mine
# but used together with read_face(), the rest situations can be avoided
# return code: (same as tile definition in 'board' variable)
    # untouched tile: -1
    # empty tile: 0
    # number tile 1~8: 1~8
    # error code: -2  (not likely)
def read_tile(tile_pos):
    # convert tile pos in pixel positions
    tile_pixel_pos = {'left': w_pos[0] + gb_pos[0] + tile_size*tile_pos[0],
                      'top': w_pos[1] + gb_pos[1] + tile_size*tile_pos[1],
                      'width': tile_size,
                      'height': tile_size}
    sct_img = sct.grab(tile_pixel_pos)  # grab the tile image
    # convert to RGB
    img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
    img = img.convert('RGB')
    # get the two important pixels for reading the tile statuses
    # pixel_1 is at (0, 0), for distinguish untouch tile and rest
    # pixel_2 is at (9, 8), the eigen pixel for the number tiles
    pixel_1 = img.getpixel((0, 0))
    pixel_2 = img.getpixel((9, 8))
    # following is the process of tile "image recognition"
    if pixel_1 == color_dark_grey:
        # belongs to the number tiles and the empty tile
        if pixel_2 == color_light_grey:
            return 0  # empty tile
        elif pixel_2 == color_blue:
            return 1
        elif pixel_2 == color_dark_green:
            return 2
        elif pixel_2 == color_red:
            return 3
        elif pixel_2 == color_dark_blue:
            return 4
        elif pixel_2 == color_dark_red:
            return 5
        elif pixel_2 == color_cyan:
            return 6
        elif pixel_2 == color_black:
            return 7
        elif pixel_2 == color_dark_grey:
            return 8
        else:
            # not likely to be here, not able to distinguish mines from numbers
            return -2  # error code
    elif pixel_1 == color_white:
        return -1  # untouched tile
    else:
        return -2  # error code

# read the yellow face, whether smile face, loosing face, or winning face
# return code:
    # loosing face: -1
    # smile face: 0
    # winning face: 1
    # error code: -2  (not likely to happen)
def read_face():
    # use same method from the read_tile() function for yellow face recognition
    sct_img = sct.grab(face_pixel_pos)
    # convert to RGB
    img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
    img = img.convert('RGB')
    # get the two face eigen pixels for expression recognition
    # pixel_1 is at (6, 8), pixel_2 is at (7, 8)
    # colors for eigen pixels for different faces:
        # smile face, yellow for (6, 8), black for (7, 8)
        # loosing face, black for (6, 8), yellow for (7, 8)
        # winning face, black for (6, 8), black for (7, 8)
    pixel_1 = img.getpixel((6, 8))
    pixel_2 = img.getpixel((7, 8))
    # following is the process of face expression recognition
    if pixel_1 == color_yellow:
        return 0  # smile face
    elif pixel_1 == color_black:
        if pixel_2 == color_yellow:
            return -1  # loosing face
        elif pixel_2 == color_black:
            return 1  # winning face
        else:
            return -2  # error code
    else:
        return -2 # error code

# click tile to open it
def click_tile(tile_pos)

# click face to restart the game
def click_face()




