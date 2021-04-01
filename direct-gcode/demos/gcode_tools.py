import sys
import re
import random

## Calculate the squared distance between two points.
def norm_dist(p1, p2):
    dim = len(p1)
    return sum([(p1[i]-p2[i])**2 for i in range(dim)])

## Given a GCODE command, extract the X, Y, Z, and E coordinates
## if it is a G1 linear interpolation command.
def extract_coords(command):
    coords = [False, False, False, False]
    xmatch = re.match("G1( .*)? X([0-9\.]+)(\s|$)", command)
    ymatch = re.match("G1( .*)? Y([0-9\.]+)(\s|$)", command)
    zmatch = re.match("G1( .*)? Z([0-9\.]+)(\s|$)", command)
    ematch = re.match("G1( .*)? E([0-9\.]+)(\s|$)", command)
    if xmatch: coords[0] = float(xmatch[2])
    if ymatch: coords[1] = float(ymatch[2])
    if zmatch: coords[2] = float(zmatch[2])
    if ematch: coords[3] = float(ematch[2])
    return coords

## Find the maximum, minimum, and average X, Y, and Z values
## for the extruder in a GCODE file.
def coord_stats(filename):
    xvals = []
    yvals = []
    zvals = []
    with open(filename) as file:
        for line in file:
            c = extract_coords(line)
            if c[0] != False: xvals.append(c[0])
            if c[1] != False: yvals.append(c[1])
            if c[2] != False: zvals.append(c[2])
    stats = {
        "max": [max(xvals), max(yvals), max(zvals)],
        "min": [min(xvals), min(yvals), min(zvals)],
        "avg": [np.average(xvals), np.average(yvals), np.average(zvals)]
    }
    return stats

## Given a GCODE command and (optional) values of X, Y, Z, E,
## substitute those values into the command.
def substitute_coords(x, y, z, e, string):
    new_str = string
    if x: new_str = re.sub(r"X[0-9\-\.]+($|\s)", "X"+str(x)+" ", new_str)
    if y: new_str = re.sub(r"Y[0-9\-\.]+($|\s)", "Y"+str(y)+" ", new_str)
    if z: new_str = re.sub(r"Z[0-9\-\.]+($|\s)", "Z"+str(z)+" ", new_str)
    if e: new_str = re.sub(r"E[0-9\-\.]+($|\s)", "E"+str(e)+" ", new_str)
    return new_str

## Optionally remove the X, Y, Z, or E components of a GCODE command.
def delete_coords(x, y, z, e, string):
    new_str = string
    if x: new_str = re.sub(r"X[0-9\-\.]+($|\s)", "", new_str)
    if y: new_str = re.sub(r"Y[0-9\-\.]+($|\s)", "", new_str)
    if z: new_str = re.sub(r"Z[0-9\-\.]+($|\s)", "", new_str)
    if e: new_str = re.sub(r"E[0-9\-\.]+($|\s)", "", new_str)
    return new_str
