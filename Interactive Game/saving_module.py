import os
import csv
import numpy as np
import pandas as pd

def save_g(play, main_stor, point_stor, degrees, left_x, top_y, override, choice):
    parent_dir = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs"
    os.makedirs(parent_dir, exist_ok=True) 

    try:
        f = open(parent_dir + '\count.txt', "x")
    except:
        pass

    try:
        cr1 = open(parent_dir + '\\recent.csv', "x")
    except:
        pass

    f = open(parent_dir + '\count.txt', "r")
    if f.read() == '':
        #print('jeep')
        count = 1
    else:
        f1 = open(parent_dir + '\count.txt', "r")
        count = f1.read()
        count = int(count)
    
    if not override:
        f = open(parent_dir + '\count.txt', "w")
        f.write(str(count + 1))

    if override:
        leaf = 'Graph ' + str(choice)
    else:
        leaf = 'Graph ' + str(count)
    path = os.path.join(parent_dir, leaf) 
    os.makedirs(path, exist_ok=True) 

    rec_dir = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\recent.csv"
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

    if not override:
        return count
    else:
        return choice
