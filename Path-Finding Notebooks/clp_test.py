import closed_path

def generate_closed(comb, adj_filt_loop_i, cas):
    adj_filt_loop = adj_filt_loop_i/1.414
    cpoints = []

    if cas ==1:
        for cx in range(comb[0] + 1, int(round(comb[0] + adj_filt_loop * 2**0.5))):
            for cy in range(comb[1] + 1, round(comb[1] + adj_filt_loop * 2**0.5)):
                if abs((cx - (comb[0] + adj_filt_loop/2)) ** 2 + (cy - (comb[1]+adj_filt_loop/2)) ** 2 -(adj_filt_loop/2)**2 *2) < 4:
                    cpoints.append((cx, cy))

    if cas ==2:
        for cx in range(int(round(comb[0] - adj_filt_loop * 2**0.5)), comb[0]):
            for cy in range(comb[1] + 1, round(comb[1] + adj_filt_loop * 2**0.5)):
                if abs((cx - (comb[0] - adj_filt_loop/2)) ** 2 + (cy - (comb[1]+adj_filt_loop/2)) ** 2 -(adj_filt_loop/2)**2 *2) < 4:
                    cpoints.append((cx, cy))

    if cas ==3:
        for cx in range(int(round(comb[0] - adj_filt_loop * 2**0.5)), comb[0]):
            for cy in range(round(comb[1] - adj_filt_loop * 2**0.5), comb[1]):
                if abs((cx - (comb[0] - adj_filt_loop/2)) ** 2 + (cy - (comb[1]-adj_filt_loop/2)) ** 2 -(adj_filt_loop/2)**2 *2) < 4:
                    cpoints.append((cx, cy))

    if cas ==4:
        for cx in range(comb[0] + 1, int(round(comb[0] + adj_filt_loop * 2**0.5))):
            for cy in range(round(comb[1] - adj_filt_loop * 2**0.5), comb[1]):
                if abs((cx - (comb[0] + adj_filt_loop/2)) ** 2 + (cy - (comb[1] - adj_filt_loop/2)) ** 2 -(adj_filt_loop/2)**2 *2) < 4:
                    cpoints.append((cx, cy))      

    points = cpoints
    points.append(comb)
    n = len(points)

    return closed_path.printClosedPath(points, comb, len(points))
