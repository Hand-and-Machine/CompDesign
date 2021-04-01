import sys

new_filename = sys.argv[1]

f = open(new_filename, 'w')

with open("init_seq.gcode",'r') as init_file:
    for line in init_file:
        f.write(line)

f.write("G01 X50 Y50\n")
f.write("G01 F3000\n")
for l in range(1,300):
    f.write("G01 X50 Y100 E2.5\n")
    f.write("G04 S0.2\n")
    f.write("G01 X100 Y100 E2.5\n")
    f.write("G04 S0.2\n")
    f.write("G01 X100 Y50 E2.5\n")
    f.write("G04 S0.2\n")
    f.write("G01 X50 Y50 E2.5\n")
    f.write("G04 S0.2\n")
    f.write("G01 Z" + str(l*0.2) + "\n")

with open("final_seq.gcode",'r') as final_file:
    for line in final_file:
        f.write(line)

f.close()
