# this program plays Minesweeper X in Windows
# by reading the game board through image, using rules to decide the locations of
# the mines, and playing the game with mouse click

# minesweeper x version 1.15
# python version 2.7.13
# dependency: numpy-1.13.1+mkl, opencv-python
    # mss-3.0.1
    # Pillow-4.2.1

# auto minesweeping strategy

import win32gui
import mss
from PIL import Image

# constants from measuring the game
gb_margin = (15, 101)  # left and top margin of game board, relative to window pos
nbl_margin = (20, 62)  # margins of left number board
nbr_margin_levels = ((97, 62), (225, 62), (449, 62))  # margins of right number board
face_margin_levels = ((69, 64), (133, 64), (245, 64))  # margins of face

hwnd = win32gui.FindWindow(None, 'Minesweeper X')  # get window handle
rect = win32gui.GetWindowRect(hwnd)  # get game window positions
w_pos = (rect[0], rect[1])  # left and top positions of the window

# decide game board size by the window size


