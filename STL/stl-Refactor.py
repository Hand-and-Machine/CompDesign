import os
import numpy as np

def stringify_vec(vec):
	s = ""
	for x in vec: s += str(x) + " "
	return s

def distance(p1, p2):
	p1v = np.asarray(p1)
	p2v = np.asarray(p2)
	return np.linalg.norm(p1v - p2v)

class Triangle:

	def __init__(self, pt1, pt2, pt3):

		self.p1 = np.asarray(pt1)
		self.p2 = np.asarray(pt2)
		self.p3 = np.asarray(pt3)
		cross = np.cross(self.p3 - self.p2, self.p1 - self.p2)
		self.normal = cross / np.linalg.norm(cross)

	def to_stl(self):

		stl_str = []
		stl_str.append("facet normal " + stringify_vec(self.normal))
		stl_str.append("outer loop")
		stl_str.append("vertex " + stringify_vec(self.p1))
		stl_str.append("vertex " + stringify_vec(self.p2))
		stl_str.append("vertex " + stringify_vec(self.p3))
		stl_str.append("endloop")
		stl_str.append("endfacet")
		return stl_str

class Face:

	def __init__(self, vertex_ids):

		self.vertices = vertex_ids
		self.num_sides = len(vertex_ids)
		self.edges = [(vertex_ids[i], vertex_ids[(i + 1) % self.num_sides]) for i in range(0, self.num_sides)]


	def shift_ids(num):

		for id in self.vertices: id += num

class Solid:

	def __init__(self, name, error=1.0E-7):

		self.name = name
		self.error = error
		self.triangles = []
		self.vertices = []
		self.num_vertices = 0
		self.faces = []

	## adds a vertex to the solid if it does not already exist... within a margin of error
	## and returns its index in the self.vertices array (these are the IDs of these vertices)
	def add_vertex(self, v, check_equality=True):

		if type(v) == int: return v

		if check_equality:
			for i in range(0, len(self.vertices)):
				if distance(v, self.vertices[i]) < self.error: return i
		self.vertices.append(np.asarray(v))
		self.num_vertices += 1
		return self.num_vertices - 1

	# adds a new (oriented) face to the solid, along with any necessary new vertices
	# pts is a list of points (tuples) and ints, where the ints refer to preexisting points in the solid
	def add_face(self, pts):

		vertex_ids = [ self.add_vertex(p) for p in pts ]

		face = Face(vertex_ids)
		self.faces.append(face)

	def translate(self, trans):

		for v in self.vertices: v += np.asarray(trans)

	def build_face(self, face):

		pts = [ self.vertices[id] for id in face.vertices ]
		num_pts = len(pts)

		# generate triangles for STL file
		for i in range(0, num_pts-2):
			t = Triangle(pts[0], pts[i+1], pts[i+2])
			self.triangles.append(t)

	def build(self):

		self.triangles = []
		for f in self.faces: self.build_face(f)

	## danger! this will overwrite files
	def gen_file(self):

		filename = self.name + ".stl"
		if os.path.exists(filename): os.remove(filename)
		f = open(filename, "a")

		filetext = []
		filetext.append("solid " + self.name)
		for t in self.triangles: filetext = filetext + t.to_stl()
		filetext.append("endsolid " + self.name)
		
		for l in filetext: 
			f.write(l+"\n")
		f.close()
