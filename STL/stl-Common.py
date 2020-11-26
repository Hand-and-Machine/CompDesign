class Prism(Solid):

	def __init__(self, name, base_pts, height):

		super().__init__(name)

		num_pts = len(base_pts)
		vec_pts = [np.asarray(p) for p in base_pts]
		vec_pts.reverse()
		normal = np.cross(vec_pts[1] - vec_pts[0], vec_pts[1] - vec_pts[2])
		height_vec = height * normal / np.linalg.norm(normal)
		otherbase_pts = [p + height_vec for p in vec_pts]
		otherbase_pts.reverse()
		
		self.add_face(vec_pts)
		self.add_face(otherbase_pts)
		for i in range(0, num_pts):
			p1 = vec_pts[i]
			p2 = vec_pts[(i + 1) % num_pts]
			self.add_face([p2, p1, p1 + height_vec, p2 + height_vec])

class Pyramid(Solid):

	def __init__(self, name, base_pts, peak):

		super().__init__(name)

		num_pts = len(base_pts)
		vec_pts = [np.asarray(p) for p in base_pts]
		normal = np.cross(vec_pts[1] - vec_pts[0], vec_pts[1] - vec_pts[2])

		self.add_face(vec_pts)
		for i in range(0, num_pts):
			p1 = vec_pts[i]
			p2 = vec_pts[(i + 1) % num_pts]
			self.add_face([p2, p1, peak])


