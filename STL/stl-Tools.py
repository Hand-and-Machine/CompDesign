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


## given three points and a distance, finds a point which is precisely that distance away from all three points (in the opposite direction of their normal vector)
## this is not always possible - if impossible, it returns False
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

## see documentation
def fold_up(p1, p2, p3, theta, phi, length):

	pv1 = np.asarray(p1)
	pv2 = np.asarray(p2)
	pv3 = np.asarray(p3)
	v1 = pv1 - pv2
	v2 = pv3 - pv2
	normal = np.cross(v1, v2)
	unit_normal = normal / np.linalg.norm(normal)

	u1 = v1
	u2 = v2 - v1 * np.dot(v1, v2) / np.linalg.norm(v1)**2
	proj1 = np.cos(theta)
	proj2 = np.cos(phi) * np.linalg.norm(v2) / np.linalg.norm(u2) - np.cos(theta) * np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(u2))
	proj3 = np.sqrt(1 - proj1**2 - proj2**2)
	x = u1 * proj1 / np.linalg.norm(u1) + u2 * proj2 / np.linalg.norm(u2) + unit_normal * proj3

	return pv2 + x * length

# given 3 points of a regular polygon and the number of points, finds the rest of the points
def complete_reg_polygon(p1, p2, p3, num_pts):

	pv1 = np.asarray(p1)
	pv2 = np.asarray(p2)
	cc = circumcenter(p1, p2, p3)
	cv = np.asarray(cc)
	rv1 = pv1 - cv
	rv2 = pv2 - cv
	rv3 = rv2 - rv1 * np.dot(rv1, rv2) / np.linalg.norm(rv1)**2
	rv3 = rv3 * np.linalg.norm(rv1) / np.linalg.norm(rv3)

	pts = [cv + rv1 * np.cos(2 * np.pi * i / num_pts) + rv3 * np.sin(2 * np.pi * i / num_pts) for i in range(0, num_pts)]

	return pts

# rotates a set of points counterclockwise about an oriented line defined by a point and vector
def rotate_points_about_line(points, base_pt, vec, theta):

	pvs = [np.asarray(p) for p in points]
	bpv = np.asarray(base_pt)
	lv = np.asarray(vec)
	new_pvs = []

	for pv in pvs:
		diffv = pv - bpv
		diffproj = np.dot(diffv, lv) / np.linalg.norm(lv)**2
		projv = bpv + diffproj
		rv1 = pv - projv
		rv2 = np.cross(lv, rv1) / np.linalg.norm(lv)
		new_pv = projv + rv1 * np.cos(theta) + rv2 * np.sin(theta)
		new_pvs.append(new_pv)

	return new_pvs

## gives the counterclockwise angle between two vectors' projections into the plane defined by a given normal vector
def angle_in_plane(normal, vec1, vec2):

	normal_vec = np.asarray(normal)
	v1 = np.asarray(vec1)
	v2 = np.asarray(vec2)

	proj1 = v1 - normal_vec * np.dot(v1, normal_vec) / np.linalg.norm(normal_vec)**2
	proj2 = v2 - normal_vec * np.dot(v2, normal_vec) / np.linalg.norm(normal_vec)**2
	cos = np.dot(proj1, proj2) / (np.linalg.norm(proj1) * np.linalg.norm(proj2))
	angle = np.arccos(min(1, max(-1, cos)))
	if np.dot(normal_vec, np.cross(proj1, proj2)) < 0: angle = 2 * np.pi - angle

	return angle

## sorts a list of vectors in counterclockwise order around a normal
def counterclockwise_order(normal_vec, vecs, vec_ids=False):

	base_vec = vecs[0]

	if vec_ids != False:
		return sorted(vec_ids, key = lambda id: angle_in_plane(normal_vec, base_vec, vecs[id]))
	else:
		return sorted(vecs, key = lambda v: angle_in_plane(normal_vec, base_vec, v))

## given a point and normal vector defining a plane and a second point, 
## checks whether the second point is on the side of the plane indicated by the vector
def side_of_plane(check_point, plane_point, plane_normal):

	ppv = np.asarray(plane_point)
	nv = np.asarray(plane_normal)
	cpv = np.asarray(check_point)

	return np.dot(nv, cpv - ppv) > 0

## finds the point at which a line segment intersects a plane
## or returns False, if no such point exists
def segment_intersect_plane(point1, point2, plane_point, plane_normal):

	if side_of_plane(point1, plane_point, plane_normal) == side_of_plane(point2, plane_point, plane_normal):
		return False

	pv1 = np.asarray(point1)
	pv2 = np.asarray(point2)
	ppv = np.asarray(plane_point)
	nv = np.asarray(plane_normal)
	dv = pv2 - pv1

	coef1 = abs(np.dot(pv1 - ppv, nv) / np.linalg.norm(nv))
	coef2 = abs(np.dot(pv2 - ppv, nv) / np.linalg.norm(nv))

	return (coef2 * pv1 + coef1 * pv2) / (coef1 + coef2)