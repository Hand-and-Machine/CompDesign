import sys
import re

filename = sys.argv[1]
new_gcode = ""

with open(filename) as file:
    for line in file:
        match = re.match("G1( X[0-9\.]+ Y[0-9\.]+ E[0-9\.-]+)", line)
        if match:
            new_command = "G2" + match[1] + "\n"
            new_gcode += new_command
        else:
            new_gcode += line

new_file = open("circ_interp_test.gcode", 'w')
new_file.write(new_gcode)
new_file.close()
