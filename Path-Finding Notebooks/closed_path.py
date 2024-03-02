from functools import cmp_to_key
p0 = None
def dist(p1, p2):
    return (p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1])

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0: return 0  # collinear
    return 1 if val > 0 else 2 # clockwise or counterclock wise
def compare(vp1, vp2):
    p1 = vp1
    p2 = vp2

    o = orientation(p0, p1, p2)
    if o == 0:
        return -1 if dist(p0, p2) >= dist(p0, p1) else 1

    return -1 if o == 2 else 1

def printClosedPath(points, comb, n):
    global p0
    # Find the bottommost point
    ymin = points[0][1]
    min = 0
    for i in range(1,n):
        y = points[i][1]

        if (y < ymin) or (ymin == y and points[i][0] < points[min][0]):
            ymin = points[i][1]
            min = i

    temp = points[0]
    points[0] = points[min]
    points[min] = temp

    p0 = points[0]
    points.sort(key=cmp_to_key(compare))

    pathl = []
    for i in range(n):
      pathl.append((points[i][0],points[i][1]))
    origin = pathl.index(comb)
    pathf = pathl[origin:] + pathl[:origin] + [comb]
    return(pathf)

# Driver program to test above functions
# points = cpoints
# points.append(comb)
# n = len(points)

# print(printClosedPath(points, n))
