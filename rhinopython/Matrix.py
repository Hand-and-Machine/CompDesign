def is_number(x):
	try:
		tmp = int(x)
		return True
	except:
		return False

class Matrix:

	def __init__(self, entries):

		self.entries = [row.copy() for row in entries]
		self.rows = len(entries)
		self.cols = len(entries[0])

	def at(self, i, j):

		return self.entries[i][j]

	def set(self, i, j, val):

		self.entries[i][j] = val
		return self

	def row_at(self, i):

		return self.entries[i].copy()

	def col_at(self, j):

		return [[row[j]] for row in self.entries]

	def set_row(self, i, row):

		self.entries[i] = row.copy()
		return self

	def set_col(self, j, col):

		for i in range(0, len(col)):
			self.entries[i][j] = col[i]
		return self

	def add_row(self, row):
	
		self.entries.append(row)
		self.rows += 1
		return self

	def add_col(self, col):

		for i in range(0, self.rows):
			self.entries[i].append(col[i])
		self.cols += 1
		return self

	def clone(self):

		return Matrix(self.entries)

	def print(self):

		for row in self.entries: print(row)

	def __add__(a, b):

		if type(a) != Matrix or type(b) != Matrix:
			raise Exception("Matrices can only be added to other matrices")
		elif a.rows != b.rows or a.cols != b.cols:
			raise Exception("Matrices with different dimensions cannot be added")
		else:
			r = a.rows
			c = a.cols
			ae = a.entries
			be = b.entries
			entries = [[ae[i][j] + be[i][j] for j in range(c)] for i in range(r)]
			return Matrix(entries)

	def __mul__(a, b):

		if type(a) != Matrix or type(b) != Matrix:
	
			if is_number(a):
				entries = [[entry * a for entry in row] for row in b.entries]
				return Matrix(entries)
	
			elif is_number(b):
				entries = [[entry * b  for entry in row] for row in a.entries]
				return Matrix(entries)
	
			else:
				raise Exception("Only matrix-matrix and matrix-scalar multiplication are supported")

		elif a.cols != b.rows:
			raise Exception("Incompatible matrix dimensions for multiplication")

		else:
			entries = [[0] * b.cols for ph in range(a.rows)]
			length = a.cols
			for i in range(a.rows):
				for j in range(b.cols):
					a_row = a.row_at(i)
					b_col = b.col_at(j)
					entry = sum([a_row[n] * b_col[n][0] for n in range(length)])
					entries[i][j] = entry
			return Matrix(entries)

	def __rmul__(a, b):
		
		return Matrix.__mul__(b, a)

	def column(entries):

		return Matrix([[e] for e in entries])

	def zeroes(i, j):

		return Matrix([[0] * j for i in range(dim)])

	def identity(dim):

		m = Matrix([[0] * dim for i in range(dim)])
		for i in range(dim):
			m.set(i, i, 1)
		return(m)	

	def translation(vec):

		dim = len(vec)
		t = Matrix.identity(dim)
		t.add_col(vec)
		t.add_row([0] * (dim+1))
		return(t)

	def dilation(factor, center):

		dim = len(center)
		d = Matrix.identity(dim+1).set(dim, dim, 0) * factor
		t = Matrix.translation([-x for x in center])
		t_inv = Matrix.translation(center)
		return t_inv * d * t

	def rotation(theta, normal):

		dim = len(normal)

class Vector(Matrix):

	def __init__(self, coords):

		entries = [[e] for e in coords]
		super().__init__(entries)

	def print(self):

		for e in self.entries: print(e[0])

	def to_list(self):

		return [e[0] for e in self.entries]

	def norm(self):

		return sum([e[0]**2 for e in self.entries])**(1/2)

	def normalize(self):

		norm = self.norm()
		for i in range(self.rows):
			val = self.at(i, 0)
			self.set(i, 0, val/norm)
		return self

class Point(Matrix):

	def __init__(self, coords):
		entries = [[e] for e in coords] + [[1]]
		super().__init__(entries)

	def print(self):
		for e in self.entries[:-1]:
			print(e[0], end=" ")
		print("")
