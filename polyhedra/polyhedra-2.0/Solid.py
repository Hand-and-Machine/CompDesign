class Triangle:

    def __init__(self, p1, p2, p3):

        self.p1 = np.asarray(p1)
        self.p2 = np.asarray(p2)
        self.p3 = np.asarray(p3)
        cross = np.cross(self.p3 - self.p2, self.p1 - self.p2)
        self.normal = cross / np.linalg.norm(cross)

    def to_stl(self):

        stl_str = ""
        stl_str += "facet normal " + stringify_vec(self.normal) + "\n"
        stl_str += "outer loop\n"
        stl_str += "vertex " + stringify_vec(self.p1) + "\n"
        stl_str += "vertex " + stringify_vec(self.p2) + "\n"
        stl_str += "vertex " + stringify_vec(self.p3) + "\n"
        stl_str += "endloop\n"
        stl_str += "endfacet\n"

        return stl_str

class Face:

    def __init__(self, vertex_ids, supersolid):

        self.vertex_ids = vertex_ids[:]
        self.num_sides = len(self.vertex_ids)
        self.vertex_lookup = { self.vertex_ids[index]: index for index in range(self.num_sides) }
        self.edges = [(self.get_id(i), self.get_id(i+1)) for i in range(self.num_sides)]

        self.solid = supersolid

    ## Set the Solid that this face belongs to
    def set_supersolid(self, supersolid):

        self.solid = supersolid
        supersolid.faces.append(self)
        return self

    ## Get the ID of a vertex at a given index
    def get_id(self, index):

        return self.vertex_ids[index % self.num_sides]

    ## Get the coordinates of a vertex at a given index
    def get_coords(self, index):

        id = self.get_id(index)
        return self.solid.get_vertex(id)

    ## Get the coordinates of all vertices
    def all_coords(self):

        return [self.get_coords(index) for index in range(self.num_sides)]

    ## Calculate the center (centroid) of the face
    def center(self):

        return sum(self.all_coords()) / self.num_sides

    ## Calculate the normal vector, assuming the face is nondegenerate
    def normal(self):

        pv0 = self.get_coords(0)
        pv1 = self.get_coords(1)
        pv2 = self.get_coords(2)
        v0 = pv0 - pv1
        v1 = pv1 - pv2
        normal = np.cross(v0, v1)
        normal = normal / np.linalg.norm(normal)

        return normal

    ## Determine whether the face (facet) is visible from the given point
    def is_visible(self, standpoint, strict=True):

        pv = np.asarray(standpoint)
        cv = self.center()
        nv = self.normal()

        if strict:
            return (np.dot(nv, pv - cv) > self.solid.error)
        else:
            return (np.dot(nv, pv - cv) > -self.solid.error)

    ## Clone this Face and return the clone
    def copy(self):
        return Face(self.vertex_ids, None)

    ## Cut the fact up into Triangles for STL generation
    def build(self):

        triangles = []

        num_pts = self.num_sides
        center = self.center()

        for i in range(num_pts):
            t = Triangle(center, self.get_coords(i), self.get_coords(i+1))
            triangles.append(t)

        return triangles

class Solid:

    def __init__(self, name, error=1.0e-7):

        self.name = name
        self.error = error
        self.triangles = []
        self.vertices = []
        self.num_vertices = 0
        self.edges = []
        self.faces = []
        self.faces_by_vertex = []
        self.faces_by_edge = []

    ## Return the coords of the vertex with a given ID
    def get_vertex(self, id):

        return self.vertices[id]

    ## Add a vertex if it has not already been added, returning the ID
    def add_vertex(self, v, check_equality=True):

        if check_equality:
            for i in range(self.num_vertices):
                if distance(v, self.get_vertex(i)) < self.error:
                    return i

        self.vertices.append(np.asarray(v).copy())
        self.num_vertices += 1
        self.edges.append(set())
        self.faces_by_vertex.append([])
        self.faces_by_edge.append({})

        return self.num_vertices - 1

    ## Add an edge between two vertices with given IDs
    def add_edge(self, id1, id2):

        if max(id1, id2) >= self.num_vertices:
            return

        self.edges[id1].add(id2)
        self.edges[id2].add(id1)

    ## Add a face with given points, automatically adding vertices and edges
    def add_face(self, pts, ids=[]):

        num_pts = len(pts)
        vertex_ids = ids.copy()

        if ids == []:

            ## Add IDs to array while avoiding duplicate entries
            next_id = self.add_vertex(pts[0])
            for i in range(num_pts):
                id = next_id
                next_id = self.add_vertex(pts[(i + 1) % num_pts])
                if id != next_id:
                    vertex_ids.append(id)

        face = Face(vertex_ids, self)
        self.faces.append(face)

        for i in range(num_pts):
            id = face.get_id(i)
            next_id = face.get_id(i+1)
            self.add_edge(id, next_id)
            self.faces_by_vertex[id].append(face)
            self.faces_by_edge[id][next_id] = face

    ## Find the faces with a given edge, starting with the face containing that edge in the correct orientation
    def faces_with_edge(self, id1, id2):

        faces_list = [self.faces_by_edge[id1][id2], self.faces_by_edge[id2][id1]]
        return faces_list  
 
    ## Clone this Solid and return its clone
    def copy(self, name):
        
        s = Solid(name, error=self.error)
        s.vertices = [np.copy(v) for v in self.vertices]
        s.num_vertices = self.num_vertices
        s.edges = [vs.copy() for vs in self.edges]

        face_clones = {f: f.copy().set_supersolid(s) for f in self.faces}
        s.faces = [face_clones[f] for f in face_clones]
        s.faces_by_vertex = [[face_clones[f] for f in fs] for fs in self.faces_by_vertex]
        s.faces_by_edge = [{id: face_clones[fs[id]] for id in fs} for fs in self.faces_by_edge]

        return s

    ## Overwrite this Solid with a clone of another Solid
    def overwrite(self, solid):

        self.error = solid.error
        self.vertices = [np.copy(v) for v in solid.vertices]
        self.num_vertices = solid.num_vertices
        self.edges = [vs.copy() for vs in solid.edges]

        face_clones = {f: f.copy().set_supersolid(self) for f in solid.faces}
        self.faces = [face_clones[f] for f in face_clones]
        self.faces_by_vertex = [[face_clones[f] for f in fs] for fs in solid.faces_by_vertex]
        self.faces_by_edge = [{id: face_clones[fs[id]] for id in fs} for fs in solid.faces_by_edge]

        return self

    ## Dilate this Solid about the origin by a given factor
    def origin_dilate(self, factor):

        for v in self.vertices: v = v * factor
        return self

    def center(self):

        return sum(self.vertices) / self.num_vertices
 
    ## Generate the Triangles for each face, to be used for STL generation
    def build(self):

        self.triangles = []
        for f in self.faces:
            self.triangles += f.build()

        return self

    ## Generate an STL file (WARNING: overwrites preexisting files)
    def gen_file(self):

        filename = self.name + ".stl"
        if os.path.exists(filename): os.remove(filename)
        file = open(filename, "a")

        filetext = ""
        filetext += "solid " + self.name + "\n"
        for t in self.triangles:
            filetext += t.to_stl()
        filetext += "endsolid " + self.name + "\n"

        file.write(filetext)
        file.close()

        return self

    ## Save this solid's data as a text file with extension .solid
    def save(self, filename):

        file = open(filename + ".solid", 'w')

        file.write("VERTICES:\n")
        for v in self.vertices:
            x = str(v[0])
            y = str(v[1])
            z = str(v[2])
            file.write(x + " " + y + " " + z + "\n")

        file.write("FACES:\n")
        for f in self.faces:
            file.write(stringify_vec(f.vertex_ids) + "\n")

    ## Load preexisting data from a .solid file into a new Solid and return it
    def load(filename, name):

        s = Solid(name)

        with open(filename + ".solid", 'r') as file:

            section = 0
            for line in file:
                if line in ["VERTICES:\n", "FACES:\n"]:
                    section += 1
                elif section == 1:
                    verts = [float(x) for x in line.split()]
                    s.add_vertex(verts, check_equality=False)
                elif section == 2:
                    ids = [int(id) for id in line.split()]
                    s.add_face([], ids=ids)

        return s

    ## Given a bunch of faces, find the exposed boundary, assuming it is contiguous
    def boundary(faces):

        if len(faces) == 0: return []

        visible_edges = {e for f in faces for e in f.edges}
        boundary_edges = []
        for e in visible_edges:
            if (e[1], e[0]) not in visible_edges:
                boundary_edges.append(e)

        boundary_dict = {e[0]: e for e in boundary_edges}
        last_edge = boundary_edges[0]
        boundary_verts = []
        for i in range(len(boundary_edges)):
            boundary_verts.append(last_edge[0])
            last_edge = boundary_dict[last_edge[1]]

        return boundary_verts
