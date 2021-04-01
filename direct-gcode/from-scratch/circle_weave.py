exec(open("Extruder.py").read())

## Parameters for the print
NUM_PILLARS = 14
BASE_X = 100
BASE_Y = 100
LAYER_HEIGHT = 0.2
LAYER_THICKNESS = 0.1
EXTRA_PILLAR_LAYERS = 5
RADIUS = 30

## Points on the unit circle
CIRC_X = [math.cos(2*math.pi*i/NUM_PILLARS) for i in range(NUM_PILLARS)]
CIRC_Y = [math.sin(2*math.pi*i/NUM_PILLARS) for i in range(NUM_PILLARS)]

## Set up the extruder
ext = Extruder(BASE_X, BASE_Y, 0.6)
ext.set_density(0.05)
ext.initialize()
ext.feedrate(3000)

## Draw pillar bases
for p in range(NUM_PILLARS):
    x = BASE_X + RADIUS*CIRC_X[p] - 3
    y = BASE_Y + RADIUS*CIRC_Y[p] - 3
    ext.goto(x, y)
    ext.lift(-0.4)
    ext.rect_spiral(6, 6, 0.4)
    ext.lift(0.4)

## Get a headstart on the pillars
for l in range(EXTRA_PILLAR_LAYERS):
    for p in range(NUM_PILLARS):
        x = BASE_X + RADIUS*CIRC_X[p]
        y = BASE_Y + RADIUS*CIRC_Y[p]
        ext.lift(1)
        ext.goto(x, y)
        ext.lift(-1)
        ext.extrude(LAYER_THICKNESS)
        ext.dwell(200)
    ext.lift(LAYER_HEIGHT)

## Draw all of the pillars while weaving between pillars
starting_thread_offset = 6
clearance = EXTRA_PILLAR_LAYERS*LAYER_HEIGHT
for l in range(300):

    ## All of the thin circular pillars
    ext.feedrate(3000)
    ext.lift(clearance)
    for p in range(NUM_PILLARS):
        x = BASE_X + RADIUS*CIRC_X[p]
        y = BASE_Y + RADIUS*CIRC_Y[p]
        ext.lift(1)
        ext.goto(x, y)
        ext.lift(-1)
        ext.extrude(LAYER_THICKNESS)
        ext.dwell(200)
    ext.goto(BASE_X + (RADIUS+starting_thread_offset), BASE_Y)
    ext.lift(-clearance)

    ## Filament woven between the pillars
    if (l % 5 == 0):
        ext.feedrate(1000)
        thread_offset = starting_thread_offset
        starting_thread_offset = -starting_thread_offset
        ext.lift(clearance)
        for p in range(1,NUM_PILLARS+1):
            x = BASE_X + (RADIUS+thread_offset)*CIRC_X[p % NUM_PILLARS]
            y = BASE_Y + (RADIUS+thread_offset)*CIRC_Y[p % NUM_PILLARS]
            thread_offset = -thread_offset
            ext.drawline(x, y, l*LAYER_HEIGHT)

    ext.lift(LAYER_HEIGHT)

ext.finalize()
ext.save("circle-weave.gcode")
