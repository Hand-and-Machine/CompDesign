class ConvexSolid(Solid):

    def __init__(self, name):

        super().__init__(name)

    def contains(self, p):

        pv = np.asarray(p)
        cv = np.asarray(self.center())
        axis_vec = cv - pv
        pointer_vecs = [np.asarray(vert) - pv for vert in self.vertices]
        projections = [np.dot(axis_vec, v) for v in pointer_vecs]

        return all([pj > self.error for pj in projections])

    def is_visible(self, face, standpoint):

        pv = np.asarray(standpoint)
        cv = np.asarray(face.center(self.vertices))
        nv = np.asarray(face.normal(self.vertices))

        return ( np.dot(nv, pv - cv) > self.error )

    def horizon(self, visible_faces):

        if len(visible_faces) == 0: return []

        visible_edges = {e for f in visible_faces for e in f.edges}
        horizon_edges = []
        for e in visible_edges:
            if (e[1], e[0]) not in visible_edges:
                horizon_edges.append(e)

        horizon_dict = {e[0]: e for e in horizon_edges}
        last_edge = horizon_edges[0]
        horizon_verts = []
        for i in range(len(horizon_edges)):
            horizon_verts.append(last_edge[0])
            last_edge = horizon_dict[last_edge[1]]

        return horizon_verts

    def add_hull_vertex(self, vertex):

        cs = ConvexSolid(self.name)

        pv = np.asarray(vertex)
        visible_faces = [f for f in self.faces if self.is_visible(f, vertex)]
        horizon = self.horizon(visible_faces)
        horiz_length = len(horizon)        

        for i in range(horiz_length):
            id1 = horizon[i]
            id2 = horizon[(i + 1) % horiz_length]
            v1 = self.vertices[id1]
            v2 = self.vertices[id2]
            adj_face = self.faces_with_edge(id1, id2)[1]
            cv = adj_face.center(self.vertices)
            nv = adj_face.normal(self.vertices)
            pj = abs(np.dot(nv, pv - cv))
            if abs(np.dot(nv, pv - cv)) > self.error:
                cs.add_face([v1, v2, vertex])
            else:
                visible_faces.append(adj_face)
                new_vertices = adj_face.insert_vertex_after(pv, id2, self.vertices)
                cs.add_face(new_vertices)

        for f in self.faces:
            if f not in visible_faces: cs.add_face(f.vertex_coords(self.vertices))
       
        ## I still need to deal with the case in which the vertex is coplanar with some preexisting face of the solid
 
        self.overwrite(cs)
        return self

    def tetrahedron(name, p1, p2, p3, p4):

        cs = ConvexSolid(name)

        pv1 = np.asarray(p1)
        pv2 = np.asarray(p2)
        pv3 = np.asarray(p3)
        pv4 = np.asarray(p4)
        cv = (pv1 + pv2 + pv3 + pv4)/4

        for f in itertools.combinations([p1,p2,p3,p4], 3):
            cs.add_face_unordered(f, cv)

        return cs

    def hull(name, pts, error=1e-7):

        pv1 = np.asarray(pts[0])
        pv2 = np.asarray(pts[1])
        pv3 = np.asarray(pts[2])
        cv = (pv1 + pv2 + pv3) / 3
        nv = np.cross(pv2-pv1, pv3-pv2)
        nv = nv / np.linalg.norm(nv)
        proj = 0
        id4 = 3
        pv4 = np.asarray(pts[id4])
        while abs(np.dot(nv, pv4 - cv)) < error:
            id4 += 1
            pv4 = np.asarray(pts[id4])
        remaining_pts = [pts[i] for i in range(len(pts)) if i not in [0,1,2,id4]]

        cs = ConvexSolid.tetrahedron(name, pv1, pv2, pv3, pv4)
        for p in remaining_pts:
            cs.add_hull_vertex(p)

        return cs
