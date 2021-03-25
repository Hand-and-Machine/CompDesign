import numpy as np

class Extruder:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.gcode = []
        self.density = 0
        self.position_cache = (0,0,0)
        self.density_cache = 0

    def dwell(self, ms):
        cmd = "G04 P" + str(ms)
        self.gcode.append(cmd)

    def extrude(self, e):
        cmd = "G1 E" + str(e)
        self.gcode.append(cmd)

    def drawline(self, x, y, z=0):
        dist = ((x-self.x)**2+(y-self.y)**2+(z-self.z)**2)**(1/2)
        extrude = dist * self.density
        cmd = "G1"
        if x != self.x: cmd += " X" + str(x)
        if y != self.y: cmd += " Y" + str(y)
        if z != self.z: cmd += " Z" + str(z)
        if self.density != 0: cmd += " E" + str(extrude)
        self.gcode.append(cmd)
        self.x = x
        self.y = y
        self.z = z

    def set_density(self, density):
        self.density = density

    def get_density(self):
        return self.density

    def cache_density(self):
        self.density_cache = self.density

    def reset_density(self):
        self.density = self.density_cache

    def cache_position(self):
        self.position_cache = (self.x, self.y, self.z)

    def reset_position(self):
        pc = self.position_cache
        self.x = pc[0]
        self.y = pc[1]
        self.z = pc[2]

    def goto(self, x, y, z=0):
        self.cache_density()
        self.set_density(0)
        if z == 0:
            self.drawline(x, y, self.z)
        else:
            self.drawline(x, y, z)
        self.reset_density()

    def setz(self, z):
        self.cache_density()
        self.set_density(0)
        self.drawline(self.x, self.y, z)
        self.reset_density()

    def drawdelta(self, dx, dy, dz=0):
        self.drawline(self.x + dx, self.y + dy, self.z + dz)

    def move(self, dx, dy, dz=0):
        self.cache_density()
        self.set_density(0)
        self.drawdelta(dx, dy, dz)
        self.reset_density()

    def lift(self, dz):
        self.cache_density()
        self.set_density(0)
        self.drawdelta(0, 0, dz)
        self.reset_density()

    def initialize(self):
        cmd = "G90\nM83\nM104 S215\nM140 S60\nM190 S60\nM109 S215\nG21\nG92 E0\nG28 W\nG80\n"
        self.gcode.append(cmd)

    def finalize(self):
        cmd = "\nM104 S0\nM140 S0\nM107\nG1 Z81.5\nM84"
        self.gcode.append(cmd)

    ## WARNING: will overwrite files!
    def save(self, filename):
        f = open(filename, 'w')
        for cmd in self.gcode:
            f.write(cmd + "\n")
        f.close()

    def rectangle(self, x_len, y_len):
        self.drawdelta(x_len, 0)
        self.drawdelta(0, y_len)
        self.drawdelta(-x_len, 0)
        self.drawdelta(0, -y_len)

    def circle(self, radius, n):
        self.cache_position()
        self.move(radius, 0)
        x_diffs = [np.cos(2*np.pi*(k+1)/n) - np.cos(2*np.pi*k/n) for k in range(n)]
        y_diffs = [np.sin(2*np.pi*(k+1)/n) - np.sin(2*np.pi*k/n) for k in range(n)]
        for i in range(n):
            x_diff = x_diffs[i]
            y_diff = y_diffs[i]
            self.drawdelta(x_diff, y_diff)
        self.reset_position()

    def rect_spiral(self, x_len, y_len, delta, dwell=0):
        x_move = x_len
        y_move = y_len
        sgn = 1
        while x_move > 0 and y_move > 0:
            self.drawdelta(sgn*x_move, 0)
            self.drawdelta(0, sgn*y_move)
            x_move += -delta
            y_move += -delta
            sgn = -sgn
            self.dwell(dwell)