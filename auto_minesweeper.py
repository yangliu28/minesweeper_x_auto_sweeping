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


# replace all the error code with sys.exit() function
# no need to wait for an empty tile to appear, start reasoning right away


from auto_minesweeper_functions import *
import random, sys

# get game board size, tiles on horizontal and vertical directions
gb_size = get_board_size()
if gb_size[0] < 1 or gb_size[1] < 1:
    # there should be at least one row and one colomn
    print("game board size not right")
    sys.exit()

game_won = False  # only quit the program until a win
while game_won == False:
    click_face()  # start a new game

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
    game_lost = False  # indicate if accidently open a mine
    while len(list_1) != 0:
        # continue trying to open tiles form 'list_1' if it's not empty
        tile_pos = random.choice(list_1)
        tile_pos = (tile_pos, 0)  # expand tile pos for the first row
        click_tile(tile_pos)  # open the tile
        # always read the face after open a tile
        face_status = read_face()
        if face_status == 0:  # game is good to continue
            tile_status = read_tile(tile_pos)
            if tile_status >= 0:
                # only update a good status reading
                gb[tile_pos[0]][tile_pos[1]] = tile_status
                if tile_status == 0:
                    empty_found = True
                    # update the game board ########################
                    break
                else:
                    # update the priority lists
                    list_1.remove(tile_pos[0])  # remove from first priority list
                    if (tile_pos[0] > 0) and ((tile_pos[0]-1) in list_1):
                        # remove the left neighbor, add to second priority
                        list_1.remove(tile_pos[0]-1)
                        list_2.append(tile_pos[0]-1)
                    if (tile_pos[0] < gb_size[0]-1) and ((tile_pos[0]+1) in list_1):
                        # remove the right neighbor, add to second priority
                        list_1.remove(tile_pos[0]+1)
                        list_2.append(tile_pos[0]+1)
            else:
                # should not be untouched(-1)
                print("tile clicking does not take effect, still untouched")
                sys.exit()
        elif face_status == -1:
            game_lost = True
            break
        elif face_status == 1
            game_won = True
            break
    # if game is won, program will return naturally; if game is lost, will start over
    if game_won or game_lost: continue
    # only start on 'list_2' if no empty tile was found from 'list_1'
    if not empty_found:
        while len(list_2) != 0:
            # continue trying to open tiles form 'list_2' if it's not empty
            tile_pos = random.choice(list_2)
            tile_pos = (tile_pos, 0)
            click_tile(tile_pos)
            face_status = read_face()
            if face_status == 0:  # game is good to continue
                tile_status = read_tile(tile_pos)
                if tile_status >= 0:
                    # only update a good status reading
                    gb[tile_pos[0]][tile_pos[1]] = tile_status
                    if tile_status == 0:
                        empty_found = True
                        # update the game board ########################
                        break
                    else:
                        # number tile, update the 'list_2'
                        list_2.remove(tile_pos[0])
                else:
                    # should not be untouched(-1)
                    print("tile clicking does not take effect, still untouched")
                    sys.exit()
            elif face_status == -1:
                game_lost = True
                break
            elif face_status == 1:
                game_won = True
                break
        if game_won or game_lost: continue
    # If under rare circumstance, the first row contains no empty tile,
    # then just try luck randomly with the rest tiles, no further rules on where to click




