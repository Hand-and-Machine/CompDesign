This folder contains Python scripts I've written to generate 3D geometrical forms as STL files by directly writing the contents of the STL files. I'm sure something similar has been done before by someone else, so I may be reinventing the wheel... but hey, I'm learning a lot by doing this!

The script `stl-Solid.py` contains the basic functions and classes that are required for all other scripts. 

The `Triangle` class is very low-level and is defined by three points. The order of these points is important, since a single facet in an STL file only defines one side of a 2D shape. Initializing a `Triangle` as `Triangle(p1, p2, p3)` will create a facet that is visible from the side on which `p1, p2, p3` appear in counterclockwise order. A `Solid` object may contain many facets, which are added by calling the `Solid.add_face(pts)` method, where `pts` is a list of points. Again, a face added this way will only be visible from the direction in which the list of points `pts` appears in counterclockwise order. Once you have a solid, calling the method `Solid.gen_file()` will render the solid in an STL file with the same name as the solid was given when it was initialized.

The script `stl-Common.py` defines classes for some common solids. Here's a list:

- `Prism(name, base_pts, height)` defines a right prism with base vertices given in an array `base_pts` (listed in counterclockwise order, as viewed from outside the solid) and height `height`.
- `Pyramid(name, base_pts, peak)` defines a pyramid with base vertices given in an array `base_pts` (listed in counterclockwise order, as viewed from the outside) and peak vertex `peak`. Make sure to order the base vertices properly.
