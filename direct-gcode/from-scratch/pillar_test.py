exec(open("Extruder.py").read())

ext = Extruder(100, 100, 0.6)
ext.set_density(0.05)

ext.initialize()

ext.lift(-0.4)
ext.rect_spiral(150, 20, 0.6)
ext.lift(0.4)

ext.lift(0.8)
for l in range(100):
    ## ext.lift(-0.2)
    ext.goto(105, 105)
    ext.rectangle(5, 10)
    ext.lift(0.2)
    ## ext.extrude(-1)
    ext.goto(240, 105)
    ext.lift(-0.2)
    ext.rectangle(5, 10)
    ext.lift(0.7)
    ## ext.extrude(-1)
    ## ext.dwell(100)

ext.finalize()
ext.save("pillar-test.gcode")
