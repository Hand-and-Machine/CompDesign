exec(open("Extruder.py").read())

NUM_PILLARS = 6

ext = Extruder(100, 100, 0.6)
ext.set_density(0.05)

ext.initialize()
ext.feedrate(3000)

##ext.rect_spiral(10, 10*NUM_PILLARS, 0.5)
for p in range(NUM_PILLARS):
    ext.lift(-0.4)
    ext.goto(102, 102 + 10*p)
    ext.rect_spiral(6, 6, 0.4)
    ext.lift(0.4)

for l in range(500):
    for p in range(NUM_PILLARS):
        ext.lift(1)
        ## ext.extrude(-0.1)
        ext.goto(105, 105 + 10*p)
        ext.lift(-1)
        ext.extrude(0.1)
        ext.dwell(200)
    ext.lift(0.2)

ext.finalize()
ext.save("thinpillar-test.gcode")
