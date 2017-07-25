# test program to grab the images for researching the game design

import win32gui
import mss
from PIL import Image
import random  # generate random filename

hwnd = win32gui.FindWindow(None, 'Minesweeper X')
(left, top, right, bottom) = rect = win32gui.GetWindowRect(hwnd)
print(rect)
img_pos = {'left': left+(right-left)/2-10,
           'top': top+64,
           'width': 20,
           'height': 20}
sct = mss.mss()
sct_img = sct.grab(img_pos)  # get raw pixels from the screen
# create the image
img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
img = img.convert('RGB')  # convert to RGB
# print(img.getpixel((1,2)))

output = 'image-{}.png'.format(random.randint(0, 255))  # random number for filename
img.save(output)




# after testing, I found the positions(left, right, top, bottom) returned from
# win32gui.GetWindowRect() starts from 0, like dividing lines between the pixels,
# or like the indices of a string in python

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
# face pos:
    # beginner: [69, 64]
    # intermediate: [133, 64]
    # expert: [245, 64]
# face size: 20x20
# game board pos: [15, 101]
# game board size:
    # beginner: 8x8 mines, 128x128 pixels
    # intermediate: 16x16 mines, 256x256 pixels
    # expert: 30x16 mines, 480x256 pixels
# tile size: 16x16

# color rgb data:
# white: (255, 255, 255), some boundary areas
# light grey: (192, 192, 192), most background
# dark grey: (128, 128, 128), some boundary areas, number 8
# yellow: (255, 255, 0), face
# black: (0, 0, 0), mines, number 7
# blue: (0, 0, 255), number 1
# dark green: (0, 128, 0), number 2
# red: (255, 0, 0), number 3, number board
# dark blue: (0, 0, 128), number 4
# dark red: (128, 0, 0), number 5, number board
# cyan: (0, 128, 128), number 6

