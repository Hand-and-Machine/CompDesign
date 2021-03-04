import sys
import re
import random
import numpy as np
exec(open("gcode_tools.py").read())

MAX_PERTURBANCE = 1
POWER = 2

filename = sys.argv[1]
new_filename = sys.argv[2]
new_gcode = ""
max_z = get_max_zvalue(filename)

with open(filename) as file:
    z = 0
    for line in file:
        new_command = line
        coords = extract_coords(line)
        if coords[2]: z = coords[2]
        elif coords[0] and coords[1] and coords[3]:
            perturb_theta = 2*np.pi*random.random()
            perturb_r = MAX_PERTURBANCE*random.random()*(z/max_z)**POWER
            new_x = coords[0] + perturb_r*np.cos(perturb_theta)
            new_y = coords[1] + perturb_r*np.sin(perturb_theta)
            new_command = "G1 X" + str(new_x) + " Y" + str(new_y) + " E" + str(coords[3]) + "\n"
        new_gcode += new_command

new_file = open(new_filename, 'w')
new_file.write(new_gcode)
new_file.close()
