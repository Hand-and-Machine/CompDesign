exec(open("Extruder.py").read())

ext = Extruder(100, 100, 0.6)
ext.set_density(0.05)

ext.initialize()

ext.lift(-0.4)
ext.rect_spiral(50, 100, 0.5)
ext.lift(0.4)

ext.finalize()
ext.save("rectspiral-test.gcode")
