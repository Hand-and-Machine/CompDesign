## generates the vertices of a regular polygon with a given center, initial vertex, normal vector, and number of sides
def reg_polygon_pts(center, p1, normal, num_pts, adjust_sidelength=0):

	center_vec = np.asarray(center)
	p1_vec = np.asarray(p1)
	normal_vec = np.asarray(normal)
	radial_vec = p1_vec - center_vec
	radial_vec2 = np.cross(normal_vec, radial_vec) / np.linalg.norm(normal_vec)

	if adjust_sidelength != 0:
		radius = adjust_sidelength / (2 * np.sin(np.pi / num_pts))
		radial_vec = radius * radial_vec / np.linalg.norm(radial_vec)
		radial_vec2 = radius * radial_vec2 / np.linalg.norm(radial_vec2)

	pts = [center_vec + radial_vec * np.cos(2 * np.pi * i / num_pts) + radial_vec2 * np.sin(2 * np.pi * i / num_pts) for i in range(0, num_pts)]

	return pts

## finds the circumcenter of the triangle with given vertices
def circumcenter(p1, p2, p3):

	pv1 = np.asarray(p1)
	pv2 = np.asarray(p2)
	pv3 = np.asarray(p3)

	n1 = np.linalg.norm(pv3 - pv2)**2
	n2 = np.linalg.norm(pv3 - pv1)**2
	n3 = np.linalg.norm(pv2 - pv1)**2

	c1 = n1 * (n2 + n3 - n1)
	c2 = n2 * (n3 + n1 - n2)
	c3 = n3 * (n1 + n2 - n3)

	cc = (c1 * pv1 + c2 * pv2 + c3 * pv3) / (c1 + c2 + c3)
	return cc


## given three points and a distance, finds a point which is precisely that distance away from all three points (in the opposite direction of their normal vector), if possible
def equidistant_pt(p1, p2, p3, d):

	pv1 = np.asarray(p1)
	pv2 = np.asarray(p2)
	pv3 = np.asarray(p3)

	cc = circumcenter(p1, p2, p3)
	min_d = np.linalg.norm(pv1 - cc)

	if d < min_d:
		return False
	else:
		dir_vec = np.cross(pv1 - pv2, pv3 - pv2)
		height = np.sqrt(d**2 - min_d**2)
		new_pt = cc + height * dir_vec / np.linalg.norm(dir_vec)
		return new_pt



class Prism(Solid):

	def __init__(self, name, base_pts, height, topped=True):

		super().__init__(name)

		num_pts = len(base_pts)
		vec_pts = [np.asarray(p) for p in base_pts]
		vec_pts.reverse()
		normal = np.cross(vec_pts[1] - vec_pts[0], vec_pts[1] - vec_pts[2])
		height_vec = height * normal / np.linalg.norm(normal)
		otherbase_pts = [p + height_vec for p in vec_pts]
		otherbase_pts.reverse()
		
		self.add_face(vec_pts)
		if topped: self.add_face(otherbase_pts)
		for i in range(0, num_pts):
			p1 = vec_pts[i]
			p2 = vec_pts[(i + 1) % num_pts]
			self.add_face([p2, p1, p1 + height_vec, p2 + height_vec])

class Pyramid(Solid):

	def __init__(self, name, base_pts, peak, based=True):

		super().__init__(name)

		num_pts = len(base_pts)
		vec_pts = [np.asarray(p) for p in base_pts]
		normal = np.cross(vec_pts[1] - vec_pts[0], vec_pts[1] - vec_pts[2])

		if based: self.add_face(vec_pts)
		for i in range(0, num_pts):
			p1 = vec_pts[i]
			p2 = vec_pts[(i + 1) % num_pts]
			self.add_face([p2, p1, peak])


