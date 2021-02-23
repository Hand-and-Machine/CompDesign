def stringify_vec(vec):
    s = ""
    for x in vec: s += str(x) + " "
    return s

def distance(p1, p2):
    pv1 = np.asarray(p1)
    pv2 = np.asarray(p2)
    return np.linalg.norm(pv1 - pv2)
