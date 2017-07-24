# This program plays Minesweeper X in Windows
# By reading the game board through image, using rules to decide the locations of
# the mines, and playing the game with mouse clicks

# Minesweeper X version 1.15
# python version 2.7.13
# dependency: numpy-1.13.1+mkl, opencv-python
    # mss-3.0.1
    # Pillow-4.2.1

# Auto minesweeping strategy
# It's not necessary to use information from the two number boards,
# so no image recognition from there.
# Information from the yellow face is also not necessary but has been used, because it
# can be convenient to find out if we win or loose, and restart the game if needed.
# There is no need to decide which level the game is at, the program is designed
# to adapt custom board size, which incorporates all three basic levels.
# Not mark any tile with a flag, no need to to this extra step.

# The coordinate system for this windows application is:
# Origin is at left top corner, with x pointing right, and y axis pointing down.


# The problem with pop up window when new record has been created:


import win32gui
import mss
from PIL import Image
from auto_minesweeper_functions import *

# constants from measuring the game
gb_pos = (15, 101)  # relative coordinates of the game board in the game window
gb_margin = 15  # game board margins at bottom corners, both left and right
tile_size = 16  # number of pixels of a tile in x or y direction
face_size = 20  # number of pixels of the face in x or y direction


hwnd = win32gui.FindWindow(None, 'Minesweeper X')  # get window handle
rect = win32gui.GetWindowRect(hwnd)  # get game window positions
# left and top positions of the window in the screen display coordinates
# this acts as the reference coordinates for all images in the window
w_pos = (rect[0], rect[1])
w_size = (rect[2]-rect[0], rect[3]-rect[1])
# calculate game board size from the window size, mines in x and y directions
gb_size = ((w_size[0]-gb_pos[0]-gb_margin)/tile_size,
           (w_size[1]-gb_pos[1]-gb_margin)/tile_size)
# make sure above game board size calculation is correct
if ((w_size[0]-gb_pos[0]-gb_margin)%tile_size != 0 or
    (w_size[1]-gb_pos[1]-gb_margin)%tile_size != 0):
    print("game board size calculation from pixel size of window failed")
    break
# decide face position in relative coordinates
face_pos = (w_size[0]/2-10, 64)
# the position of the middle of the face for clicking
face_click = (face_pos[0]+face_size/2, face_pos[1]+face_size/2)




