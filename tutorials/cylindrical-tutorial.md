Let's start by checking out Rhino's `Polar array` transformation. First, create a solid sphere, centered at, say `(10, 0, 0)` and with a radius of `3`.

![Fig1](/tutorials/img/cylindrical-tutorial-fig1.png)

Now select the `Polar array` transformation from the `Transform` menu. This transformation creates many copies of a specified object, rotated by different amounts around a point. You should be prompted to select (1) an object to array, (2) a center for your polar array, or the point about which your object will be rotated, (3) the number of items, or copies of your object, and (4) the angle to fill, as well as an optional `Z Offset` parameter. For (1), select your sphere; for (2) choose the origin `(0,0,0)`; for (3) pick any number you want, say between 5 and 10; and for (4) choose the default value of `360` degrees (and leave the `Z Offset` parameter at its default value of `0`). You should get something that looks like this:

![Fig2](/tutorials/img/cylindrical-tutorial-fig2.png)

However, you may have more than 5 copies of the sphere depending on what value you chose for (3).

Let's apply the `Polar array` transformation again. This time, select all 5 spheres as the object to be arrayed, set the angle to fill equal to `45` degrees, and set the value of `Z Offset` to be `5`. Now, instead of just rotating each copy of your object, the transformation will translate each copy 5 units in the z-direction. You should get something like this, depending on how many copies you chose to make:

![Fig3](/tutorials/img/cylindrical-tutorial-fig3.png)

(Note: the above image was created using `Display` -> `Rendered viewport`, since it doesn't look good when displayed using `Wireframe`.) We get a bunch of stacked spheres, where each level is `5` units higher than the previous, and each pile sweeps through an angle of `45` degrees. If you want, play around with the `Polar array` transformation some more, trying out different values for each of the parameters.

One limitation of the `Polar array` transformation is that it can only rotate and elevate each copy of an object by a constant amount. What if we want to make a twisting stacked structure where the gap between levels increases from one level to the next? The `Polar array` functionality isn't flexible enough to do this, but we can accomplish something similar by writing our own functions in Grasshopper.
