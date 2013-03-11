import math
import os
import shutil
import Image
import ImageChops

COMPARE_CONSTANT = 10

def compare_tiles_cheap(tile_1, tile_2):
    '''
        Pixel by pixel match algorithm. Exits as soon as a pixel is found which
        does not match.

    '''
    tile_1_data = tile_1.getdata()
    tile_2_data = tile_2.getdata()
    return all(tile_1_data[i] == tile_2_data[i] for i in range(len(tile_1_data)))

def compare_tiles_expensive(tile_1, tile_2):
    '''
        Least sum squares algorithm on the histogram of the difference between
        images.

        Setting the COMPARE_CONSTANT at the top of the file to a larger 
        value will allow more difference between tiles which are considered the
        same.

        This is more expensive to run than is ideal.
    '''
    h = ImageChops.difference(tile_1, tile_2).histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(tile.size[0] * c_tile.size[1]))

    return rms < COMPARE_CONSTANT

tiles = {}

if os.path.isdir('tiles'):
    if raw_input('tiles directory already exists. Would you like to empty it? (Y/N)').lower() == 'y':
        shutil.rmtree('tiles')

os.makedirs('tiles')

#filename = raw_input('Please enter the base image filename: ')
#tile_width = int(raw_input('Please enter the tile width: '))
#tile_height = int(raw_input('Please enter the tile height: '))
filename = 'pokemon-fl-kanto.png'
tile_width = 16
tile_height = 16

im = Image.open(filename)
width, height = im.size

if width % tile_width != 0:
    print('The image width ({0}) must be a multiple of the tile width ({1})'.format(width, tile_width))
elif height & tile_height != 0:
    print('The image height must be a multiple of the tile height')
else:
    print("The image being imported has width = {0} and height = {1}. You are using tile width {2} and tile height = {3}".format(width, height, tile_width, tile_height))
    id_image = [[-1 for x in range(width / tile_width)] for y in range(height / tile_height)]

    for x in range(0, width, tile_width):
        print('Processing column {0}: there are currently {1} unique tiles'.format(x, len(tiles)))
        for y in range(0, height, tile_height):
            tile_x, tile_y = x / tile_width, y / tile_height
            tile = im.crop((x, y, x + tile_width, y + tile_height))

            is_similar = False
            for c_tile in tiles:
                
                if compare_tiles_cheap(tile, c_tile):
                    is_similar = True
                    tiles[c_tile]['count'] += 1
                    id_image[tile_y][tile_x] = tiles[c_tile]['id']
                    break

            if not is_similar:
                id_image[tile_y][tile_x] = len(tiles)
                tiles[tile] = {'count':1, 'id':len(tiles)}

    with open('tiles/counts.csv', 'w') as ofile:
        for tile in tiles:
            tile.save('tiles/{0}.png'.format(tiles[tile]['id']))
            ofile.write('{0}, {1}\n'.format(tiles[tile]['id'], tiles[tile]['count']))

    with open('tiles/id_map.txt', 'w') as ofile:
        for y in range(0, height / tile_height):
            ofile.write(','.join([str(a) for a in id_image[y]]) + '\n')