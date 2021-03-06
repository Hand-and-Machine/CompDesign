import sys
import re
import random
import numpy as np
exec(open("gcode_tools.py").read())

MAX_PERTURBANCE = 2

filename = sys.argv[1]
new_filename = sys.argv[2]
new_gcode = ""

x_sum = 0
x_num = 0
with open(filename) as file:
    for line in file:
        coords = extract_coords(line)
        if coords[0]:
            x_sum += coords[0]
            x_num += 1
x_avg = x_sum/x_num

with open(filename) as file:
    for line in file:
        new_command = line
        coords = extract_coords(line)
        if coords[0] > x_avg:
            perturb_theta = 2*np.pi*random.random()
            perturb_r = MAX_PERTURBANCE*random.random()
            new_x = coords[0] + perturb_r*np.cos(perturb_theta)
            new_y = coords[1] + perturb_r*np.sin(perturb_theta)
            new_command = "G1 X" + str(new_x) + " Y" + str(new_y) + " E" + str(coords[3]) + "\n"
        new_gcode += new_command

new_file = open(new_filename, 'w')
new_file.write(new_gcode)
new_file.close()
