import os
import csv
import numpy as np
import pandas as pd

def open_graph(graph_path):
    open_line_path = graph_path + r"/line_data.csv"
    open_points_path = graph_path + r"/points_data.csv"
    open_play_path = graph_path + r"/play_data.txt"
    open_tra_path = graph_path + r"\point_transform.csv"
    rec_dir = r"C:\Users\zinnu\OneDrive\Desktop\Sprouts-main\Saved Graphs\recent.csv"

    if len(graph_path.split('\\')[-1]) < len(graph_path.split('/')[-1]):
        leaf = graph_path.split('\\')[-1]
    else:
        leaf = graph_path.split('/')[-1]

    try:
        rec_df = pd.read_csv(rec_dir, sep=',', header=None)
        rec_array = rec_df.to_numpy(dtype= str)[1:]
    except:
        rec_list_ar = np.array([[leaf]])
        df = pd.DataFrame(rec_list_ar)
        df.to_csv(rec_dir, index=False)
    else:
        print('saving meep test')
        rec_list = [[str(item[0])] for item in rec_array]
        for i in range(len(rec_list) - 1, -1, -1):
            if rec_list[i] == [leaf]:
                del rec_list[i]
        rec_list.insert(0, [leaf])
        rec_list_ar = np.array(rec_list)
        df = pd.DataFrame(rec_list_ar)
        df.to_csv(rec_dir, index=False)


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

    return open_play, open_degrees_stor, open_points_stor, open_main_stor, open_tra_stor

