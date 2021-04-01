exec(open("Extruder.py").read())

ext = Extruder(50, 50, 0.2)
ext.set_density(0.05)
ext.initialize()
ext.feedrate(3000)

for l in range(300):
    ext.drawline(50, 100)
    ext.drawline(100, 100)
    ext.drawline(100, 50)
    ext.drawline(50, 50)
    ext.lift(0.2) 

ext.finalize()
ext.save("square-prism.gcode")
