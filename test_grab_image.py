# grab image for researching the game design

import win32gui
import mss
from PIL import Image
import random  # generate random filename



hwnd = win32gui.FindWindow(None, 'Minesweeper X')
(left, top, right, bottom) = rect = win32gui.GetWindowRect(hwnd)
img_pos = {'left': left+15+16*9,
           'top': top+101+16*3,
           'width': 16,
           'height': 16}
sct = mss.mss()
sct_img = sct.grab(img_pos)  # get raw pixels from the screen
# create the image
img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
img = img.convert('RGB')  # convert to RGB

output = 'image-{}.png'.format(random.randint(0, 255))  # random number for filename
img.save(output)




# after testing, I found the positions(left, right, top, bottom) returned from
# win32gui.GetWindowRect() starts from 0 and like dividing lines between the pixels,
# or like the index of a string in python

# facts about the pixels of images in the game
# game window size:
    # beginner: 158x244
    # intermediate: 286x372
    # expert: 510x372
# left number board pos: [20, 62] (defined as pixels to left and top)
# right number board pos: (pixels to left is game window width subtracts 61)
    # beginner: [97, 62]
    # intermediate: [225, 62]
    # expert: [449, 62]
# number board size(left/right): 39x23
    # each digit is 13 pixels width
# middle face pos:
    # beginner: [69, 64]
    # intermediate: [133, 64]
    # expert: [245, 64]
# middle face size: 20x20
# game board pos: [15, 101]
# game board size:
    # beginner: 8x8 mines, 128x128 pixels
    # intermediate: 16x16 mines, 256x256 pixels
    # expert: 30x16 mines, 480x256 pixels
# tile size: 16x16



