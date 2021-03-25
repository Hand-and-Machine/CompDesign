def distance(p1, p2):
    dim = len(p1)
    dist = 0
    for n in range(dim):
        dist += (p1[n]-p2[n])**2
    dist = dist**(1/2)
    return dist

def floormap(num, stepsizes):
    num_steps = len(stepsizes)
    image = num_steps
    cumsum = 0
    for i in range(num_steps):
        cumsum += stepsizes[i]
        if cumsum >= num:
            image = i
            return image
    return image

def segment_map(segments):
    dim = len(segments[0][0])
    lengths = [distance(s[0], s[1]) for s in segments]
    total_length = sum(lengths)
    def map(x):
        x = (x * total_length) % total_length
        n = floormap(x, lengths)
        cumsum = sum(lengths[:n])
        prop = (x - cumsum)/lengths[n]
        seg = segments[n]
        image = [(1-prop)*seg[0][i] + prop*seg[1][i] for i in range(dim)]
        return image
    return map
