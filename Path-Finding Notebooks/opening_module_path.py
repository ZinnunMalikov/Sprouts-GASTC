import os
import csv
import numpy as np
import pandas as pd

def curve_dist(inp):
        curve_dist = 0
        for i in range(len(inp) - 1):
            curve_dist += ((inp[i + 1][0] - inp[i][0]) ** 2 + (inp[i + 1][1] - inp[i][1]) ** 2) ** 0.5
        return curve_dist

def open_graph(graph_path):
    open_line_path = graph_path + r"/line_data.csv"
    open_points_path = graph_path + r"/points_data.csv"
    open_play_path = graph_path + r"/play_data.txt"
    open_tra_path = graph_path + r"\point_transform.csv"

    open_f = open(open_play_path, "r")
    open_play = open_f.read()
    open_play = int(open_play)
    open_line_df = pd.read_csv(open_line_path, sep=',', header=None)
    open_line_df = open_line_df.fillna('9999')
    open_line_array = open_line_df.to_numpy(dtype = float)[1:]
    open_points_df = pd.read_csv(open_points_path, sep=',', header=None)
    open_points_array = open_points_df.to_numpy(dtype = float)[1:]
    open_tra_df = pd.read_csv(open_tra_path , sep=',', header=None)
    open_tra_array = open_tra_df.to_numpy(dtype = float)[1:]
    open_tra_stor = [open_tra_array[0][0], open_tra_array[0][1]]

    open_degrees_stor = [int(deg) for deg in open_points_array[0]]

    open_points_stor = []
    for i in range(len(open_points_array[0])):
        open_points_stor.append((open_points_array[1][i], open_points_array[2][i]))

    open_main_stor = []
    for i in range(int(len(open_line_array)/2)):
        open_line = []
        for j in range(len(open_line_array[i])):
            if open_line_array[2*i][j] < 9999:
                open_line.append((open_line_array[2*i][j], open_line_array[2*i + 1][j]))
        open_main_stor.append(open_line)

    open_edges_stor = []
    for line in open_main_stor:
        edge = (open_points_stor.index(line[0]) + 1, open_points_stor.index(line[-1]) + 1)
        open_edges_stor.append(edge)

    return open_play, open_degrees_stor, open_points_stor, open_main_stor, open_edges_stor, open_tra_stor

