# grab image for researching the game design

import win32gui
import mss
from PIL import Image
import random  # generate random filename



hwnd = win32gui.FindWindow(None, 'Minesweeper X')
(left, top, right, bottom) = rect = win32gui.GetWindowRect(hwnd)
img_pos = {'left': left,
           'top': top,
           'width': right-left,
           'height': bottom-top}
sct = mss.mss()
sct_img = sct.grab(img_pos)  # get raw pixels from the screen
# create the image
img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
img = img.convert('RGB')  # convert to RGB

output = 'image-{}.png'.format(random.randint(0, 255))  # random number for filename
img.save(output)

