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


	def shift_ids(self, num):

		for id in self.vertices: id += num

class Solid:

	def __init__(self, name, error=1.0E-7):

		self.name = name
		self.error = error
		self.triangles = []
		self.vertices = []
		self.num_vertices = 0
		self.edges = []
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
		self.edges.append(set())
		return self.num_vertices - 1

	## adds an edge to the solid
	## edges are stored redundantly - once under each vertex
	def add_edge(self, v_id, w_id):

		if max(v_id, w_id) >= self.num_vertices: return False
		self.edges[v_id].add(w_id)
		self.edges[w_id].add(v_id)

	# adds a new (oriented) face to the solid, along with any necessary new vertices
	# pts is a list of points (tuples) and ints, where the ints refer to preexisting points in the solid
	def add_face(self, pts):

		num_pts = len(pts)
		vertex_ids = [ self.add_vertex(p.copy()) for p in pts ]

		face = Face(vertex_ids)
		self.faces.append(face)

		for i in range(0, num_pts):
			self.add_edge(vertex_ids[i], vertex_ids[(i + 1) % num_pts])

	def translate(self, trans):

		for v in self.vertices: v += np.asarray(trans)

	def join_solid(self, solid):

		for f in solid.faces:
			pts = [solid.vertices[id].copy() for id in f.vertices]
			self.add_face(pts)

	def overwrite(self, solid):

		self.triangles = []
		self.vertices = []
		self.num_vertices = 0
		self.edges = []
		self.faces = []

		self.join_solid(solid)

	def plane_slice(self, plane_point, plane_normal):

		s = Solid(self.name, error=self.error)

		sliced_vertices = []
		for id in range(0, self.num_vertices):
			if side_of_plane(self.vertices[id], plane_point, plane_normal): 
				sliced_vertices.append(id)

		intermediate_vertices = [{} for v in self.vertices]
		all_intermediate_vertices = []
		num_intermediate_vertices = 0
		edge_dict = [d.copy() for d in self.edges]
		center_vec = np.array((0.0,0.0,0.0))
		for id1 in range(0, self.num_vertices):
			for id2 in edge_dict[id1]:
				if id1 < id2:
					v1 = self.vertices[id1]
					v2 = self.vertices[id2]
					if (id1 in sliced_vertices) != (id2 in sliced_vertices):
						intermediate_vertex = segment_intersect_plane(v1, v2, plane_point, plane_normal)
						intermediate_vertices[id1][id2] = intermediate_vertex
						intermediate_vertices[id2][id1] = intermediate_vertex
						all_intermediate_vertices.append(intermediate_vertex)
						num_intermediate_vertices += 1
						center_vec += intermediate_vertex
		center_vec = center_vec / num_intermediate_vertices

		for f in self.faces:
			new_pts = []
			for i in range(0, f.num_sides):
				j = (i + 1) % f.num_sides
				id1 = f.vertices[i]
				id2 = f.vertices[j]
				if (id2 in sliced_vertices) != (id1 in sliced_vertices):
					new_pts.append(intermediate_vertices[id1][id2])
					if id2 not in sliced_vertices:
						new_pts.append(self.vertices[id2])
				elif id2 not in sliced_vertices:
					new_pts.append(self.vertices[id2])
			if new_pts:
				s.add_face(new_pts)

		displacement_vecs = [v - center_vec for v in all_intermediate_vertices]
		if displacement_vecs: 
			ordered_displacement_vecs = counterclockwise_order(plane_normal, displacement_vecs)
			ordered_intermediate_points = [v + center_vec for v in ordered_displacement_vecs]
			s.add_face(ordered_intermediate_points)

		return s

	def truncate(self, proportion):

		s = Solid(self.name, error=1.0E-14)
		s.join_solid(self)

		for id in range(0, self.num_vertices):

			cut_vertex = np.asarray(self.vertices[id])
			adjacent_vertices = [np.asarray(self.vertices[edge_id]) for edge_id in self.edges[id]]
			edge_vecs = [cut_vertex - av for av in adjacent_vertices]
			cut_normal = sum(edge_vecs)
			projections = [abs(np.dot(ev, cut_normal)) / np.linalg.norm(cut_normal) for ev in edge_vecs]
			cut_distance = proportion * min(projections)
			cut_point = cut_vertex - cut_distance * cut_normal / np.linalg.norm(cut_normal)

			s.overwrite(s.plane_slice(cut_point, cut_normal))

		return s

	def build_face(self, face):

		pts = [ self.vertices[id] for id in face.vertices ]
		num_pts = len(pts)

		# generate triangles for STL file
		for i in range(0, num_pts-2):
			t = Triangle(pts[0], pts[i+1], pts[i+2])
			self.triangles.append(t)

	def build(self):

		self.triangles = []
		for f in self.faces: 
			self.build_face(f)

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
