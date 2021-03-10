## Here's a key for the different ID numbers of Platonic solids:
## 1 - regular tetrahedron
## 2 - regular octahedron
## 3 - cube
## 4 - regular dodecahedron
## 5 - regular icosahedron

class PlatonicSolid(Solid):

	def __init__(self, name, id, sidelength):
		
		super().__init__(name)

		if id == 1:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 3, adjust_sidelength=sidelength)
			peak = equidistant_pt(base_pts[0], base_pts[1], base_pts[2], sidelength) ## (0, 0, np.sqrt(2/3))
			th = Pyramid("temp", base_pts, peak)

			self.join_solid(th)

		elif id == 2:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 4, adjust_sidelength=sidelength)
			peak = equidistant_pt(base_pts[0], base_pts[1], base_pts[2], sidelength)
			top_pm = Pyramid("temp", base_pts, peak, based=False)
			base_pts.reverse()
			bottom_pm = Pyramid("temp", base_pts, -peak, based=False)

			self.join_solid(top_pm)
			self.join_solid(bottom_pm)

		elif id == 3:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, 1), 4, adjust_sidelength=sidelength)
			cb = RightPrism("temp", base_pts, sidelength)

			self.join_solid(cb)

		elif id == 4:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 5, adjust_sidelength=sidelength)
			bottom_half_faces = [base_pts]
			top_half_faces = []

			for i in range(0, 5):
				inclined_pt = fold_up(base_pts[i], base_pts[(i + 1) % 5], base_pts[(i + 2) % 5], 3 * np.pi / 5, 3 * np.pi / 5, sidelength)
				bottom_face_pts = complete_reg_polygon(inclined_pt, base_pts[(i + 1) % 5], base_pts[i], 5)
				bottom_half_faces.append(bottom_face_pts)

			for i in range(0,5):
				bottom_face = bottom_half_faces[i + 1]
				inclined_pt = fold_up(bottom_face[-2], bottom_face[-1], bottom_face[0], 3 * np.pi /5, 3 * np.pi / 5, sidelength)
				top_face_pts = complete_reg_polygon(bottom_face[0], bottom_face[-1], inclined_pt, 5)
				top_half_faces.append(top_face_pts)

			tophalf_face = top_half_faces[0]
			inclined_pt = fold_up(tophalf_face[2], tophalf_face[3], tophalf_face[4], 3 * np.pi / 5, 3 * np.pi / 5, sidelength)
			topface = complete_reg_polygon(inclined_pt, tophalf_face[3], tophalf_face[2], 5)
			top_half_faces.append(topface)

			for f in bottom_half_faces: self.add_face(f)
			for f in top_half_faces: self.add_face(f)

		elif id == 5:

			middle_bottom_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 5, adjust_sidelength=sidelength)
			bottom_pt = equidistant_pt(middle_bottom_pts[0], middle_bottom_pts[1], middle_bottom_pts[2], sidelength)
			bottom_faces = []

			for i in range(0, 5):
				bottom_faces.append([middle_bottom_pts[(i + 1) % 5], middle_bottom_pts[i], bottom_pt])

			middle_top_pts = []
			for i in range(0, 5):
				pent_pts = complete_reg_polygon(middle_bottom_pts[i], bottom_pt, middle_bottom_pts[(i + 2) % 5], 5)
				middle_top_pts.append(pent_pts[-1])

			middle_faces = []
			for i in range(0, 5):
				middle_faces.append([middle_bottom_pts[i], middle_bottom_pts[(i + 1) % 5], middle_top_pts[i]])
				middle_faces.append([middle_bottom_pts[(i + 1) % 5], middle_top_pts[(i + 1) % 5], middle_top_pts[i]])

			top_pt = equidistant_pt(middle_top_pts[2], middle_top_pts[1], middle_top_pts[0], sidelength)
			top_faces = []

			for i in range(0, 5):
				top_faces.append([middle_top_pts[i], middle_top_pts[(i + 1) % 5], top_pt])

			for f in bottom_faces: self.add_face(f)
			for f in middle_faces: self.add_face(f)
			for f in top_faces: self.add_face(f)

			self.translate(-bottom_pt)

## Key for the ID numbers of Archimedean solids:
## 1 - truncated tetrahedron
## 2 - cuboctahedron
## 3 - truncated cube
## 4 - truncated octahedron
## 5 - rhombicuboctahedron
## 6 - truncated cuboctahedron
## 7 - snub cube
## 8 - icosidodecahedron
## 9 - truncated dodecahedron
## 10 - truncated icosahedron
## 11 - rhombicosidodecahedron
## 12 - truncated icosidodecahedron
## 13 - snub dodecahedron

class ArchimedeanSolid(Solid):

	def __init__(self, name, id, sidelength):

		super().__init__(name)

		if id == 1:

			t = PlatonicSolid(self.name, 1, sidelength)
			tt = t.conway_truncate(1/3)

			self.overwrite(tt)
			self.origin_dilate(3)

		elif id == 2:

			c = PlatonicSolid(self.name, 2, sidelength)
			co = c.conway_truncate(1/2)

			self.overwrite(co)
			self.origin_dilate(2**(1/2))

		elif id == 3:

			c = PlatonicSolid(self.name, 3, sidelength)
			tc = c.conway_truncate(1/3)

			self.overwrite(tc)
			self.origin_dilate(3)

		elif id == 4:

			o = PlatonicSolid(self.name, 2, sidelength)
			to = o.conway_truncate(1/3)

			self.overwrite(to)
			self.origin_dilate(3)

		elif id == 5:

			c = PlatonicSolid(self.name, 3, sidelength)

			dist = sidelength / 2**(1/2)
			ce = c.conway_expand(dist)

			self.overwrite(ce)

		elif id == 6:

			c1 = 1 + 2**(1/2)
			c2 = 1 + 2*2**(1/2)

			vertices = point_permutations(point_sign_combinations([(1,c1,c2)]))

			tco = ConvexSolid.hull(name, vertices)
			tco.origin_dilate(sidelength/2)

			self.overwrite(tco)

		elif id == 7:

			## the Tribonacci Constant
			tr = (1 + (19 - 3*33**(1/2))**(1/3) + (19 + 3*33**(1/2))**(1/3)) / 3
			offset = (-1 + ((tr-1)/(2-tr))**(1/2)) / 2
			twist = np.arctan((tr-1)/(tr+1))

			c = PlatonicSolid(self.name, 3, sidelength)
			sc = c.conway_snub(sidelength * offset, twist)

			self.overwrite(sc)

		elif id == 8:

			i = PlatonicSolid(self.name, 5, sidelength)
			id = i.conway_truncate(1/2)

			self.overwrite(id)
			self.origin_dilate(2)

		elif id == 9:

			dd = PlatonicSolid(self.name, 4, sidelength)
			tdd = dd.conway_truncate(1/3)

			self.overwrite(tdd)
			self.origin_dilate(3)

		elif id == 10:

			i = PlatonicSolid(self.name, 5, sidelength)
			ti = i.conway_truncate(1/3)

			self.overwrite(ti)
			self.origin_dilate(3)

		elif id == 11:

			phi = (1 + 5**(1/2))/2

			vertices = [(1,1,phi**3), (phi**2,phi,2*phi), (2+phi,0,phi**2)]
			vertices = point_sign_combinations(vertices)
			vertices = point_cycles(vertices)

			ricodd = ConvexSolid.hull(name, vertices)
			ricodd.origin_dilate(sidelength/2)

			self.overwrite(ricodd)

		elif id == 12:

			phi = (1 + 5**(1/2))/2

			vertices = [(1/phi,1/phi,3+phi), (2/phi,phi,1+2*phi), (1/phi,phi**2,-1+3*phi), (2*phi-1,2,2+phi), (phi,3,2*phi)]
			vertices = point_sign_combinations(vertices)
			vertices = point_cycles(vertices)

			ticodd = ConvexSolid.hull(name, vertices)
			ticodd.origin_dilate(sidelength/2)

			self.overwrite(ticodd)

		elif id == 13:

			offset = 0.867399
			twist = 0.22874

			dd = PlatonicSolid(name, 4, 1)
			sdd = dd.conway_snub(offset, twist)

			self.overwrite(sdd)
