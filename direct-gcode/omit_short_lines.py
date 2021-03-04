import sys
import re
import random
import numpy as np
exec(open("gcode_tools.py").read())

MIN_LENGTH = 2

filename = sys.argv[1]
new_filename = sys.argv[2]
new_gcode = ""

## NOTE: This gcode has a very conspicuous inefficiency!
##       It will make the 3D printer go through all the same motions as before,
##       but it will only actually extrude plastic at a few of them.
##       Fix this later by skipping these unnecessary movements altogether!

total_lines = 0
lines_sustained = 0
lines_omitted = 0
with open(filename) as file:
    prev_x = 0
    prev_y = 0
    for line in file:
        total_lines += 1
        new_command = line
        coords = extract_coords(line)
        if coords[0] or coords[1]:
            x = coords[0]
            y = coords[1]
            if x == False: x = prev_x
            if y == False: y = prev_y
            norm = (x-prev_x)**2 + (y-prev_y)**2
            if norm < MIN_LENGTH**2:
                new_command = "G1 X" + str(x) + " Y" + str(y) + "\n"
                lines_omitted += 1
            else:
                lines_sustained += 1
            prev_x = x
            prev_y = y
        new_gcode += new_command

print("Total lines: " + str(total_lines))
print("Lines omitted: " + str(lines_omitted))
print("Lines sustained: " + str(lines_sustained))

new_file = open(new_filename, 'w')
new_file.write(new_gcode)
new_file.close()
