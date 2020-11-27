## Here's a key for the different ID numbers of uniform solids:
## 1 - regular tetrahedron
## 2 - regular octahedron
## 3 - cube
## 4 - regular dodecahedron
## 5 - regular icosahedron

class UniformSolid(Solid):

	def __init__(self, name, id, sidelength):
		
		super().__init__(name)

		## centered at the center of its base
		if id == 1:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 3, adjust_sidelength=sidelength)
			peak = equidistant_pt(base_pts[0], base_pts[1], base_pts[2], sidelength) ## (0, 0, np.sqrt(2/3))
			th = Pyramid("temp", base_pts, peak)

			self.join_solid(th)

		## centered at its center
		if id == 2:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 4, adjust_sidelength=sidelength)
			peak = equidistant_pt(base_pts[0], base_pts[1], base_pts[2], sidelength)
			top_pm = Pyramid("temp", base_pts, peak, based=False)
			base_pts.reverse()
			bottom_pm = Pyramid("temp", base_pts, -peak, based=False)

			self.join_solid(top_pm)
			self.join_solid(bottom_pm)

		if id == 3:

			base_pts = reg_polygon_pts((0, 0, 0), (1, 0, 0), (0, 0, -1), 4, adjust_sidelength=sidelength)
			cb = Prism("temp", base_pts, sidelength)

			self.join_solid(cb)
