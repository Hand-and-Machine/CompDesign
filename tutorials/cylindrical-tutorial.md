### Part 1

Let's start by checking out Rhino's `Polar array` transformation. First, create a solid sphere, centered at, say `(10, 0, 0)` and with a radius of `3`.

![Fig1](/tutorials/img/cylindrical-tutorial-fig1.png)

Now select the `Polar array` transformation from the `Transform` menu. This transformation creates many copies of a specified object, rotated by different amounts around a point. You should be prompted to select (1) an object to array, (2) a center for your polar array, or the point about which your object will be rotated, (3) the number of items, or copies of your object, and (4) the angle to fill, as well as an optional `Z Offset` parameter. For (1), select your sphere; for (2) choose the origin `(0,0,0)`; for (3) pick any number you want, say between 5 and 10; and for (4) choose the default value of `360` degrees (and leave the `Z Offset` parameter at its default value of `0`). You should get something that looks like this:

![Fig2](/tutorials/img/cylindrical-tutorial-fig2.png)

However, you may have more than 5 copies of the sphere depending on what value you chose for (3).

Let's apply the `Polar array` transformation again. This time, select all 5 spheres as the object to be arrayed, set the angle to fill equal to `45` degrees, and set the value of `Z Offset` to be `5`. Now, instead of just rotating each copy of your object, the transformation will translate each copy 5 units in the z-direction. You should get something like this, depending on how many copies you chose to make:

![Fig3](/tutorials/img/cylindrical-tutorial-fig3.png)

(Note: the above image was created using `Display` -> `Rendered viewport`, since it doesn't look good when displayed using `Wireframe`.) We get a bunch of stacked spheres, where each level is `5` units higher than the previous, and each pile sweeps through an angle of `45` degrees. If you want, play around with the `Polar array` transformation some more, trying out different values for each of the parameters.

## Part 2

One limitation of the `Polar array` transformation is that it can only rotate and elevate each copy of an object by a constant amount. What if we want to make a twisting stacked structure where the gap between levels increases from one level to the next? The `Polar array` functionality isn't flexible enough to do this, but we can accomplish something similar by writing our own functions in Grasshopper.

Open Grasshopper (`Tools` -> `Grasshopper`) and connect a GhPython script component, a Panel component, and a Point component as shown below:

![Fig4](/tutorials/img/cylindrical-tutorial-fig4.png)

The panel will be used to debug our Python script by printing messages to the console, and we'll use the script to generate a set of points in Rhino by sending them to the point component. Open up the python script editor and start by pasting the following simple script:

```
import rhinoscriptsyntax as rs
import math

print("hello world!")
```

Since we're interested in creating copies of objects that are rotated about the z-axis, we can use cylindrical coordinates to make this job easier. Recall that cylindrical coordinates identifies points by their distance `r` from the z-axis, the angle `theta` that they make with the xz-plane, and their height `z`. A point in 3-space is uniquely identified by the triple `(r, theta, z)` in cylindrical coordinates, whereas the triple `(x, y, z)` is used in the more common rectangular coordinates.

![Fig5](/tutorials/img/cylindrical-tutorial-fig5.png)
[CREATE A PICTURE SHOWING HOW THE COORDINATE SYSTEMS WORK]

Let's write a class in Python that will help us store and transform points in the cylindrical coordinate system.

```
class CylindricalPoint:
    
    def __init__(self, x, y, z):
        self.r = math.sqrt(x**2 + y**2)
        self.theta = math.atan2(x, y)
        self.z = z
        
    def to_rectangular(self):
        x = self.r * math.cos(self.theta)
        y = self.r * math.sin(self.theta)
        z = self.z
        return (x, y, z)

    def to_rhinopoint(self):
        rect_coords = self.to_rectangular()
        rhino_pt = rs.CreatePoint(rect_coords[0], rect_coords[1], rect_coords[2])
        return rhino_pt

    def clone(self):
        pp = CylindricalPoint(0, 0, 0)
        pp.r, pp.theta, pp.z = self.r, self.theta, self.z
        return pp
```

The `__init__` method generates values of `r`, `theta`, and `z` for a point in 3-space, given its rectangular coordinates `x, y, z`. The `to_rectangular` method will allow us to convert the point back to rectangular coordinates after we've finished applying different transformations to the point. The method `to_rhinopoint` simply takes the point's rectangular coordinates and uses them to generate a Rhino point object. Finally, the `clone` method makes a copy of a `CylindricalPoint` instance, which will be useful if we want to make transformed copies of a single point.

Now suppose we have some instance `p` of a `CylindricalPoint` object. We can easily transform `p` in a number of useful ways by directly altering its `r`, `theta`, and `z` attributes. For example, executing `p.r = p.r * 3` would increase the radius by a factor of 3, effectively dilating it about the z-axis.Executing `p.theta += math.pi/4` would rotate the point counterclockwise about the z-axis by an angle of PI/4, or 45 degrees. Executing `p.z += 1` would lift the point 1 unit higher.

### Part 3

Let's use this new class to recreate the arrangement of spheres we made earlier (this time just using points instead of spheres). First let's generate the 5 base points, using the following code:

```
p1 = CylindricalPoint(10, 0, 0)
base = []

for i in range(0, 5):
    base.append(p1.clone())
    p1.theta += 2*math.pi/5
    
a = [p.to_rhinopoint() for p in base]
```

The `for` loop in the second point repeatedly appends a copy of `p1` to the array and then rotates it by an angle of `2*math.pi/5`. Note that the angle `2*math.pi/5` must be used to get 5 evenly spaced rotations of the point: a full rotation about the z-axis sweeps through an angle of 360 degrees or 2*PI, and since we want 5 evenly spaced points, we must divide this angle by 5. Running this code should give you something like this:

![Fig6](/tutorials/img/cylindrical-tutorial-fig6.png)

Let's make this code more modular by making it possible to create more than 5 evenly spaced points. Create a new Number Slider component, rename it as `num_pts`, and connect it to the Python component like this:

![Fig7](/tutorials/img/cylindrical-tutorial-fig7.png)

Edit the slider so that its values are integers between `5` and `20` (or some other suitable values), then modify your `for` loop as follows:

```
for i in range(0, num_pts):
    base.append(p1.clone())
    p1.theta += 2*math.pi/num_pts
```

Now you should be able to change the number of points by adjusting the slider. For instance, setting the slider to a value of `9` gives the following arrangement:

![Fig8](/tutorials/img/cylindrical-tutorial-fig8.png)

### Part 4

Now let's make multiple layers that are rotated and stacked on top of each other, as we did earlier with the spheres. We'll store each layer of points in its own array for easy access later on. Add the following lines to your code immediately after the other `for` loop:

```
layers = []

for i in range(0, 5):
    next_layer = [p.clone() for p in base]
    layers.append(next_layer)
    for p in base:
        p.theta += math.pi/16
        p.z += 5
```

This `for` loop repeatedly adds copies of the points in `base` to the list `layers`, and then rotates each point by an angle of `math.pi/20` and translates them `5` units up the z-axis. Note that this is exactly the same as what we did with the spheres: recall that each stack of spheres swept out an angle of 45 degrees or PI/4, meaning that each sphere must have been rotated exactly PI/16 degrees (because 4 rotated duplicates were created for each sphere, and 4 * PI/16 = PI/4). Before running, don't forget about the last line of your code:

```
a = [p.to_rhinopoint() for p in base]
``` 

This only considers the points in the array `base`, but we care about all of the points stored in `layers`. Recall that `layers` is a list of lists, with each list corresponding to one of the stacked layers. We can generate a list of Rhino points from `layers` by replacing the above line with the following:

```
a = [p.to_rhinopoint() for layer in layers for p in layer]
```



### Troubleshooting

#### Part 3

`Runtime error (TypeErrorException): range() integer end argument expected, got float`
If you get the above error after incorporating the `num_pts` input into your `for` loop, right-click on the `num_pts` input of the Python component and select `Type hint` -> `int`. This will let the Python component know to interpret that input as an integer, so that it is compatible with the `range()` function.


