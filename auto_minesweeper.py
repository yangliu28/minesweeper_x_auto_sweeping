# The main program. This program plays Minesweeper X in Windows
# By reading the game board through image, using rules to decide the locations of
# the mines, and playing the game with mouse clicks

# Minesweeper X version 1.15
# python version 2.7.13
# dependency: numpy-1.13.1+mkl
    # mss-3.0.1
    # Pillow-4.2.1
    # win32api

# Auto minesweeping strategy
# It's not necessary to use information from the two number boards,
# so no image recognition from there.
# Information from the yellow face is also not necessary but has been used, because it
# can be convenient to find out if we win or loose, and restart the game if needed.
# There is no need to decide which level the game is at, the program is designed
# to adapt custom board size, which incorporates all three basic levels.
# There is no right click on any tile, only left click is used to solve the game.

# The coordinate system for this windows application is:
# Origin is at left top corner, with x pointing right, and y axis pointing down.


# The problem with pop up window when new record has been created:


# add keyboard control for pause and quit


from auto_minesweeper_functions import *
import random

# get game board size, tiles on horizontal and vertical directions
gb_size = get_board_size()
if gb_size[0] < 1 or gb_size[1] < 1:
    print("game board size not right")
    return

game_win = False  # only quit the program until a win
while game_win == False:
    # the start of a new game

    # instantiate a variable holding all states of tiles on the game board
    gb = [[-1 for j in range(gb_size[1])] for i in range(gb_size[0])]
    # when indexing, first index is how many tiles from left, second is how many from top
    # status value explanation:
        # '-1': untouched
        # '0': empty
        # '1~8': number 1~8
        # '9': mine

    # start with a random click on the top row, until a large area is discovered
    # (this technique has been used by the professional human players)
    # method is that if a number is opened, there is chance that the two tiles on left
    # and right have mines, so avoid them too. If no such tile is available, then try
    # the ones adjacent to the opened numbers.
    empty_found = False  # whether an empty tile has been found or not
    list_1 = list(range(gb_size[0]))  # list with first priority
    list_2 = []  # list with second priority
    while len(list_1) is not 0:
        # could still try to open tiles from the list_1
        tile_pos = random.choice(list_1)
        tile_pos = (tile_pos, 0)  # expand tile pos for the first row
        click_tile(tile_pos)  # open the tile
        tile_status = read_tile(tile_pos)


    # If under rare circumstance, the first row contains no empty tile,
    # then just try luck randomly with the rest tiles, no further rules on where to click




