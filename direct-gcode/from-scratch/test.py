exec(open("Extruder.py").read())

ext = Extruder(100, 100, 0.6)
density = 0.05

ext.initialize()

ext.lift(-0.4)
for l in range(20):
    ext.drawdelta(density, 20, 0)
    ext.drawdelta(density, 0, 20)
    ext.drawdelta(density, -20, 0)
    ext.drawdelta(density, 0, -20)
    ext.lift(0.2)

ext.finalize()
ext.save("from-scratch-test.gcode")
