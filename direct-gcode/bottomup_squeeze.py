import sys
import re
import random
import numpy as np
exec(open("gcode_tools.py").read())

SQUEEZE_COEF = 0
POWER = 1

filename = sys.argv[1]
new_filename = sys.argv[2]
new_gcode = ""

stats = coord_stats(filename)
max_z = stats["max"][2]
avg_x = stats["avg"][0]
avg_y = stats["avg"][1]

with open(filename) as file:
    z = 0
    for line in file:
        new_command = line
        coords = extract_coords(line)
        progress = (z/max_z)**POWER
        squeeze = progress*SQUEEZE_COEF + (1-progress)
        if coords[2]: z = coords[2]
        if coords[0]:
            new_x = avg_x + squeeze*(avg_x-coords[0])
            new_command = substitute_coords(new_x, False, False, False, new_command)
        if coords[1]:
            new_y = avg_y + squeeze*(avg_y-coords[1])
            new_command = substitute_coords(False, new_y, False, False, new_command)
        if coords[3]:
            new_e = squeeze*coords[3]
            new_command = substitute_coords(False, False, False, new_e, new_command)
        new_gcode += new_command

new_file = open(new_filename, 'w')
new_file.write(new_gcode)
new_file.close()
