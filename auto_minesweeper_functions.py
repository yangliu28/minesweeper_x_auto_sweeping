# functions frequently used in the auto minesweeper

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

# read tile, from possibilities include numbers(1~8), empty, or untouched
# there are other possibilities for the tile like flag, mine, red mine, or red cross mine
# but used together with read_face(), the rest situations can be avoided
# return code: (same as tile definition in 'board' variable)
    # untouched tile: -1
    # empty tile: 0
    # number tile 1~8: 1~8
    # error code: -2  (not likely)
def read_tile(pixel_1, pixel_2):
    # pixel_1 is at (0, 0), for distinguish untouch tile and rest
    # pixel_2 is at (9, 8), the eigen pixel for the number tiles
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
            # not likely to be here, not able to distinguish mines this way
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
    # error code: -2  (not likely)
def read_face(pixel_1, pixel_2):
    # use same principle from the read_tile
    # pixel_1 is at (6, 8), eigen pixel 1 for the face
    # pixel_2 is at (7, 8), eigen pixel 2 for the face
    # colors for eigen pixels for different faces:
        # smile face, yellow for (6, 8), black for (7, 8)
        # loosing face, black for (6, 8), yellow for (7, 8)
        # winning face, black for (6, 8), black for (7, 8)
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

# click anywhere with the left key of the mouse
# no right key click is used like marking the mine with a flag
def left_click()



