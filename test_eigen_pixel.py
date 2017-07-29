# test program to find the eigen pixels of different statuses of the tiles
# for the use of image recognition with pixels
# run this under the "images" folder to find out the common eigen pixels

from PIL import Image

light_grey = (192, 192, 192)

title_initial = "tile digit "
title_suffix = ".png"

# a list of positions of the eigen pixels share by every tile statuses
common_list = []
# initialize it with number '1' tile
title = title_initial + str(1) + title_suffix
im = Image.open(title)
for i in range(1,16):
    for j in range(1,16):
        # skip the dark boundaries on top and left
        pixel = im.getpixel((i,j))
        if pixel != light_grey:
            common_list.append((i,j))  # append the pixel position

# check from all number files for common eigen pixel positions
for i in range(2,9):  # from 2 to 8
    title = title_initial + str(i) + title_suffix
    im = Image.open(title)
    edit_list = common_list[:]
    for pixel_pos in common_list:
        pixel = im.getpixel(pixel_pos)
        if pixel == light_grey:
            edit_list.remove(pixel_pos)
    # reflect edit_list to common_list
    common_list = edit_list[:]

# print the common eigen pixel positions
print(common_list)


# the eigen pixel positions for the number digit tiles:
# [(7, 4), (9, 3), (9, 4), (9, 7), (9, 8), (9, 11), (9, 12)]

# decide to use the one around the middle: (9, 8)

# double check the pixels from the number files
# for i in range(1,9):
#     title = title_initial + str(i) + title_suffix
#     im = Image.open(title)
#     print(im.getpixel((9,8)))

