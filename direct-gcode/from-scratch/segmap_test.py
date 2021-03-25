exec(open("Extruder.py").read())
exec(open("tools.py").read())

square_segs = [
    [(100,100),(130,100)],
    [(130,100),(130,130)],
    [(130,130),(100,130)],
    [(100,130),(100,100)]
]

props = [1/16, 3/16, 5/16, 7/16, 9/16, 11/16, 13/16, 15/16]

segmap = segment_map(square_segs)

ext = Extruder(100, 100, 0.6)
density = 0.05

ext.initialize()

ext.lift(-0.4)
for l in range(200):
    progress = l/100
    points = [segmap(prop) for prop in props]
    
    ext.lift(0.2)
    ext.goto(*points[0])
    ext.lift(-0.2)
    ext.drawline(density, *points[1])
    ext.drawline(density, *points[4])
    ext.drawline(density, *points[5])
    ext.drawline(density, *points[0])

    ext.lift(0.2)
    ext.goto(*points[2])
    ext.lift(-0.2)
    ext.drawline(density, *points[3])
    ext.drawline(density, *points[6])
    ext.drawline(density, *points[7])
    ext.drawline(density, *points[2])
    
    ext.lift(0.2)

ext.finalize()
ext.save("segmap-cube-test.gcode")
