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

# While the custom size of the game board can be as large as possible, there is a
# lower limit of 8 tiles in x direction so that the program can function well.
# This program calculates the game board size from the pixel size of the window,
# if there are less than 8 tiles in x, the window size will still reflect 8 tiles.
# Refer to the "game window minimum case.png" file under image templates folder.


# The problem with pop up window when new record has been created:


# add keyboard control for pause and quit
# remove untouched tile option from read_tile() function?


from auto_minesweeper_functions import *
import random, sys

# get game board size, tiles on horizontal and vertical directions
gb_size = get_board_size()
if gb_size[0] < 1 or gb_size[1] < 1:
    # there should be at least one row and one colomn
    print("game board size not right")
    sys.exit()

game_won = False  # only quit the program until winning the game
while not game_won:
    click_face()  # start a new game

    # instantiate a variable holding all states of tiles on the game board
    gb = [[-1 for j in range(gb_size[1])] for i in range(gb_size[0])]
    # when indexing, first index is how many tiles from left, second is how many from top
    # status value explanation:
        # '-1': untouched
        # '0': empty
        # '1~8': number 1~8
        # '9': mine

    # instantiate a dictionary variable for the reasoning process
    rp = {}  # reasoning pool
    # key is the tile pos (x,y), only number tiles qualify for this pool, and the tile
    # needs to have at least one unknown neighbor. Once all unknown neighbors are defined,
    # this tile will be removed from the pool.
    # value: [list_1, list_2, list_3, list_4]
        # list_1: positions of unknown neighbors
        # list_2: positions of empty neighbors
        # list_3: positions of number neighbors
        # list_4: positions of mine neighbors

    # 1.start with a random click on the top row
    # (this technique has been used by the professional human players)
    # previously I tried continue clicking until an empty tile is discovered
    # but that just make this part of the program unnecessarily complicated
    # right now it just opens one tile, and start reasoning or guessing right away
    # maybe unluckily sometimes, but the chance is the same with finding the empty tile
    tile_pos = random.choice(range(gb_size[0]))
    tile_pos = (tile_pos, 0)  # expand tile pos for the first row
    click_tile(tile_pos)  # click to open the tile
    # should always read the face first after opening a tile
    # but no need here, because it is always safe for the first click
    tile_status = read_tile(tile_pos)
    # tile status can only be empty or numbers for the first click
    if tile_status > 0:
        actions_on_number(gb, rp, gb_size, tile_pos, tile_status)
    elif tile_status == 0:
        actions_on_empty(gb, rp, gb_size, tile_pos, tile_status)
    else:
        # should not be here, after clicking the tile should not be untouched
        print("tile is still untouched ater clicking - random starting click")
        sys.exit()

    # the repeated loop implementing the reasoning strategy
    game_finished = False  # indicate if this round of game is done
    while not game_finished:
        # continuously reasoning until this game is finished(win or loose)
        # In each cycle of this while loop, one action needs to be done.
        # Either locate position of at least one mine, or open at least one tile.
        # Will try out strategies in the order of basic strategy, advanced strategy,
        # and guessing strategy. Once an action is done in any one of them, this will
        # end the cycle and go on a new one. Guessing strategy will ensure an action
        # is done if basic and advanced strategies failed.
        action_done = False  # flag indicating an action is done or not in this cycle

        # 2.basic strategy
        # check each tile individually to locate mines or find safe tiles
        for tile_pos in rp.keys():
            tile_number = gb[tile_pos[0]][tile_pos[1]]
            if tile_number - len(rp[tile_pos][3]) == 0:
                # all unknowns are safe
                safe_tiles = rp[tile_pos][0]  # list for all safe tiles
                for tp in safe_tiles:
                    click_tile(tp)  # open this tile
                    face_status = read_face()
                    if face_status == -1: 
                        # loosing face, this should not happen if reasoning is correct
                        print("step on a mine - 2.basic strategy")
                        sys.exit()
                    elif face_status == 1:
                        # game has been won, exit the program
                        print("game is won - 2.basic strategy")
                        sys.exit()
                    else:
                        # smile face, game is good to continue
                        tile_status = read_tile(tp)
                        if tile_status > 0:

                action_done = True
                break  # exiting the reasoning pool check
            elif tile_number - len(rp[tile_pos][3]) == len(rp[tile_pos][0]):
                # all unknowns are mines
                action_done = True
                break  # exiting the reasoning pool check

        # skip the following strategies if an action is done
        if action_done: continue







