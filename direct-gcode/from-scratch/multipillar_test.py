exec(open("Extruder.py").read())

NUM_PILLARS = 6
BASE_X = 50
BASE_Y = 50

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

for l in range(300):
    ext.lift(1)
    ext.goto(BASE_X + 2, BASE_Y - 8)
    ext.feedrate(500)
    ext.lift(-1)
    ext.rectangle(6, 6)

    ext.feedrate(3000)
    for p in range(NUM_PILLARS):
        ext.lift(1)
        ## ext.extrude(-0.1)
        ext.goto(BASE_X + 5, BASE_Y + 5 + 10*p)
        ext.lift(-1)
        ext.extrude(0.1)
        ext.dwell(200)

    ext.lift(1)
    ext.goto(BASE_X + 2, BASE_Y + 10*NUM_PILLARS + 2)
    ext.feedrate(500)
    ext.lift(-1)
    ext.rectangle(6, 6)

    ext.lift(0.2)

ext.finalize()
ext.save("multipillar-test.gcode")
