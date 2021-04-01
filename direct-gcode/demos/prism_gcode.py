import sys
import math

## Parameters for the print
CENTER_X = 100
CENTER_Y = 100
RADIUS = 20
NUM_SIDES = 7
LAYERS = 300
LAYER_HEIGHT = 0.2
DENSITY = 0.05

## Calculate the points on the regular polygon
polygon_pts = [(CENTER_X + RADIUS*math.cos(2*math.pi*i/NUM_SIDES), CENTER_Y + RADIUS*math.sin(2*math.pi*i/NUM_SIDES)) for i in range(NUM_SIDES)]

## Get the side length of the polygon, and calculate how much extrusion
## is needed for one side, using the provided DENSITY value.
p0 = polygon_pts[0]
p1 = polygon_pts[1]
dist = math.sqrt((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)
extrusion = dist*DENSITY

new_filename = sys.argv[1]

f = open(new_filename, 'w')

## Write initialization sequence
with open("init_seq.gcode",'r') as init_file:
    for line in init_file:
        f.write(line)

## Move the extruder to the first point, and set the feedrate
f.write("G01 X" + str(p0[0]) + " Y" + str(p0[1]) + "\n")
f.write("G01 F3000\n")

## Loop over the number of layers
for l in range(1,NUM_LAYERS):
    ## Loop over the number of sides on the polygon
    for n in range(NUM_SIDES):
        p = polygon_pts[n]
        f.write("G01 X" + str(p[0]) + " Y" + str(p[1]) + " E" + str(extrusion) + "\n")
        f.write("G04 S0.2\n")
    f.write("G01 Z" + str(l*LAYER_HEIGHT) + "\n")

## Write the finalization sequence
with open("final_seq.gcode",'r') as final_file:
    for line in final_file:
        f.write(line)

f.close()
