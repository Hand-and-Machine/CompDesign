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
		self.vertex_lookup = { vertex_ids[index]: index for index in range(self.num_sides) }
		self.edges = [(vertex_ids[i], vertex_ids[(i + 1) % self.num_sides]) for i in range(0, self.num_sides)]

	def center(self, vertices):

		center = sum([np.asarray(vertices[id]) for id in self.vertices]) / self.num_sides
		return center

	def normal(self, vertices):

		p0 = np.asarray(vertices[self.vertices[0]])
		p1 = np.asarray(vertices[self.vertices[1]])
		p2 = np.asarray(vertices[self.vertices[2]])
		v0 = p0 - p1
		v1 = p1 - p2
		normal = np.cross(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1))

		return normal

	def next_vert(self, id):

		index = self.vertex_lookup[id]
		n = self.num_sides

		return self.vertices[(index + 1) % n]

	def prev_vert(self, id):

		index = self.vertex_lookup[id]
		n = self.num_sides

		return self.vertices[(index - 1) % n]

	def adjacent_verts(self, id):

		return [self.prev_vert(id), self.next_vert(id)]

	def replace_vertex(self, id, vertices, replacements):

		new_vertices = []

		for i in self.vertices:
			if i == id:
				new_vertices += replacements
			else:
				new_vertices += [vertices[i]]

		return new_vertices

class Solid:

	def __init__(self, name, error=1.0E-7):

		self.name = name
		self.error = error
		self.triangles = []
		self.vertices = []
		self.num_vertices = 0
		self.edges = []
		self.faces = []
		self.faces_by_vertex = []
		self.faces_by_edge = []
		self.face_normals = {}

	## adds a vertex to the solid if it does not already exist... within a margin of error
	## and returns its index in the self.vertices array (these are the IDs of these vertices)
	def add_vertex(self, v, check_equality=True):

		if type(v) == int: return v

		match = False
		if check_equality:
			for i in range(0, len(self.vertices)):
				if distance(v, self.vertices[i]) < self.error: 
					match = True
					return i

		if not match:
			self.vertices.append(np.asarray(v))
			self.num_vertices += 1
			self.edges.append(set())
			self.faces_by_vertex.append([])
			self.faces_by_edge.append({})
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

		# failsafe to protect against duplicate entries
		checked_vertex_ids = []
		for i in range(0, num_pts):
			if vertex_ids[(i + 1) % num_pts] != vertex_ids[i]:
				checked_vertex_ids.append(vertex_ids[i])
		num_pts = len(checked_vertex_ids)
		vertex_ids = checked_vertex_ids

		face = Face(vertex_ids)
		self.faces.append(face)

		for i in range(0, num_pts):
			self.add_edge(vertex_ids[i], vertex_ids[(i + 1) % num_pts])
			self.faces_by_vertex[vertex_ids[i]].append(face)
			self.faces_by_edge[vertex_ids[i]][vertex_ids[(i + 1) % num_pts]] = face

		self.face_normals[face] = face.normal(self.vertices)

	def add_face_unordered(self, pts, interior_pt):

		num_pts = len(pts)

		pvs = [np.asarray(p) for p in pts]
		ipv = np.asarray(interior_pt)
		cv = sum(pvs) / num_pts
		nv = cv - ipv
		offset_vecs = [pv - ipv for pv in pvs]
		ordered_offset_vecs = counterclockwise_order(nv, offset_vecs)
		ordered_pvs = [ipv + ov for ov in ordered_offset_vecs]

		self.add_face(ordered_pvs)

	def copy(self):

		s = Solid(self.name)

		for f in self.faces:
			s.add_face([self.vertices[id] for id in f.vertices])
		
		return s

	def center(self):

		center = sum([np.asarray(v) for v in self.vertices]) / self.num_vertices
		return center

	def faces_with_edge(self, id1, id2):

		faces_list = []

		for f in self.faces:
			if id1 in f.vertices and id2 in f.vertices:
				faces_list.append(f)
		
		return faces_list

	## returns the edges in counterclockwise order, pointing towards the vertex in question
	## might not work for "floating" faces or vertices
	def adjacent_vertices_sorted(self, id):

		adj_verts = []
		num_verts = 0
		degree = len(self.edges[id])

		v_id = next(iter(self.edges[id]))
		original_v_id = v_id

		while num_verts < degree:
			
			adj_verts.append(v_id)
			num_verts += 1

			face = self.faces_by_edge[id][v_id]
			v_id = face.prev_vert(id)

		return adj_verts

	def translate(self, trans):

		for v in self.vertices: v += np.asarray(trans)

	def origin_dilate(self, factor):

		for v in self.vertices: v = v * factor

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

	## currently only supported for convex solids
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

	def conway_dual(self):

		s = Solid(self.name)

		for id in range(0, self.num_vertices):

			adj_faces = self.faces_by_vertex[id]
			adj_centers = [np.asarray(f.center(self.vertices)) for f in adj_faces]
			solid_center = self.center()

			s.add_face_unordered(adj_centers, solid_center)

		return s


	def conway_kis(self, distance):

		s = Solid(self.name)
		pts = self.vertices

		for f in self.faces:

			center = f.center(pts)
			normal = self.face_normals[f]
			peak = center + distance * normal

			for i in range(0, f.num_sides):

				p0 = pts[f.vertices[i]]
				p1 = pts[f.vertices[(i + 1) % f.num_sides]]
				triangle_pts = [peak, p0, p1]

				s.add_face(triangle_pts)

		return s

	def conway_truncate(self, distance):

		s = self.copy()
		vertices = self.vertices

		for v in vertices:
			s = s.truncate_vertex(s.add_vertex(v), distance)

		return s

	def truncate_vertex(self, id, distance):

		s = Solid(self.name)
		v = np.asarray(self.vertices[id])

		edge_vecs = {id2: v - np.asarray(self.vertices[id2]) for id2 in self.adjacent_vertices_sorted(id)}
		unit_edge_vecs = {id2: edge_vecs[id2] / np.linalg.norm(edge_vecs[id2]) for id2 in edge_vecs}
		normal = sum([unit_edge_vecs[id2] for id2 in unit_edge_vecs])
		normal = normal / np.linalg.norm(normal)
		cut_normal = -normal
		edge_cutoffs = [1/np.dot(unit_edge_vecs[id2], normal) for id2 in unit_edge_vecs]
		max_edge_cutoff = max(edge_cutoffs)
		cut_normal = cut_normal * distance / max_edge_cutoff
		disp_vecs = {id2: unit_edge_vecs[id2] * np.linalg.norm(cut_normal)**2 / np.dot(unit_edge_vecs[id2], cut_normal) for id2 in unit_edge_vecs}
		cut_pts = {id2: v + disp_vecs[id2] for id2 in disp_vecs}
		face_normal = sum([self.face_normals[f] for f in self.faces if id in f.vertices])
		s.add_face([cut_pts[id2] for id2 in cut_pts])
		
		for f in self.faces:

			vertices = [self.vertices[i] for i in f.vertices]
			if id in f.vertices:
				adj_ids = f.adjacent_verts(id)
				new_verts = [cut_pts[id2] for id2 in adj_ids]
				new_face = f.replace_vertex(id, self.vertices, new_verts)
				s.add_face(new_face)				
			else:
				s.add_face(vertices)

		return s

	def conway_expand(self, distance):

		s = Solid(self.name)

		center = self.center()
		pushed_vertices = { f: { id: np.asarray((0, 0, 0)) for id in f.vertices } for f in self.faces }

		for f in self.faces:

			face_center = f.center(self.vertices)
			trans_vec = face_center - center
			trans_vec = trans_vec * distance / np.linalg.norm(trans_vec)
			trans_verts = []

			for id in f.vertices:
				trans_vert = np.asarray(self.vertices[id]) + trans_vec
				trans_verts.append(trans_vert)
				pushed_vertices[f][id] = trans_vert

			s.add_face(trans_verts)

		for id in range(0, self.num_vertices):

			pushed_copies = [ pushed_vertices[f][id] for f in pushed_vertices if id in pushed_vertices[f]]
			s.add_face_unordered(pushed_copies, center)

		for id1 in range(0, len(self.edges)):
			for id2 in self.edges[id1]:
				if id1 < id2:

					f1, f2 = self.faces_with_edge(id1, id2)
					e1 = [pushed_vertices[f1][id1], pushed_vertices[f1][id2]]
					e2 = [pushed_vertices[f2][id1], pushed_vertices[f2][id2]]
					s.add_face_unordered(e1 + e2, center)

		return s


	def build_face(self, face):

		pts = [ self.vertices[id] for id in face.vertices ]
		num_pts = face.num_sides
		center = sum([np.asarray(p) for p in pts]) / num_pts

		# generate triangles for STL file
		for i in range(0, num_pts):
			t = Triangle(center, pts[i], pts[(i+1) % num_pts])
			self.triangles.append(t)

	def build(self):

		self.triangles = []
		for f in self.faces: 
			self.build_face(f)

		return self

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

		return self
