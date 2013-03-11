import os

id_char_map = {}
id_color_map = {}
id_custom_map = {}

#id_char_map_filename = raw_input('Enter the filename that contains the map of id to character: ')
#map_filename = raw_input('Enter the filename that contains the map of the original tiles in id form: ')
map_filename = 'tiles/id_map.txt'
id_char_map_filename = 'tiles/id_char_map.txt'
ascii_map_filename = 'tiles/ascii_id_map.txt'
color_map_filename = 'tiles/color_id_map.txt'
custom_map_filename = 'tiles/custom_id_map.txt'

if not os.path.isfile(id_char_map_filename):
    with open(id_char_map_filename, 'w') as a:
        a.write('')


with open(id_char_map_filename, 'r') as ifile:
    for line in ifile:
        tline = line.replace('\r','').replace('\n','').strip()
        char = None
        color = None
        custom = None

        if len(tline.split(',')) == 4:
            id, char, color, custom = tline.split(',')
        elif len(tline.split(',')) == 3:
            id, char, color = tline.split(',')
        elif len(tline.split(',')) == 2:
            id, char = tline.split(',')

        if char:
            id_char_map[int(id)] = char
        if color:
            id_color_map[int(id)] = color
        if custom:
            id_custom_map[int(id)] = custom

unknown_color_ids = {}
unknown_char_ids = {}
unknown_custom_ids = {}

with open(map_filename, 'r') as ifile, open(ascii_map_filename, 'w') as ascii_file, open(color_map_filename, 'w') as color_file, open(custom_map_filename, 'w') as custom_file:
    for line in ifile:
        for id in line.replace('\r','').replace('\n','').strip().split(','):
            actual_id = int(id)

            if actual_id in id_char_map:
                ascii_file.write('{0}'.format(id_char_map[actual_id]))
            else:
                ascii_file.write('?'.format())
                
                if not actual_id in unknown_char_ids:
                    unknown_char_ids[actual_id] = 0
                
                unknown_char_ids[actual_id] += 1

            if actual_id in id_color_map:
                color_file.write('{0},'.format(id_color_map[actual_id]))
            else:
                color_file.write(',')

                if not actual_id in unknown_color_ids:
                    unknown_color_ids[actual_id] = 0
                
                unknown_color_ids[actual_id] += 1

            if actual_id in id_custom_map:
                custom_file.write('{0},'.format(id_custom_map[actual_id]))
            else:
                custom_file.write(',')

                if not actual_id in unknown_custom_ids:
                    unknown_custom_ids[actual_id] = 0
                
                unknown_custom_ids[actual_id] += 1

        ascii_file.write('\n')
        color_file.write('\n')
        custom_file.write('\n')

with open('results.txt', 'w') as result_file:
    result_file.write('Unknown custom sorted by number of appearances\n')
    for id in sorted(unknown_custom_ids, key=unknown_custom_ids.get, reverse=True):
        result_file.write('{0} - {1}\n'.format(id, unknown_custom_ids[id]))

    result_file.write('Unknown characters sorted by number of appearances\n')
    for id in sorted(unknown_char_ids, key=unknown_char_ids.get, reverse=True):
        result_file.write('{0} - {1}\n'.format(id, unknown_char_ids[id]))

    result_file.write('Unknown colors sorted by number of appearances\n')
    for id in sorted(unknown_color_ids, key=unknown_color_ids.get, reverse=True):
        result_file.write('{0} - {1}\n'.format(id, unknown_color_ids[id]))