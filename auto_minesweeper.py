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

# strategies for human players
# http://www.minesweeper.info/wiki/Strategy

# The problem with pop up window when new record has been created:


# add keyboard control for pause and quit
# remove untouched tile option from read_tile() function?


from auto_minesweeper_interface import *
import random, sys

# get game board size, tiles on horizontal and vertical directions
gb_size = get_board_size()
if gb_size[0] < 1 or gb_size[1] < 1:
    # there should be at least one row and one colomn
    print("game board size not right")
    sys.exit()

game_won = False  # only quit the program until winning the game
game_count = 0  # count how many games have been played to get a win
while not game_won:
    game_count = game_count + 1
    print "*************** new game {} ***************".format(game_count)
    # start a new game, always click even if a game is ready
    click_face()

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
        actions_on_empty(gb, rp, gb_size, tile_pos)

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
        # Searching for two basic situation here:
        # Tile number subtracts mines number equals zero, then all unknowns are safe.
        # Tile number subtracts mines number equals number of unknowns, then all
        # unkowns are mines.
        for tile_pos in rp.keys():
            tile_number = gb[tile_pos[0]][tile_pos[1]]
            if tile_number - len(rp[tile_pos][3]) == 0:
                # all unknowns are safe
                safe_tiles = rp[tile_pos][0]  # list for all safe tiles
                # can open multiple tiles at a time
                for tile_pos_t in safe_tiles:  # stands for tile pos temp
                    click_tile(tile_pos_t)  # open this tile
                    face_status = read_face()
                    if face_status == -1: 
                        # loosing face, this should not happen if reasoning is correct
                        debug_print_gb(gb, gb_size)
                        debug_print_rp(rp)
                        print("step on a mine - basic strategy")
                        sys.exit()
                    elif face_status == 1:
                        # game has been won, exit the program
                        print("game is won - basic strategy")
                        sys.exit()
                    else:
                        # smile face, game is good to continue
                        tile_status = read_tile(tile_pos_t)
                        if tile_status > 0:  # for number tile
                            actions_on_number(gb, rp, gb_size, tile_pos_t, tile_status)
                        elif tile_status == 0:  # for empty tile
                            actions_on_empty(gb, rp, gb_size, tile_pos_t)
                action_done = True  # reverse the flag
                break  # wait here to break so can have multiple tiles opened
            elif tile_number - len(rp[tile_pos][3]) == len(rp[tile_pos][0]):
                # all unknowns are mines
                mine_tiles = rp[tile_pos][0]  # list for all mine tiles
                for tile_pos_t in mine_tiles:
                    actions_on_mine(gb, rp, gb_size, tile_pos_t)
                action_done = True  # reverse the flag
                break

        # skip the following strategies if an action is done
        if action_done: continue

        # 3.advanced strategy
        # check every pair of adjacent tiles to collectively decide mines or safe tiles
        # In such pair, two tiles share several public unknown tiles, each also has its
        # own private unknown tiles. Each tile decides the possible number of mines in the
        # public unknown tiles, then there are two sets of decisions on public tiles.
        # If the intersection of the two sets contains only one decision, then this is the
        # only possibility for the public unknown tiles.
        rp_len = len(rp.keys())  # number of entries in reasoning pool
        if rp_len > 1:  # there should be at least two entries to form minimum of one pair
            # find every combination of tiles
            pairs = []
            for i in range(rp_len):
                for j in range(i+1, rp_len):
                    tile_1_pos = rp.keys()[i]
                    tile_2_pos = rp.keys()[j]
                    # check if they are adjacent
                    if (abs(tile_1_pos[0] - tile_2_pos[0]) <= 1 and
                        abs(tile_1_pos[1] - tile_2_pos[1]) <= 1):
                        pairs.append((i,j))
            for pair in pairs:
                tile_1_pos = rp.keys()[pair[0]]
                tile_2_pos = rp.keys()[pair[1]]
                # public unknown tiles share by tile_1 and tile_2
                public_tiles = list(set(rp[tile_1_pos][0]) & set(rp[tile_2_pos][0]))
                if len(public_tiles) > 0:  # they do share public unknown tiles
                    # private unknown tiles owned by tile_1 and tile_2
                    private_1_tiles = list(set(rp[tile_1_pos][0]) - set(rp[tile_2_pos][0]))
                    private_2_tiles = list(set(rp[tile_2_pos][0]) - set(rp[tile_1_pos][0]))
                    # number on the tiles
                    number_1 = gb[tile_1_pos[0]][tile_1_pos[1]]
                    number_2 = gb[tile_2_pos[0]][tile_2_pos[1]]
                    # calculate possibilities of number of mines in public tiles
                    # from tile_1's persective
                    min_1 = max(0, number_1-len(private_1_tiles))
                    max_1 = min(len(public_tiles), number_1)
                    decision_1 = set(range(min_1, max_1+1))
                    # from tile_2's persective
                    min_2 = max(0, number_2-len(private_2_tiles))
                    max_2 = min(len(public_tiles), number_2)
                    decision_2 = set(range(min_2, max_2+1))
                    # intersection of the two sets
                    comm_decision = list(decision_1 & decision_2)
                    if len(comm_decision) == 1:
                        print "the pair that reaches the decision {} and {}".format(tile_1_pos, tile_2_pos)
                        print "public tiles {}".format(public_tiles)
                        print "private tiles {} and {}".format(private_1_tiles, private_2_tiles)
                        print "common decision for public tiles {}".format(comm_decision)
                        # there is only one possibility for public tiles
                        # meaning only one possibility for the private tiles
                        # Since following steps are similar for public tiles and two sets of
                        # private tiles, put them in iterations to avoid repeated code.
                        mine_nums = [comm_decision[0]]  # initialize with number of public mines
                        tile_sets = [public_tiles]
                        if len(private_1_tiles) > 0:
                            mine_nums.append(number_1 - len(private_1_tiles))
                            tile_sets.append(private_1_tiles)
                        if len(private_2_tiles) > 0:
                            mine_nums.append(number_2 - len(private_2_tiles))
                            tile_sets.append(private_2_tiles)
                        # start iteration
                        for i in range(len(mine_nums)):
                            mine_num = mine_nums[i]
                            tile_set = tile_sets[i]
                            if mine_num == 0:
                                # all tiles are safe in tile_set
                                print "actions: safe tiles are {}".format(tile_set)
                                for tile_pos in tile_set:
                                    click_tile(tile_pos)
                                    face_status = read_face()
                                    if face_status == -1:
                                        debug_print_gb(gb, gb_size)
                                        debug_print_rp(rp)
                                        print("step on a mine - advanced strategy")
                                        sys.exit()
                                    elif face_status == 1:
                                        print("game is won - advanced strategy")
                                        sys.exit()
                                    else:
                                        tile_status = read_tile(tile_pos)
                                        if tile_status > 0:
                                            actions_on_number(gb, rp, gb_size, tile_pos, tile_status)
                                        elif tile_status == 0:
                                            actions_on_empty(gb, rp, gb_size, tile_pos)
                                action_done = True  # reverse the flag
                                break
                            elif mine_num == len(tile_set):
                                # all public tiles are mines
                                print "actions: mine tiles are {}".format(tile_set)
                                for tile_pos in tile_set:
                                    actions_on_mine(gb, rp, gb_size, tile_pos)
                                action_done = True  # reverse the flag
                                break
                    elif len(comm_decision) == 0:
                        # the two tiles contradict on the public tiles
                        debug_print_gb(gb, gb_size)
                        debug_print_rp(rp)
                        print "the pair that reaches the decision {} and {}".format(tile_1_pos, tile_2_pos)
                        print "public tiles {}".format(public_tiles)
                        print "private tiles {} and {}".format(private_1_tiles, private_2_tiles)
                        print "common decision for public tiles {}".format(comm_decision)
                        print("two adjacent tiles contradict on public tiles - advanced strategy")
                        sys.exit()

        # skip the following strategies if an action is done
        if action_done: continue

        # 4.guessing strategy (final resort)
        # no need to pick one tile in the middle of large untouched tiles
        # still try guessing one entry from the reason pool, now using the first one
        # Guessing the safe tiles instead of mine tiles, so that we can open the safe
        # tiles instead of mark tile as mine, then we know immediately if guessing is correct.
        # Only one tile is opened from this guess, so to keep risk to the minimum.
        tile_pos = rp.keys()[0]
        tile_number = gb[tile_pos[0]][tile_pos[1]]  # the number on the tile
        unknown_tiles = rp[tile_pos][0]
        mine_left = tile_number - len(rp[tile_pos][3])  # number of mines left
        if mine_left > 0 and mine_left < len(unknown_tiles):
            # guessing conditions satisfied
            safe_left = len(unknown_tiles) - mine_left  # safe tiles in the unknowns
            safe_tiles = random.sample(unknown_tiles, safe_left)  # randomly choose the safe ones
            # Used to open all the guessed safe tiles, but risk is too high, try one at a time
            # In this case, the first one in safe_tiles is our guess.
            guess_tile = safe_tiles[0]
            print "guess the safe tile is {}".format(guess_tile)  # print out the guess
            # try luck on the guess
            click_tile(guess_tile)
            face_status = read_face()
            if face_status == -1:
                print("step on a mine - guessing strategy")
                # should not quit program, it is a forgivable mistake
                game_finished = True
                break  # just break
            elif face_status == 1:
                print("game is won - guessing strategy")
            else:  # smile face, game is good to go
                tile_status = read_tile(guess_tile)
                if tile_status > 0:
                    actions_on_number(gb, rp, gb_size, guess_tile, tile_status)
                elif tile_status == 0:
                    actions_on_empty(gb, rp, gb_size, guess_tile)
            action_done = True  # reverse the flag, not necessary though
        else:
            debug_print_gb(gb, gb_size)
            debug_print_rp(rp)
            print("tile is not satisfied with guessing conditions - guessing strategy")
            sys.exit()


