## Solid Example 1
## A tetrahedron with four vertices lying on the coordinate axes.

exec(open("loader-0.2.py").read())

# Create an empty solid
s = Solid("example1")

# The four vertices of the tetrahedron
p1 = (0,0,0)
p2 = (1,0,0)
p3 = (0,1,0)
p4 = (0,0,1)

# The order of the vertices matters!
s.add_face([p1, p3, p2])
s.add_face([p1, p2, p4])
s.add_face([p1, p4, p3])
s.add_face([p2, p3, p4])

s.build().gen_file()
