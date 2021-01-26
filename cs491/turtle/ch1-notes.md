- Basic commands
	- `FORWARD x` and `BACK x`, implemented in Processing as `.forward(x)` and `.back(x)`
	- `LEFT theta` and `RIGHT theta`, implemented as `.left(theta)` and `.right(theta)`
	- `PENUP` and `PENDOWN`, implemented as `.penUp()` and `.penDown()`
	- `REPEAT n`, implemented as a `for` loop
- A potential stumbling block is that, when using the Turtle, we must measure polygons by their exterior angles, not their interior angles
	- These are supplementary to the interior angles
- <details> <summary> Here's a geometry puzzle: if a circle is created (approximately) by repeatedly running <code><pre>FORWARD x, RIGHT theta</pre></code>, for some small value of <code><pre>theta</pre></code>, what will the radius of the approximated circle be? </summary> The radius is <code><pre>x/(2*sin(theta/2))</pre></code>, which is approximately <code><pre>x/theta</pre></code> for small values of <code><pre>theta</pre></code>. </details> 