## Solid Example 2
## The convex hull of some points.

exec(open("loader-0.2.py").read())

# Some points
pts = [
    (-1,1,2),
    (1,-1,2),
    (1,1,-2),
    (-2,1,1),
    (2,-1,1),
    (2,1,-1),
    (-1,2,1),
    (1,-2,1),
    (1,2,-1)
]

# Create a solid as the convex hull of these points
ch = ConvexSolid.hull("example2", pts)

ch.build().gen_file()
