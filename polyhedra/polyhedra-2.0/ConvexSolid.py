class ConvexSolid(Solid):

    def __init__(self, name):

        super().__init__(name)

    def contains(self, p):

        pv = np.asarray(p)
        cv = self.center()
        axis_vec = cv - pv
        pointer_vecs = [v - pv for v in self.vertices]
        projections = [np.dot(axis_vec, v) for v in pointer_vecs]

        return all([pj > self.error for pj in projections])
