# functions for interfacing the operations like image grabing, mouse clicking

import win32gui, win32api, win32con
import mss
from PIL import Image
import sys

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

# calculate game board size from window pixel size, number of tile in x and y directions
def get_board_size():
    # make sure game board size can be calculated from the pixels
    if ((w_size[0]-gb_pos[0]-gb_margin)%tile_size != 0 or
        (w_size[1]-gb_pos[1]-gb_margin)%tile_size != 0):
        print("game board size calculation from pixel size of the window failed")
        sys.exit()
    # calculate game board size of tiles in x and y directions, and return
    return ((w_size[0]-gb_pos[0]-gb_margin)/tile_size,
            (w_size[1]-gb_pos[1]-gb_margin)/tile_size)

# read tile, from possibilities include numbers(1~8), empty, or untouched
# there are other possibilities for the tile like flag, mine, red mine, or red cross mine
# but used together with read_face(), the rest situations can be avoided
# return code: (same as tile definition in 'board' variable)
    # untouched tile: -1
    # empty tile: 0
    # number tile 1~8: 1~8
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
            print("read_tile() error, pixel_2 error")
            sys.exit()
    elif pixel_1 == color_white:
        return -1  # untouched tile
    else:
        print("read_tile() error, pixel_1 error")
        sys.exit()

# read the yellow face, whether smile face, loosing face, or winning face
# return code:
    # loosing face: -1
    # smile face: 0
    # winning face: 1
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
            print("read_face() error, pixel_2 error")
            sys.exit()
    else:
        print("read_face() error, pixel_1 error")
        sys.exit()

# click tile to open it
def click_tile(tile_pos):
    tile_click_pos = (w_pos[0] + gb_pos[0] + tile_size*tile_pos[0] + tile_size/2,
                      w_pos[1] + gb_pos[1] + tile_size*tile_pos[1] + tile_size/2)
    win32api.SetCursorPos(tile_click_pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# click face to restart the game
def click_face():
    win32api.SetCursorPos(face_click_pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# return a list of positions of the neighbor tiles
def get_neighbors(tp, gb_size):
    # input: tile pos and game board size
    if tile_pos[0] > 0:
        if tile_pos[0] < gb_size[0]-1:
            if tile_pos[1] > 0:
                if tile_pos[1] < gb_size[1]-1:
                    # return all eight tiles around
                    return [(tp[0]-1, tp[1]-1), (tp[0]-1, tp[1]), (tp[0]-1, tp[1]+1),
                            (tp[0], tp[1]-1), (tp[0], tp[1]+1),
                            (tp[0]+1, tp[1]-1), (tp[0]+1, tp[1]), (tp[0]+1, tp[1]+1)]
                else:
                    # on the bottom row, not corners
                    return [(tp[0]-1, tp[1]-1), (tp[0]-1, tp[1]),
                            (tp[0], tp[1]-1),
                            (tp[0]+1, tp[1]-1), (tp[0]+1, tp[1])]
            else:
                # on the top row, not corners
                return [(tp[0]-1, tp[1]), (tp[0]-1, tp[1]+1),
                        (tp[0], tp[1]+1),
                        (tp[0]+1, tp[1]), (tp[0]+1, tp[1]+1)]
        else:
            if tile_pos[1] > 0:
                if tile_pos[1] < gb_size[1]-1:
                    # on the right row, not corners
                    return [(tp[0]-1, tp[1]-1), (tp[0]-1, tp[1]), (tp[0]-1, tp[1]+1),
                            (tp[0], tp[1]-1), (tp[0], tp[1]+1)]
                else:
                    # on the right bottom corner
                    return [(tp[0]-1, tp[1]-1), (tp[0]-1, tp[1]),
                            (tp[0], tp[1]-1)]
            else:
                # on the right top corner
                return [(tp[0]-1, tp[1]), (tp[0]-1, tp[1]+1),
                        (tp[0], tp[1]+1)]
    else:
        if tile_pos[1] > 0:
            if tile_pos[1] < gb_size[1]-1:
                # on the left row, not corners
                return [(tp[0], tp[1]-1), (tp[0], tp[1]+1),
                        (tp[0]+1, tp[1]-1), (tp[0]+1, tp[1]), (tp[0]+1, tp[1]+1)]
            else:
                # on the left bottom corner
                return [(tp[0], tp[1]-1),
                        (tp[0]+1, tp[1]-1), (tp[0]+1, tp[1])]
        else:
            # on the left top corner
            return [(tp[0], tp[1]+1),
                    (tp[0]+1, tp[1]), (tp[0]+1, tp[1]+1)]

# check if new number tile is qualified for the reasoning pool, and update rp
def rp_check_new(gb, rp, gb_size, tile_pos):
    if tile_pos in rp.keys(): return  # skip if it is already in the reasoning pool
    rp_value = [[],[],[],[]]  # new value for the new entry in rp
    for tile_pos_n in get_neighbors(tile_pos, gb_size):
        if gb[tile_pos_n[0]][tile_pos_n[1]] == -1:
            rp_value[0].append(tile_pos_n)  # add this neighbor to unknown tiles list
        elif gb[tile_pos_n[0]][tile_pos_n[1]] == 0:
            rp_value[1].append(tile_pos_n)  # add this neighbor to empty tiles list
        elif (gb[tile_pos_n[0]][tile_pos_n[1]] >= 1 and
              gb[tile_pos_n[0]][tile_pos_n[1]] <= 8):
            rp_value[2].append(tile_pos_n)  # add this neighbor to number tiles list
        else:  # tile_pos_n is a mine tile
            rp_value[3].append(tile_pos_n)  # add this neighbor to mine tiles list
    if len(rp_value[0]) > 0:
        # this tile has at least one unknown neighbors, qualified for the reasoning pool
        rp[tile_pos] = rp_value

# actions to be taken after opening a number tile
def actions_on_number(gb, rp, gb_size, tile_pos, tile_status):
    # gb and rp are mutables, changes will be reflected outside
    # update this tile's status into gb variable
    gb[tile_pos[0]][tile_pos[1]] = tile_status
    # check if new number tile qualifies for reasoning pool
    rp_check_new(gb, rp, gb_size, tile_pos)
    # check disqualifications in the reasoning pool, only check the adjacent tiles
    for tile_pos_n in get_neighbors(tile_pos, gb_size):
        if tile_pos_n in rp.keys():
            # then it must be in the unknown list of tile_pos_n
            rp[tile_pos_n][0].remove(tile_pos)
            if len(rp[tile_pos_n][0]) == 0:
                rp.pop(tile_pos_n)
            else:
                # tile_pos_n entry in reasoning pool is still valid
                # put its neighbor tile_pos to where it is supposed to be
                rp[tile_pos_n][2].append(tile_pos)  # add to number tiles list

# actions to be taken after opening an empty tile
def actions_on_empty(gb, rp, gb_size, tile_pos):
    # update this tile's status into gb variable
    gb[tile_pos[0]][tile_pos[1]] = 0  # '0' is the status for empty tile
    # search adjacent for empty tiles, a connected empty area should be out there
    empty_pool = [tile_pos]  # will search empty neighbors of all tiles in this pool
    rp_temp = []  # temporary reasoning pool, will check qualification afterwards
    while len(empty_pool) != 0:
        # the following is for processing the neighbors of empty_pool[0]
        # first remove it from dynamic empty tile pool
        empty_pool.pop(0)  # pop out the first tile
        for tile_pos_n in get_neighbors(empty_pool[0], gb_size):
            if gb[tile_pos_n[0]][tile_pos_n[1]] == -1:
                # only continue if tile has not been read yet
                tile_status = read_tile(tile_pos_n)
                gb[tile_pos_n[0]][tile_pos_n[1]] = tile_status  # update in gb variable
                if tile_status == 0:
                    # new empty tile found, add it to the dynamic pool
                    empty_pool.append(tile_pos_n)
                elif tile_status == -1 or tile_status == 9:
                    # error here, the neighbor of an empty tile should not be untouched
                    # tiles or mine tiles
                    print("error in check neighbors of empty tiles - actions_on_empty()")
                    sys.exit()
                else:  # this neighbor is a number tile
                    # put it in an accumulating list, rp_temp
                    # will check later if it is qualified for the reasoning pool
                    if tile_pos_n not in rp_temp:  # avoid duplication
                        rp_temp.append(tile_pos_n)
    # check and add new entries to the reasoning pool from rp_temp
    for tile_pos_t in rp_temp:  # tile pos temp
        rp_check_new(gb, rp, gb_size, tile_pos_t)
    # check disqualifications in the the reasoning pool
    # since a new empty area is opened, it might be simple to just check all tiles in pool
    for tile_pos_t in rp.keys():
        for tile_pos_tn in rp[tile_pos_t][0]:  # tile pos temp neighbor
            tile_status = gb[tile_pos_tn[0]][tile_pos_tn[1]]
            if tile_status != -1:
                # remove it first from the unknown tiles list
                rp[tile_pos_t][0].remove(tile_pos_tn)
                # relocate this tile to the right list
                if tile_status == 0:
                    # add it to the empty tiles list
                    rp[tile_pos_t][1].append(tile_pos_tn)
                elif tile_status >= 1 and tile_status <= 8:
                    # add it to the number tiles list
                    rp[tile_pos_t][2].append(tile_pos_tn)
                else:
                    # add it to the mine tiles list
                    rp[tile_pos_t][3].append(tile_pos_tn)
        # finish checking the unknown tiles list
        if len(rp[tile_pos_t][0]) == 0:
            rp.pop(tile_pos_t)

# actions to be taken after locating a mine
def actions_on_mine(gb, rp, gb_size, tile_pos):
    # update this tile's status into gb variable
    gb[tile_pos[0]][tile_pos[1]] = 9  # '9' is the status for mine tile
    # check disqualifications in the reasoning pool, only check the adjacent tiles
    for tile_pos_n in get_neighbors(tile_pos, gb_size):
        if tile_pos_n in rp.keys():
            # then it must be in the unknown list of tile_pos_n
            rp[tile_pos_n][0].remove(tile_pos)
            if len(rp[tile_pos_n][0]) == 0:
                rp.pop(tile_pos_n)
            else:
                rp[tile_pos_n][2].append(tile_pos)  # add to number tiles list


