exec(open("gcode_tools.py").read())

filename = sys.argv[1]
new_gcode = ""

## Maximum random offset added to any given X/Y coordinate
MAX_PERTURBANCE = 2

with open(filename) as file:
    for line in file:
        match = extract_coords(line)
        if match[0] or match[1]:
            qx = float(match[0])
            qy = float(match[1])
            qx += MAX_PERTURBANCE * (2*random.random() - 1)
            qy += MAX_PERTURBANCE * (2*random.random() - 1)
            new_command = substitute_coords(qx, qy, False, False, line)
            new_gcode += new_command
        else:
            new_gcode += line

new_file = open("perturbed.gcode", 'w')
new_file.write(new_gcode)
new_file.close()
