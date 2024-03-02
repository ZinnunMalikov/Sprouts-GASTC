import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
import opening_module_path
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
from matplotlib.patches import Circle
from matplotlib.figure import Figure 
import pandas as pd
import numpy as np
import itertools
import heapq
from shapely import *
from shapelysmooth import *
import copy
import closed_path
import clp_test
import math
import random
import io

def main(graph):
    global fill_image, col_i, colors
    name = r"\Graph " + str(graph)
    source_path = r"C:\Users\zinnu\OneDrive\Desktop\Sprouts-main\Saved Graphs" + name
    image_path = source_path + r'\Plain.png'

    play, degrees, point_stor, main_stor, edges_stor, transforms = opening_module_path.open_graph(source_path)
    for i in range(len(point_stor)):
        x, y = point_stor[i]
        point_stor[i] = (x - transforms[0] + 100, (y - transforms[1] + 100))

    for i in range(len(main_stor)):
        for j in range(len(main_stor[i])):
            x, y = main_stor[i][j]
            main_stor[i][j] = (x - transforms[0] + 100, (y - transforms[1] + 100))

    bound_points_simple = []
    bound_points_full = []
    for edge in edges_stor:
        for point in edge:
            if point not in bound_points_simple:
                bound_points_simple.append(point)
                bound_points_full.append(point_stor[point - 1])


    image = Image.open(image_path)
    width, height = image.size

    # colors = [(255, 153, 153), (255, 204, 153), (255, 255, 153), (204, 255, 153), (153, 255, 153), (153, 255, 204), (153, 255, 255), (153, 204, 255), (153, 153, 255), (204, 153, 255), (255, 153, 255), (255, 153, 204), (255, 102, 102), (255, 178, 102), (255, 255, 102), (178, 255, 102), (102, 255, 102), (102, 255, 178), (102, 255, 255), (102, 178, 255), (102, 102, 255), (178, 102, 255), (255, 102, 255), (255, 102, 178), (255, 204, 204), (255, 229, 204), (255, 255, 204), (229, 255, 204), (204, 255, 204), (204, 255, 299), (204, 255, 255), (204, 229, 255), (204, 204, 255), (255, 204,255), (255, 204, 229)]
    colors= [(216, 108, 108), (229, 131, 114), (242, 157, 121), (255, 184, 127), (216, 173, 108), (229, 200, 114), (242, 230, 121), (248, 255, 127), (195, 216, 108), (189, 229, 114), (181, 242, 121), (172, 255, 127), (130, 216, 108), (120, 229, 114), (121, 242, 133), (127, 255, 159), (108, 216, 151), (114, 229, 177), (121, 242, 205), (127, 255, 235), (108, 216, 216), (114, 212, 229), (121, 205, 242), (127, 197, 255), (108, 151, 216), (114, 143, 229), (121, 133, 242), (133, 127, 255), (130, 108, 216), (154, 114, 229), (181, 121, 242), 
    (210, 127, 255), (195, 108, 216), (223, 114, 229), (242, 121, 230), (255, 127, 223), (216, 108, 173), (229, 114, 166), (242, 121, 157), (255, 127, 146)]

    # print(len(colors))
    random.shuffle(colors)

    col_i = 0
    fig, ax = plt.subplots()
    plt.imshow(image)
    plt.axis('off')

    fill_image = image.copy()
    cursor = Rectangle((0, 0), 0, 0, fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(cursor)

    def dist(tupl1, tupl2):
            return ((tupl2[0] - tupl1[0]) ** 2 + (tupl2[1] - tupl1[1]) ** 2) ** 0.5


    regions = {}

    def coloring():
        global fill_x, fill_y, prev_fill_color, fill, flood_fill
        fill_x, fill_y = 0, 0
        prev_fill_color = (255, 255, 0, 255)

        def fill(x, y):
            global colors, col_i, fig, ax, fill_image, fill_x, fill_y, prev_fill_color, dist, fill, flood_fill
            fill_x, fill_y = int(x), int(y)

            current_fill_color = fill_image.getpixel((fill_x, fill_y))[0:3]

            if current_fill_color[0:3] != (240, 240, 240):
                return

            if col_i == len(colors):
                col_i = 0

            fill_color = colors[col_i]
            col_i += 1
            flood_fill(fill_color)
            plt.draw()

        def flood_fill(fill_color):
            global colors, col_i, fig, ax, fill_image, fill_x, fill_y, prev_fill_color, dist, fill
            width, height = fill_image.size
            pixels = fill_image.load()
            target_color = pixels[fill_x, fill_y]

            stack = [(fill_x, fill_y)]
            visited = set()

            while stack:
                x, y = stack.pop()
                if (x, y) in visited:
                    continue

                visited.add((x, y))

                if (
                    0 <= x < width and
                    0 <= y < height and
                    pixels[x, y] == target_color
                ):
                    pixels[x, y] = fill_color
                    stack.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

            regions[fill_color] = {'points': []}
            plt.imshow(fill_image)

        for i in range(width):
            for j in range(height):
                fill(i, j)

    coloring()

    color_bounds = {}
    min_vbounds = {}
    min_hbounds = {}

    # Iterate through every pixel in the image
    for x in range(width):
        for y in range(height):
            pixel_color = fill_image.getpixel((x, y))[0:3]

            # Skip black border pixels
            # if pixel_color == (0, 0, 0):
            #     continue
            # else:

            # Update bounds for the current color
            if pixel_color not in color_bounds and pixel_color:
                color_bounds[pixel_color] = {'left': x, 'right': x, 'top': y, 'bottom': y}
            else:
                color_bounds[pixel_color]['left'] = min(color_bounds[pixel_color]['left'], x)
                color_bounds[pixel_color]['right'] = max(color_bounds[pixel_color]['right'], x)
                color_bounds[pixel_color]['top'] = min(color_bounds[pixel_color]['top'], y)
                color_bounds[pixel_color]['bottom'] = max(color_bounds[pixel_color]['bottom'], y)

    # Print or use the calculated bounds
    # for color, bounds in color_bounds.items():
    #     print(f"Color: {color}, Bounds: {bounds}")

    horz_lines = []
    vert_lines = []
    for color in color_bounds:
        if color != (0,0, 0):
            horz_lines.append(color_bounds[color]['left'])
            horz_lines.append(color_bounds[color]['right'])
            vert_lines.append(color_bounds[color]['top'])
            vert_lines.append(color_bounds[color]['bottom'])

    # for point in point_stor:
    #     horz_lines.append(point[0])
    #     vert_lines.append(point[1])

    # print(col_i)
    for color in color_bounds:
        min_vbounds[color] = (height, 0)
        min_hbounds[color] = (width, 0)

    previous_color = fill_image.getpixel((0, 0))[0:3]

    for x in range(width):
        diffs = [abs(x - line) for line in horz_lines]
        if min(diffs) > 30:
            current = 0
            for y in range(height):
                current_color = fill_image.getpixel((x, y))[0:3]
                # print(current_color)
                if (current_color == previous_color):
                    current += 1
                else:
                    if current > 10 and current < min_vbounds[previous_color][0]:
                        min_vbounds[previous_color] = (current, x)
                    current = 0
                    
                previous_color = current_color

    for y in range(height):
        diffs = [abs(y - line) for line in vert_lines]
        if min(diffs) > 30:
            current = 0
            for x in range(width):
                current_color = fill_image.getpixel((x, y))[0:3]
                # print(current_color)
                if (current_color == previous_color):
                    current += 1
                else:
                    if current > 10 and current < min_hbounds[previous_color][0]:
                       min_hbounds[previous_color] = (current, y)
                    current = 0
                    
                previous_color = current_color

    # print(min_hbounds)
    # print(min_vbounds)
    print('* * * * * * * * * ** * * * * * * * * * * * *')
    print(regions)
    print(color_bounds)

    debug_pixels = fill_image.load()
    debug_bad_cols = []
    for debugc, debugd in color_bounds.items():
        if (abs(debugd['left'] - debugd['right']) <= 5 or abs(debugd['top'] - debugd['bottom']) < 5):
            debug_bad_cols.append(debugc)
            for deb_i in range(debugd['left'], debugd['right']+1):
                for deb_j in range(debugd['top'], debugd['bottom']+1):
                    if fill_image.getpixel((deb_i, deb_j))[0:3] == debugc:
                        debug_pixels[deb_i, deb_j] = (0, 0, 0)
    print('bad cols')
    print(debug_bad_cols)
    print('* * * * * * * * * ** * * * * * * * * * * * *')
    for bad_col in debug_bad_cols:
        if bad_col in list(regions.keys()):
            del regions[bad_col]
        
        if bad_col in list(color_bounds.keys()):
            del color_bounds[bad_col]

    #     except:
    #         pass
        # else:
        #     del color_bounds[bad_col]
        #     del regions[bad_col]

    # print(color_bounds)


    # Show plot
    plt.close('all')
    plt.imshow(fill_image)
    for i, point in enumerate(point_stor):
        x, y = point
        plt.scatter(x , y, marker='o', color="lime", edgecolors='black')
        plt.annotate(str(i + 1), (x + 5, y + 5))

    # print(regions)
    def check_color(point, color, source):
        adj_cols = []
        x, y = point
        for j in range(-15, 15):
            for k in range(-15, 15):
                px_col = source.getpixel((x + j, y + k))[0:3]
                if px_col[0:3] != (240, 240, 240) and px_col[0:3] != (0, 0, 0) and px_col[0:3] not in adj_cols:
                    adj_cols.append(px_col[0:3])
        if color in adj_cols:
            return True
        else:
            return False

    for rgb, rdata in regions.items():
        rdata['points'] = []

    for rgb, rdata in regions.items():
        for point in point_stor:
            if check_color(point, rgb, fill_image) and point in bound_points_full:
                rdata['points'].append(point_stor.index(point) + 1)

    # # print(edges_stor)
    # for item, rdata in regions.items():
    #      print(item, rdata)
    print(regions)
    plt.imshow(fill_image)
    
    set_representation = []
    dict_representation = []
    dict_inds = []
    for rgb, rdata in regions.items():
        if True: #not rgb == colors[0]:
            bd_points = list(rdata['points'])
            temp_edges = []
            temp_edges_inds= []
            for i in range(len(edges_stor)):
                if edges_stor[i][0] in bd_points and edges_stor[i][1] in bd_points:
                    if check_color(main_stor[i][math.floor(len(main_stor[i])/2)], rgb, fill_image):
                        temp_edges.append(edges_stor[i])
                        temp_edges_inds.append(i)
            
            # print(temp_edges)
            ordering = [[]]
            ordering_inds = [[]]
            len_o = len(temp_edges)
            # print(ordering)
            init = 0
            while len_o > 0: 
                accum = 0
                for i, edge in enumerate(temp_edges):
                    if temp_edges[i] != -1:
                        if init == 0:
                            init += 1
                            accum += 1
                            ordering[-1].append(edge)
                            ordering_inds[-1].append(temp_edges_inds[i])
                            temp_edges[i] = -1
                        elif ordering[-1][-1][-1] == edge[0]:
                            accum += 1
                            ordering[-1].append(edge)
                            ordering_inds[-1].append(temp_edges_inds[i])
                            temp_edges[i] = -1
                        elif ordering[-1][-1][-1] == edge[1]:
                            accum += 1
                            r_edge = (edge[1], edge[0])
                            ordering[-1].append(r_edge)
                            ordering_inds[-1].append(temp_edges_inds[i])
                            temp_edges[i] = -1
                    
                if accum == 0:
                    ordering.append([])
                    ordering_inds.append([])
                    init = 0
            
                len_o = 0
                for obj in temp_edges:
                    if obj != -1:
                        len_o += 1
            
            rbounds = []
            for i in range(len(ordering_inds)):
                rleft_x, rright_x, rtop_y, rbottom_y = [], [], [], []
                for ind in ordering_inds[i]:
                    line = main_stor[ind]
                    rleft_x.append(min(line, key=lambda x: x[0])[0])
                    rright_x.append(max(line, key=lambda x: x[0])[0])
                    rtop_y.append(min(line, key=lambda x: x[1])[1])
                    rbottom_y.append(max(line, key=lambda x: x[1])[1])
                
                if len(rleft_x) > 0 and len(rright_x) > 0 and len(rtop_y) > 0 and len(rbottom_y) > 0:
                    rbounds.append((min(rleft_x), max(rright_x), min(rtop_y), max(rbottom_y)))
            
            largest_region = 0
            if len(ordering) > 1 and rgb != colors[0]:
                prev = rbounds[0]
                for i in range(len(rbounds)):
                    current = rbounds[i]
                    if current[0] < prev[0] and current[1] > prev[1] and current[2] < prev[2] and current[3] > prev[3]:
                        largest_region = i
                    prev = rbounds[i]
            
                # print('largest: ', ordering[largest_region])
                # print(ordering_inds[largest_region])
            
                inner_regions = copy.deepcopy(ordering)
                inner_inds = copy.deepcopy(ordering_inds)
                del inner_regions[largest_region]
                del inner_inds[largest_region]
            # print(ordering)
            set_representation.append(bd_points)
            if len(ordering) ==  1:
                inner_regions = []
                inner_inds = []
            
            if rgb != colors[0]:
                dict_representation.append({'boundary': ordering[largest_region], 'inner': inner_regions})
                dict_inds.append({'boundary': ordering_inds[largest_region], 'inner': inner_inds})
            else:
                dict_representation.append({'boundary': [], 'inner': ordering})
                dict_inds.append({'boundary': [], 'inner': ordering_inds})
            # print('*')


    for i, point in enumerate(point_stor):
        x, y = point
        plt.scatter(x , y, marker='o', color="lime", edgecolors='black', zorder= 1)
        plt.annotate(str(i + 1), (x + 10, y + 20), color = 'red')
    
    for i in range(len(set_representation)):
        for j in range(len(point_stor)):
            if degrees[j] == 0 and check_color(point_stor[j], colors[i], fill_image):
                set_representation[i].append(j + 1)

    # print(set_representation)
    # print(dict_representation)
    # print(dict_inds)
        

    # print(edges_stor)
    # plt.close('all')
    # plt.figure()
    # plt.imshow(fill_image)
    # for i, point in enumerate(point_stor):
    #     x, y = point
    #     plt.scatter(x , y, marker='o', color="lime", edgecolors='black', zorder= 1)
    #     plt.annotate(str(i + 1), (x + 10, y + 20), color = 'red')

    # section = 2
    # for path in dict_inds[section]['inner']:
    #     # print(path)
    #     for ind in path:
    #         x_val = [x[0] for x in main_stor[ind]]
    #         y_val = [x[1] for x in main_stor[ind]]
    #         plt.scatter(x_val, y_val, s = 2, color = 'red')

    # for ind in dict_inds[section]['boundary']:
    #         x_val = [x[0] for x in main_stor[ind]]
    #         y_val = [x[1] for x in main_stor[ind]]
    #         plt.scatter(x_val, y_val, s = 2, color = 'red')
    
    plt.close('all')
    # plt.show()

    point_names = [-1] + list(map(chr, range(97, 123)))
    new_set_rp = []
    for obj in set_representation:
        new_set = []
        for point in obj:
            new_set.append(point_names[point])
        new_set_rp.append(new_set)
    
    new_dict_rp = []
    for obj in dict_representation:
        newB = []
        newI = []
        if len(obj['boundary']) > 0:
            for edge in obj['boundary']:
                newE = []
                for point in edge:
                    newE.append(point_names[point])
                newB.append(newE)

        if len(obj['inner']) > 0:
            for bound in obj['inner']:
                for edge in bound:
                    newE = []
                    for point in edge:
                        newE.append(point_names[point])
                    newI.append(newE)
        new_dict_rp.append({'boundary': newB, 'inner': newI})

        


    return fill_image, new_set_rp, new_dict_rp, dict_inds
# main(1)