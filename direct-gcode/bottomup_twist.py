import sys
import re
import random
import numpy as np
exec(open("gcode_tools.py").read())

MAX_TWIST = 2*np.pi

filename = sys.argv[1]
new_filename = sys.argv[2]
new_gcode = ""

stats = coord_stats(filename)
max_z = stats["max"][2]
avg_x = stats["avg"][0]
avg_y = stats["avg"][1]

with open(filename) as file:
    x = 0
    y = 0
    z = 0
    for line in file:
        new_command = line
        coords = extract_coords(line)
        progress = (z/max_z)
        twist = progress * MAX_TWIST
        if coords[2]: z = coords[2]
        if coords[0]: x = coords[0]
        if coords[1]: y = coords[1]
        if coords[0]:
            new_x = avg_x + np.cos(twist)*(x-avg_x) - np.sin(twist)*(y-avg_y)
            new_command = substitute_coords(new_x, False, False, False, new_command)
        if coords[1]:
            new_y = avg_y + np.cos(twist)*(y-avg_y) + np.sin(twist)*(x-avg_x)
            new_command = substitute_coords(False, new_y, False, False, new_command)
        new_gcode += new_command

new_file = open(new_filename, 'w')
new_file.write(new_gcode)
new_file.close()
