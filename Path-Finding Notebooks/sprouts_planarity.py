import matplotlib
matplotlib.use('Agg')
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
    name = r"\Graph " + str(graph)
    source_path = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs" + name
    image_path = source_path + r'\Plain.png'
    point_names = [-1] + list(map(chr, range(97, 123)))

    for letter in list(map(chr, range(65, 91))):
        point_names.append(letter)
    
    for i, letter in enumerate(list(map(chr, range(97, 123)))):
        point_names.append(str(letter) + str(i + 1))


    play, degrees, point_stor, main_stor, edges_stor, transforms = opening_module_path.open_graph(source_path)
    for i in range(len(point_stor)):
        x, y = point_stor[i]
        point_stor[i] = (x - transforms[0] + 100, (y - transforms[1] + 100))

    for i in range(len(main_stor)):
        for j in range(len(main_stor[i])):
            x, y = main_stor[i][j]
            main_stor[i][j] = (x - transforms[0] + 100, (y - transforms[1] + 100))
    
    new_eds = []
    for edge in edges_stor:
        new_edge = []
        for point in edge:
            new_edge.append(point_names[point])
        new_eds.append(new_edge)
    

    return point_stor, main_stor, point_names, degrees, play, new_eds

