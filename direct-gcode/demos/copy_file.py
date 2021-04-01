import sys

filename = sys.argv[1]
new_filename = sys.argv[2]

gcode = ""

with open(filename) as file:
    for line in file:
        gcode += line

new_file = open(new_filename, 'w')
new_file.write(gcode)
new_file.close()
