import math
import Image
import ImageChops

COMPARE_CONSTANT = 10

def compare_tiles_cheap(tile_1, tile_2):
    tile_1_data = tile_1.getdata()
    tile_2_data = tile_2.getdata()
    return all(tile_1_data[i] == tile_2_data[i] for i in range(16))

def compare_tiles_expensive(tile_1, tile_2):
    h = ImageChops.difference(tile_1, tile_2).histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(tile.size[0] * c_tile.size[1]))

    return rms < COMPARE_CONSTANT

tiles = {}

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
    for x in range(0, width, tile_width):
        print('Processing column {0}: there are currently {1} unique tiles'.format(x, len(tiles)))
        for y in range(0, width, tile_height):
            tile = im.crop((x, y, x + tile_width, y + tile_height))

            is_similar = False
            for c_tile in tiles:
                
                if compare_tiles_cheap(tile, c_tile):
                    is_similar = True
                    tiles[c_tile] += 1
                    break

            if not is_similar:
                tiles[tile] = 1

with open('tiles/counts.csv', 'w') as ofile:
    id = 0
    for tile in tiles:
        id += 1
        tile.save('tiles/{0}.png'.format(id))
        ofile.write('{0}, {1}\n'.format(id, tiles[tile]))