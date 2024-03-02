import os
import csv
import numpy as np
import pandas as pd

def save_g(play, main_stor, point_stor, degrees, left_x, top_y):
    parent_dir = r"C:\Users\zinnu\OneDrive\Desktop\Sprouts-main\Computer Junk"
    os.makedirs(parent_dir, exist_ok=True) 

    leaf = 'Computer Data'
    path = os.path.join(parent_dir, leaf) 
    os.makedirs(path, exist_ok=True) 

    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    line_dir = path + r'\line_data.csv'
    points_dir = path + r'\points_data.csv'
    play_dir = path + r'\play_data.txt'
    tra_dir = path + r'\point_transform.csv'
    tra_array = np.array([[left_x, top_y]])
    df = pd.DataFrame(tra_array)
    df.to_csv(tra_dir, index=False)

    xlist = []
    ylist = []
    for point in point_stor:
        xlist.append(point[0])
        ylist.append(point[1])
    points_array = [degrees, xlist, ylist]
    df = pd.DataFrame(points_array)
    df.to_csv(points_dir, index=False)

    line_array = []
    len_list = [len(line) for line in main_stor]
    if len(len_list) > 0:
        max_length = max(len_list)
    else:
        max_length = 0
    for line in main_stor:
        xlist = []
        ylist = []
        for point in line:
            xlist.append(point[0])
            ylist.append(point[1])
        if len(xlist) < max_length:
            while len(xlist) < max_length:
                xlist.append('')
                ylist.append('')
        line_array.append(xlist)
        line_array.append(ylist)

    line_array = np.array(line_array)
    df = pd.DataFrame(line_array)
    df.to_csv(line_dir, index=False)
    #print(df)

    playf = open(play_dir, 'w')
    playf.write(str(play))
