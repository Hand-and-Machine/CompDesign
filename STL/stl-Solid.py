import os
import numpy as np

def stringify_vec(vec):
	s = ""
	for x in vec: s += str(x) + " "
	return s

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


class Solid:

	def __init__(self, name):

		self.name = name
		self.triangles = []

	## note: this only works for convex faces
	def add_face(self, pts):

		num_pts = len(pts)
		for i in range(0, num_pts-2):
			t = Triangle(pts[0], pts[i+1], pts[i+2])
			self.triangles.append(t)

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

