exec(open("Extruder.py").read())

ext = Extruder(50, 50, 0.6)
ext.set_density(0.05)

ext.initialize()

ext.lift(-0.4)
ext.rect_spiral(50, 30, 0.5)
ext.lift(0.8)

circle_coords = [(50+10*(i%6), 50+10*np.floor(i/6)) for i in range(24)]

ext.lift(0.3)
for i in range(5):
    for p in circle_coords:
        ext.goto(*p)
        ext.lift(-1)
        ext.circle(2, 20)
        ext.lift(1)
    ext.lift(0.3)

ext.lift(1)
ext.goto(50, 50)
ext.lift(-1)
ext.rect_spiral(50, 30, 0.5, dwell=100)

ext.finalize()
ext.save("wafer-test.gcode")
