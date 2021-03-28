exec(open("Extruder.py").read())

NUM_PILLARS = 6
BASE_X = 50
BASE_Y = 50
EXTRA_PILLAR_LAYERS = 5
LAYER_HEIGHT = 0.2

ext = Extruder(BASE_X, BASE_Y, 0.6)
ext.set_density(0.05)

ext.initialize()
ext.feedrate(3000)

##ext.rect_spiral(10, 10*NUM_PILLARS, 0.5)

ext.goto(BASE_X, BASE_Y - 10)
ext.lift(-0.4)
ext.rect_spiral(10, 10, 0.4)
ext.lift(0.4)

for p in range(NUM_PILLARS):
    ext.goto(BASE_X + 2, BASE_Y + 2 + 10*p)
    ext.lift(-0.4)
    ext.rect_spiral(6, 6, 0.4)
    ext.lift(0.4)

ext.goto(BASE_X, BASE_Y + 10*NUM_PILLARS)
ext.lift(-0.4)
ext.rect_spiral(10, 10, 0.4)
ext.lift(0.4)

clearance = LAYER_HEIGHT*EXTRA_PILLAR_LAYERS

## Get a headstart on the thin middle pillars
ext.feedrate(3000)
for l in range(EXTRA_PILLAR_LAYERS):
    for p in range(NUM_PILLARS):
        ext.lift(1)
        ## ext.extrude(-0.1)
        ext.goto(BASE_X + 5, BASE_Y + 5 + 10*p)
        ext.lift(-1)
        ext.extrude(0.05)
        ext.dwell(200)
    ext.lift(LAYER_HEIGHT)
ext.lift(1)
ext.goto(BASE_X, BASE_Y)
ext.lift(-clearance-1)


## Draw all of the pillars while weaving between pillars
starting_thread_offset = 4
for l in range(300):

    ## First rectangular pillar
    ext.lift(clearance+1)
    ext.goto(BASE_X + 2, BASE_Y - 8)
    ext.feedrate(500)
    ext.lift(-clearance-1)
    ext.rectangle(6, 6)

    ## All of the thin circular pillars
    ext.feedrate(3000)
    ext.lift(clearance)
    for p in range(NUM_PILLARS):
        ext.lift(1)
        ## ext.extrude(-0.1)
        ext.goto(BASE_X + 5, BASE_Y + 5 + 10*p)
        ext.lift(-1)
        ext.extrude(0.05)
        ext.dwell(200)
    ext.lift(-clearance)

    ## Second rectangular pillar
    ext.lift(clearance+1)
    ext.goto(BASE_X + 2, BASE_Y + 10*NUM_PILLARS + 2)
    ext.feedrate(500)
    ext.lift(-clearance-1)
    ext.rectangle(6, 6)

    ## Filament woven between the pillars
    if (l % 5 == 0):
        ext.feedrate(1000)
        thread_offset = starting_thread_offset
        starting_thread_offset = -starting_thread_offset
        for p in range(NUM_PILLARS):
            rp = NUM_PILLARS - p - 1
            thread_offset = -thread_offset
            ext.drawline(BASE_X + 5 + thread_offset, BASE_Y + 5 + 10*rp)
        ext.drawline(BASE_X + 5, BASE_Y)
    else:
        ext.feedrate(3000)
        ext.lift(clearance+1)
        ext.goto(BASE_X, BASE_Y)
        ext.lift(-clearance-1)

    ext.lift(LAYER_HEIGHT)

ext.finalize()
ext.save("weaving-test.gcode")
