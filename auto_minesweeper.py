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
    # but no need here, because it is the first click
    tile_status = read_tile(tile_pos)
    gb[tile_pos[0]][tile_pos[1]] = tile_status  # update in the game board variable
    if tile_status > 0:
        # number tile, update the reasoning pool
        # first number tile, all neighbors should be unknown
        rp[tile_pos] = [get_neighbors(tile_pos, gb_size), [], [], []]
    elif tile_status == 0:
        # search adjacent empty tiles, a large empty area is discovered
        empty_pool = [tile_pos]  # search empty neighbors of all tiles in this pool
        rp_temp = []  # temporary reasoning pool, check qualification afterwards 
        while len(empty_pool) != 0:
            # the following has processed the neighbors of empty_pool[0]
            # remove it from dynamic empty tile pool
            empty_pool.pop(0)  # pop out the first tile
            for tile_pos in get_neighbors(empty_pool[0], gb_size):  # use the first in pool
                if gb[tile_pos[0]][tile_pos[1]] == -1:
                    # only continue if tile has not been read yet
                    tile_status = read_tile(tile_pos)
                    gb[tile_pos[0]][tile_pos[1]] = tile_status  # update in game board variable
                    if tile_status == 0:
                        # new empty tile found, add it to the dynamic pool
                        empty_pool.append(tile_pos)
                    else:
                        # put number tiles it in an accumulating list
                        # to check later if it qualifies the reasoning pool
                        # ideally all number tiles here are qualified because of first click
                        if tile_pos not in rp_temp:  # avoid duplication
                            rp_temp.append(tile_pos)
        # check and add new entries to the reasoning pool from rp_temp
        for tile_pos in rp_temp:
            rp_value = [[],[],[],[]]  # dictionary value of rp variable
            for tile_pos_n in get_neighbors(tile_pos, gb_size):  # stands for tile pos neighbor
                if gb[tile_pos_n[0]][tile_pos_n[1]] == -1:
                    rp_value[0].append(tile_pos_n)  # add this neighbor to unknown tiles list
                elif gb[tile_pos_n[0]][tile_pos_n[1]] == 0:
                    rp_value[1].append(tile_pos_n)  # add this neighbor to empty tiles list
                elif (gb[tile_pos_n[0]][tile_pos_n[1]] >= 1 and
                      gb[tile_pos_n[0]][tile_pos_n[1]] <= 8):
                    rp_value[2].append(tile_pos_n)  # add this neighbor to number tiles list
                else:  # tile_pos_n mine tile
                    rp_value[3].append(tile_pos_n)  # add this neighbor to mine tiles list
            if len(rp_value[0]) > 0:
                # this tile has unknown neighbors, qualified for the reasoning pool
                rp[tile_pos] = rp_value  # add new entry into reasoning pool

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
        # check one tile each time to find mines or safe tiles
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
                        print("step on a mine (2.basic strategy)")
                        sys.exit()
                    elif face_status == 1:
                        # game has been won, exit the program
                        print("game is won (2.basic strategy)")
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



# check disqualification in the reasoning pool after an action has been done



