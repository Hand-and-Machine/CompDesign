import sys
import re
import random
import numpy as np
exec(open("gcode_tools.py").read())

RADIUS = 10
NUM_HOLES = 200

filename = sys.argv[1]
new_filename = sys.argv[2]
new_gcode = ""

## NOTE: This gcode has a very conspicuous inefficiency!
##       It will make the 3D printer go through all the same motions as before,
##       but it will only actually extrude plastic at a few of them.
##       Fix this later by skipping these unnecessary movements altogether!

stats = coord_stats(filename)
min_x, min_y, min_z = stats["min"]
max_x, max_y, max_z = stats["max"]
print(str(min_x) + " " + str(min_y) + " " + str(min_z))
print(str(max_x) + " " + str(max_y) + " " + str(max_z))

hole_centers = [(random.uniform(min_x,max_x), random.uniform(min_y,max_y), random.uniform(min_z,max_z)) for i in range(NUM_HOLES)]

omitted = 0
sustained = 0
with open(filename) as file:
    x = 0
    y = 0
    z = 0
    for line in file:
        new_command = line
        coords = extract_coords(line)
        if coords[0]: x = coords[0]
        if coords[1]: y = coords[1]
        if coords[2]: z = coords[2]
        omit = False
        for c in hole_centers:
            if norm_dist(c, (x,y,z)) < RADIUS**2: omit = True
        if omit: 
            omitted += 1
            new_command = delete_coords(False, False, False, True, new_command)
        else:
            sustained += 1
        new_gcode += new_command

print("Omitted: " + str(omitted))
print("Sustained: " + str(sustained))

new_file = open(new_filename, 'w')
new_file.write(new_gcode)
new_file.close()
