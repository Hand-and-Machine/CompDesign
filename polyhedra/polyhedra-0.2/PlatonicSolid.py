class PlatonicSolid(ConvexSolid):

    solid_map = {
        1: "unit-regular-tetrahedron",
        2: "unit-regular-octahedron",
        3: "unit-cube",
        4: "unit-regular-dodecahedron",
        5: "unit-regular-icosahedron"
    }

    def __init__(self, name, id, sidelength):
        super().__init__(name)

        solidname = PlatonicSolid.solid_map[id]
        file = "platonic-solids/" + solidname
        self.overwrite(Solid.load(file, name))
        self.origin_dilate(sidelength)
