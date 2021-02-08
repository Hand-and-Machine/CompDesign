This folder contains Python scripts I've written to generate 3D geometrical forms as STL files by directly writing the contents of the STL files. I'm sure something similar has been done before by someone else, so I may be reinventing the wheel... but hey, I'm learning a lot by doing this!

Here's a list of the code files with descriptions of their functions:
- `stl-Tools.py` contains a bunch of functions that are useful for geometrical constructions in 3D.
- `stl-Solid.py` defines the basic classes like `Triangle`, `Face` and `Solid` that are used to build solids.
- `stl-Common.py` defines "shortcut" classes for some common solids.
- `stl-Uniform.py` defines classes for constructing the uniform polyhedra.
- `stl-Load.py` can be used to load the above files all at once and in the correct order.

Here's a table of contents if you want to read about any of the above in greater detail:

- [3D Construction Tools](#3d-construction-tools)
- [The Solid Class](#the-solid-class)
  + [Supplementary Triangle and Face Classes](#supplementary-triangle-and-face-classes)
  + [Adding Vertices, Edges, and Faces](#adding-vertices-edges-and-faces)
  + [Solid Manipulation](#solid-manipulation)
  + [STL File Generation](#stl-file-generation)
- [Special Solids](#special-solids)
  + [Common Solids](#common-solids)
  + [Uniform Solids](#uniform-solids)

## 3D Construction Tools

Here's a list of tools for 3D construction defined in `stl-Tools.py`:

- `circumcenter(p1, p2, p3)` finds the circumcenter of three points `p1`, `p2`, and `p3`, or the point in the same plane which is the same distance from all three.
- `complete_reg_polygon(p1, p2, p3, num_pts)` will, given three vertices `p1`, `p2`, and `p3`, of a regular polygon, as well as the number of vertices `num_pts` of that polygon, return a list of all of the points of that polygon, including the three given.
- `equidistant_pt(p1, p2, p3, d)` constructs a point whose distance from each of the points `p1`, `p2`, `p3` is equal to `d`. This is not always possible, depending on the value of `d`, and if it is impossible, the function returns `False`. When a solution exists, there may exist two solutions, which are reflections of each other across the plane in which the three points lie. This function picks out the point on the side of the plane on which the points `p1`, `p2`, and `p3` appear in counterclockwise order.
- `fold_up(p1, p2, p3, theta, phi, length)` is tricky to describe without a picture! Imagine that the three points `p1`, `p2`, `p3` define the corner of a polygon, or two line segments (`p1p2` and `p2p3`) joined at a vertex (`p2`). This function returns a point which, when joined to `p2`, forms a line segment of length `length` which makes an angle of `theta` with the line segment `p1p2` and an angle of `phi` with the line segment `p2p3`. There may exist two such points, which are reflections of each other across the plane in which the three points lie. This function yields the point on the side of the plane from which `p1`, `p2`, and `p3` appear in clockwise order.
  - Why on Earth would we want to do this, you might ask? It's helpful for calculating how three polygonal faces of a solid's net which meet at a vertex "fold up" into three dimensions so that their edges are glued seamlessly together. I'll probably upload an illustration later on showing how this is done.
- `reg_polygon_pts(center, p1, normal, num_pts, adjust_sidelength=0)` generates the points of a regular polygon starting with the point `p1`. The polygon is centered at the point `center` and its vertices are generates counterclockwise about the given normal vector `normal`, and the number of points is specificed by `num_pts`. The optional parameter `adjust_sidelength`, if specified, will scale the polygon about its center so that its side length equals the given value.
- `rotate_points_about_line(points, base_pt, vec, theta)` is pretty self-explanatory. Given a list of points `points`, a point `base_pt` and a vector `vec` defining an oriented line, and an angle `theta`, this function rotates each of the points by the given angle about the oriented line, with the direction of rotation determined by the direction of `vec` and the right-hand rule. The images are returned as an array in the same order as the array of points given as input.

## The Solid Class

### Supplementary Triangle and Face Classes

Two supplementary classes are used to define the `Solid` class: the `Triangle` and `Face` classes.

The `Triangle` class is used only to construct STL files. A `Triangle` is defined by three points, which are passed as arguments to its constructor. The order in which these points are listed is important! In an STL file, triangles are stored as *facets*, which are like flat triangles that are only visible from one side and invisible from the other side. A `Triangle` will be visible on the side from which its points appear in counterclockwise order. Aside from its constructor, the `Triangle` class only has one method: `to_stl()`, which converts it to ASCII text in the STL file format.

The `Face` class is also very simple, and is just used to help organize the `Solid` class. Its most important method is `Solid.vertices`, which stores its vertices. However, it does not store the actual coordinates of each vertex, but rather the *ids* of each vertex, which are integers. In a `Solid` object, vertices are stored in the list `Solid.vertices`, and each vertex is assigned an id equal to its index in this list, so the entries of `Face.vertices` refer to these ids rather than the points themselves. Also, the order in which these points are listed is important: when the `Solid` is converted to STL, each `Face` will only appear from the side on which its vertices appear in counterclockwise order.

### Adding Vertices, Edges, and Faces

Information about the vertices, edges, and faces of each `Solid` are stored redundantly for ease of manipulation:

- `Solid.vertices` is a list of the vertices of the `Solid`, defined by floating point coordinates.
- `Solid.edges` stores information about which pairs of vertices are connected to each other by edges. It is a list of sets, where `Solid.edges[i]` is the set of ids of vertices connected to the vertex with id `i`, or `Solid.vertices[i]`. In other words, `Solid.vertices[i]` and `Solid.vertices[j]` are joined by an edge if and only if `j in Solid.edges[i]`.
- `Solid.faces` is a list of `Face` objects representing the faces of the `Solid`.

Vertices, edges, and faces can be added using the methods `Solid.add_vertex(v)`, `Solid.add_edge(v_id, w_id)`, and `Solid.add_face(pts)` where `v` is a point defined by coordinates, `v_id` and `w_id` are the ids of two points already in the `Solid`, and `pts` is a list of points defined by coordinates. The method `Solid.add_vertex(v)` automatically protects against accidentally storing the same vertex multiple times by checking whether `Solid.vertices` already contains `v` before appending it to the list again. `Solid.add_vertex(v)` also returns the id of `v`, or its index in `Solid.vertiex`, whether a duplicate was found or not. `Solid.add_edge` naturally protects against accidental duplication because it consists of sets rather than lists. Also, `Solid.add_face` automatically adds the necessary edges and vertices in addition to constructing a new face for the `Solid`, so there is no need to manually add a polygon's points and edges in addition to calling `Solid.add_face(pts)`.

One potential problem with using floating-point numbers to specify points in coordinate space in Python is that two numerical calculations which, in theory, should yield the same exact point, sometimes give slightly different results due to minute calculation errors. For example, two mathematically identical calculations might produce the results `(0.0, 0.0, 1.0)` and `(0.0, 0.0, 1.0000000003)`. This would cause the duplication fail-safe built into `Solid.add_vertex(v)` to fail, because these two points would register as unequal even though they should be the same. However, this is remedied by checking not only whether `v` is *identical* to any preexisting vertex in `Solid.vertices`, but whether it is *very close* to any of them. If `v` is sufficiently close to another vertex in `Solid.vertices`, it registers as a duplicate. The default threshhold for recognizing a vertex as a duplicate is a distance of `1E-7`, but this threshhold is stored in `Solid.error` and can be overridden.

This failsafe against accidental vertex duplication is helpful, but it has drawbacks - for example, it makes the program buggy when dealing with very small or finely-detailed solids.

### Solid Manipulation

The `Solid` class also has a few built-in higher-level functions for manipulating its geometry. (They're designed to work only for convex solids, and might not work properly for concave/stellated solids.) These include:

- `Solid.translate(trans)` rigidly translates the `Solid` (vertexwise) in the direction of the given vector `trans`.
- `Solid.join_solid(solid)` unions the `Solid` with another given solid `solid`, even if they intersect/overlap with each other.
- `Solid.overwrite(solid)` completely overwrites the `Solid` with a copy of the given solid `solid`.
- `Solid.plane_slice(plane_point, plane_normal)` returns the solid formed by slicing the `Solid` with a plane defined by the point `plane_point` and the normal vector `plane_normal`. The portion of the `Solid` on the side of the plane pointed to by `plane_normal` is removed, and the other side remains. NOTE: this method does *not* overwrite the original `Solid`, but rather returns a new `Solid` created by performing this operation.
    + Currently only supported for convex solids... sometimes works with concave solids, but often causes problems
- `Solid.conway_kis(distance)` returns the solid formed by turning each face into a pyramid, which is accomplished  by locating the center of each face and pushing it outward (or inward, for negative values of `distance`) in the direction normal to the face. Corresponds to the Conway "kis" operator.
- `Solid.conway_truncate(proportion)` returns the solid formed by cutting off (truncating) all of the vertices of the `Solid` (the depth of the cut is determined by the argument `proportion`, where a value of, say, `0.5` cuts half of the depth of the maximum cut which would not collide with any other vertices). Corresponds to the Conway "truncate" operator.
- `Solid.conway_expand(distance) returns the solid formed by pushing each face a distance `distance` away from the center, and automatically filling in the empty spaces with polygons.
- `Solid.conway_dual()` attempts to form the dual solid of a given solid by placing a point at the center of each face and connecting the points corresponding to the faces surrounding each vertex into a single face. 
    + For many solids, this results in "faces" with vertices that do not all lie in the same plane. These sorts of solids can be built and converted to STL files unproblematically, but they may not respond predictably when further transformations are applied to them.

There are a lot more methods I'd like to write to manipulate `Solid` objects with. Here's a tentative to-do list:

- Rotating the polyhedron in 3-space
- Edge-truncation (as opposed to vertex truncation)
- Snub operation
- Construct the solid given by the convex hull of a point set

### STL File Generation

When you initialize a `Solid` object, you must pass a `name` to its constructor. When you generate an STL file for the `Solid`, `name` will be the name of the file. To generate the file, first call `Solid.build()`, which turns all of the `Face` objects into `Triangle` objects that are stored in `Solid.triangles`, and then call `Solid.gen_file()`, which turns these `Triangle` objects into an STL file and saves it. BEWARE: `Solid.gen_file()` will overwrite previously created STL files with the same name.

## Special Solids

### Common Solids

`stl-Common.py` contains classes allowing for easy construction of some of the more common types of solids:

- Right prisms, which are generated using the constructor `RightPrism(name, base_pts, height)`, where `name` is the desired name of the `Solid`, `base_pts` is a list of points defining the prism's base, and `height` is the height of the prism. It also has an optional argument `topped` with default value `True` which determines whether the prism is closed by a second base (default setting) or open like a cup (which occurs when `topped=False`).
  - Note to self: it might be a good idea to create a more general `Prism` class that is not restricted to right prisms.
- Pyramids, which are generated using the constructor `Pyramid(name, base_pts, peak)` where `name` is the desired name, `base_pts` is a list of points defining the pyramid's base, and `peak` is the point at which the pyramid has its peak. Also, there is an optional argument `based` with default value `True` which determines whether the pyramid's base is closed (default setting) or open like an ice-cream cone (which occurs when `based=False`).

### Uniform Solids

Right now, the only uniform solids implemented in `stl-Uniform.py` are the Platonic solids and some of the Archimedean solids. The Platonic solids are generated by the constructor `PlatonicSolid(name, id, sidelength)`, where `name` is the desired name, `id` is one of 5 integers corresponding to the Platonic solids, and `sidelength` is the desired side length of the solid (all sides have equal length on a uniform solid). The ids are as follows:

- `1` -> regular tetrahedron
- `2` -> regular octahedron
- `3` -> cube
- `4` -> regular dodecahedron
- `5` -> regular icosahedron

The Archimedean solids can be generated analogously using the constructor `ArchimedeanSolid(name, id, sidelength)`. Not all Archimedean solids are currently supported, but here are the ids for those that are:

- `1` -> truncated tetrahedron
- `2` -> cuboctahedron
- `3` -> truncated cube
- `4` -> truncated octahedron
- `6` -> truncated cuboctahedron
- `9` -> truncated dodecahedron
- `10` -> truncated icosahedron

I hope to add more soon - the rest of the Archimedean Solids, then the Uniform prisms and antiprisms, and perhaps even all of the Johnson Solids eventually!
