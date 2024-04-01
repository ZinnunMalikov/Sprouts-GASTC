import tkinter as tk
from shapely import *
from shapelysmooth import *
import time
import math
import copy
#import pyvisgraph as vg
import pickle
import itertools
from PIL import ImageGrab
from csv import writer
import numpy as np

class smooth_fix:
    global curve_dist, dist, abs_mouse, redraw_p, draw_bound

    def __init__(self, root):
        self.root = root
        self.root.title('Game of Sprouts')
        self.bound = 600
        self.canvas = tk.Canvas(self.root, width = self.bound, height = self.bound)
        self.canvas.pack()

        self.canvas.focus_set()

        self.canvas.bind('<ButtonPress-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<Motion>', self.cursor)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        self.canvas.bind('<Control-p>', self.point_view)
        self.canvas.bind('<Control-t>', self.text_view)
        self.canvas.bind('<Control-i>', self.image_grab)

        self.is_drawing = False
        self.good_start = False
        self.line_id = None
        self.length = False
        self.main_stor = []
        self.line_stor = []
        self.freq = 1
        
        self.play = 0
        self.detection = 8
        self.inst = False
        self.temp_circle = 0
        self.buffer = 0
        self.min_buffer = 0
        self.break_case = False

        self.nump = 4

        self.point_stor = [((self.bound/2) + (100*self.bound/500)*np.cos(pim * 2*np.pi/self.nump), (self.bound/2) + (100*self.bound/500)*np.sin(pim * 2*np.pi/self.nump)) for pim in range(self.nump)]
        self.degrees = [0]*len(self.point_stor)
        self.junk_degrees = [0]*len(self.point_stor)
        self.disp_point_stor, self.junk_stor, self.disp_text_stor = [], [], []
        self.temp_deg_stor = []

        self.path_points = []
        self.rec_bound = 0
        self.pos_disp = (0, 0)
        self.play_disp = (0, 0)
        self.playerq_disp = (0, 0)
        self.text_toggle = False
        self.point_toggle = False

        self.left_x = min(self.point_stor)[0] - 50
        self.right_x = max(self.point_stor)[0] + 50
        self.top_y = min(self.point_stor)[1] - 50
        self.bottom_y = max(self.point_stor)[1] + 70
        print( max(self.point_stor)[1])

        left_x = []
        right_x = []
        top_y = []
        bottom_y = []

        left_x.append(min(self.point_stor, key=lambda x: x[0])[0])
        right_x.append(max(self.point_stor, key=lambda x: x[0])[0])
        top_y.append(min(self.point_stor, key=lambda x: x[1])[1])
        bottom_y.append(max(self.point_stor, key=lambda x: x[1])[1])
        
        left_x.append(min(self.point_stor, key=lambda x: x[0])[0])
        right_x.append(max(self.point_stor, key=lambda x: x[0])[0])
        top_y.append(min(self.point_stor, key=lambda x: x[1])[1])
        bottom_y.append(max(self.point_stor, key=lambda x: x[1])[1])

        self.left_x = min(left_x) - 100
        self.right_x = max(right_x) + 100
        self.top_y = min(top_y) - 100
        self.bottom_y = max(bottom_y) + 100
        
        self.spec_image_points = []


        self.image_points = self.point_stor

        for i, point in enumerate(self.point_stor):
            x, y = point[0], point[1]
            self.disp_point_stor.append((self.canvas.create_oval(x - self.detection/2, y - self.detection/2, x + self.detection/2, y + self.detection/2, fill = 'red')))
            self.disp_text_stor.append(self.canvas.create_text(x, y + 10, font = ('Times', 10), text = str(self.degrees[i])))

    def abs_mouse(self, x, y):
        self.canvas.event_generate('<Motion>', warp = True, x = x, y= y)
   
    def dist(tupl1, tupl2):
        return ((tupl2[0] - tupl1[0]) ** 2 + (tupl2[1] - tupl1[1]) ** 2) ** 0.5

    def curve_dist(inp):
        curve_dist = 0
        for i in range(len(inp) - 1):
            curve_dist += ((inp[i + 1][0] - inp[i][0]) ** 2 + (inp[i + 1][1] - inp[i][1]) ** 2) ** 0.5
        return curve_dist
   
    def redraw_p(self):
        for point in self.disp_point_stor:
            self.canvas.delete(point) 
        for text in self.disp_text_stor:
            self.canvas.delete(text) 

        self.disp_point_stor = []
        for i, point in enumerate(self.point_stor):
            x, y = point[0], point[1]
            self.disp_point_stor.append((self.canvas.create_oval(x - self.detection/2, y - self.detection/2, x + self.detection/2, y + self.detection/2, fill = 'red')))
            self.disp_text_stor.append(self.canvas.create_text(x, y + 10, font = ('Times', 10), text = str(self.degrees[i])))
            if self.point_toggle == True:
                self.canvas.itemconfig(self.disp_point_stor[-1], state = 'hidden')
            if self.text_toggle == True:
                self.canvas.itemconfig(self.disp_text_stor[-1], state = 'hidden')
    
    def draw_bound(self):
        left_x = []
        right_x = []
        top_y = []
        bottom_y = []

        for line in self.main_stor:
            left_x.append(min(line, key=lambda x: x[0])[0])
            right_x.append(max(line, key=lambda x: x[0])[0])
            top_y.append(min(line, key=lambda x: x[1])[1])
            bottom_y.append(max(line, key=lambda x: x[1])[1])
        
        left_x.append(min(self.point_stor, key=lambda x: x[0])[0])
        right_x.append(max(self.point_stor, key=lambda x: x[0])[0])
        top_y.append(min(self.point_stor, key=lambda x: x[1])[1])
        bottom_y.append(max(self.point_stor, key=lambda x: x[1])[1])

        self.left_x = min(left_x) - 50
        self.right_x = max(right_x) + 50
        self.top_y = min(top_y) - 50
        self.bottom_y = max(bottom_y) + 70
        if self.rec_bound != 0:
            print('deleting')
            self.canvas.delete(self.rec_bound)
        self.rec_bound = self.canvas.create_rectangle(self.left_x, self.top_y, self.right_x, self.bottom_y, width = 2)

    def start_drawing(self, event):
        print('play: ', self.play + 1)
        print('points: ', self.point_stor)
        print('lines: ', len(self.main_stor))
        print('degrees: ', self.degrees)
        self.canvas.delete(self.play_disp)
        self.play_disp = self.canvas.create_text(23, 25,  font = ('Times', 10), text = 'Play: ' + str(self.play + 1))
        self.canvas.delete(self.playerq_disp)
        self.playerq_disp = self.canvas.create_text(44, 40,  font = ('Times', 10), text = 'Player ' + str(self.play %2 + 1) + "'s Turn")
        self.junk_stor = []

        redraw_p(self)    
        self.good_start = False
        self.is_drawing = False
        for start_point in self.point_stor:
            if dist((event.x, event.y), start_point) <= self.detection * 1.7 and self.degrees[self.point_stor.index(start_point)] < 3:
                self.good_start = True
                start = start_point
                break
       
        if self.good_start == True:
            x, y = start
            abs_mouse(self, x, y)
            #print('Start', start)
            self.is_drawing = True
            self.break_case = False
            self.junk_stor.append([start])
            self.play += 1
            self.line_id = self.canvas.create_line(x, y, x, y)
            #time.sleep(0.4)
            #print('Good Start')
            ##print(junk_stor, self.play)
        else:
            print('Bad Start')
   
    def cursor(self, event):
        self.canvas.delete(self.pos_disp)
        self.pos_disp = self.canvas.create_text(30, 10,  font = ('Times', 10), text = str((event.x, event.y)))
        self.canvas.update()

        if self.inst == False:
            self.buffer = [dist(point, (event.x, event.y)) for point in self.point_stor]
            self.min_buff = self.point_stor[self.buffer.index(min(self.buffer))]
            #print(self.point_stor)
            self.temp_circ = self.canvas.create_oval(self.min_buff[0]- self.detection, self.min_buff[1]- self.detection, self.min_buff[0]+ self.detection, self.min_buff[1]+ self.detection, outline = 'blue')
            self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
            self.inst = True
        
        if self.inst == True:
            ##print(self.temp_circ)
            if dist(self.min_buff, (event.x, event.y)) < self.detection:
                self.canvas.itemconfigure(self.temp_circ, state = tk.NORMAL)
                self.canvas.update()
            else:
                self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
                self.inst == False
                self.buffer = [dist(point, (event.x, event.y)) for point in self.point_stor]
                self.min_buff = self.point_stor[self.buffer.index(min(self.buffer))]
                self.temp_circ = self.canvas.create_oval(self.min_buff[0] - self.detection, self.min_buff[1]- self.detection, self.min_buff[0]+ self.detection, self.min_buff[1]+ self.detection, outline = 'blue')
                self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
                self.canvas.update()

    def draw(self, event):
        global curve_dist, dist   
        if self.inst == False:
            self.buffer = [dist(point, (event.x, event.y)) for point in self.point_stor]
            self.min_buff = self.point_stor[self.buffer.index(min(self.buffer))]
            #print(self.point_stor)
            self.temp_circ = self.canvas.create_oval(self.min_buff[0] - self.detection, self.min_buff[1]- self.detection, self.min_buff[0]+ self.detection, self.min_buff[1]+ self.detection, outline = 'blue')
            self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
            self.inst = True
        
        if self.inst == True:
            ##print(self.temp_circ)
            if dist(self.min_buff, (event.x, event.y)) < self.detection:
                self.canvas.itemconfigure(self.temp_circ, state = tk.NORMAL)
                self.canvas.update()
            else:
                self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
                self.inst == False
                self.buffer = [dist(point, (event.x, event.y)) for point in self.point_stor]
                self.min_buff = self.point_stor[self.buffer.index(min(self.buffer))]
                self.temp_circ = self.canvas.create_oval(self.min_buff[0] - self.detection, self.min_buff[1]- self.detection, self.min_buff[0]+ self.detection, self.min_buff[1]+ self.detection, outline = 'blue')
                self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
                self.canvas.update()
        self.length = False

        if self.is_drawing:
            if event.x >= self.bound - 20:
                abs_mouse(self, self.bound - 20, event.y)
            if event.y >= self.bound - 20:
                abs_mouse(self, event.x, self.bound - 20)
            if self.junk_stor[-1][-1]!= (event.x, event.y):
                self.canvas.coords(self.line_id, self.canvas.coords(self.line_id) + [event.x, event.y])
                self.junk_stor[-1].append((event.x, event.y))
                self.freq += 1

            if curve_dist(self.junk_stor[-1]) > 2*self.detection:
                if self.break_case != True:
                    self.length = True
                if self.freq % 5 == 0:
                    line = LineString(self.junk_stor[-1])
                    if not line.is_simple:
                        print('self-intersect')
                        self.length = False
                        self.break_case = True
                        return
                    for data in self.main_stor:
                        if intersection(LineString(self.junk_stor[-1]), LineString(data)):
                            temp_str = str(intersection(LineString(self.junk_stor[-1][5:-1]), LineString(data)))
                            split = 0
                            if temp_str.startswith('MULTIPOINT'):
                                split = 12
                            elif temp_str.startswith('POINT'):
                                split = 7
                            
                            if split != 0:
                                temp_str = temp_str[split:-1]
                                temp_lst = temp_str.split(', ')
                                for i in range(len(temp_lst)):
                                    temp_lst[i] = (float(temp_lst[i].split(' ')[0]), float(temp_lst[i].split(' ')[1]))
                                
                                ##print(self.point_stor)
                                ##print(temp_lst)

                                if len(temp_lst) > 0:
                                    print('intersect another')
                                    self.length = False
                                    self.break_case = True
                                    return
            else:
                ##print('Bad LEngth')
                self.length = False
                
        #self.is_drawing = False
        ##print(self.length)

    def stop_drawing(self, event):
        global curve_dist, dist
        self.canvas.delete(self.line_id)
        print(self.length)

        if self.length == True:
            good_end = False

            # end_dist = [dist(end_point, (event.x, event.y)) for end_point in self.point_stor]
            # endpoint = self.point_stor[end_dist.index(min(end_dist))]

            if dist((event.x, event.y), self.min_buff) <= self.detection * 1.7:
                good_end = True
                end = self.min_buff

                start = self.junk_stor[-1][0]
                dist_check = copy.deepcopy(self.junk_stor[-1])
                temp_stop = False
                i, j = 0, -1
                while temp_stop == False:
                    if dist(dist_check[-1], end) < self.detection:
                        del dist_check[-1]
                    else:
                        temp_stop = True
                
                temp_stop = False
                while temp_stop == False:
                    if dist(dist_check[0], start) < self.detection:
                        del dist_check[0]
                    else:
                        temp_stop = True

                for point in self.point_stor:
                    for coord in dist_check:
                        if dist(point, coord) <= self.detection:
                            #print('Too Close to Defined Point')
                            good_end = False
                            break
           
            if good_end == True:
                #print('drawing')
                x, y = end
                abs_mouse(self, x, y)
                self.junk_stor[-1].append(end)

                if self.junk_stor[-1][0] == self.junk_stor[-1][1]:
                    del self.junk_stor[-1][1]  
                if self.junk_stor[-1][-1] == self.junk_stor[-1][-2]:
                    del self.junk_stor[-1][-2]

                mod_junk = []
                mod_junk.append(self.junk_stor[-1][0])
                
                rf = round(len(self.junk_stor[-1])/25)

                for i in range(math.floor(len(self.junk_stor[-1][1:-1])/rf)):
                    if self.junk_stor[-1][i] != end:
                        mod_junk.append(self.junk_stor[-1][rf*i])
                        
                mod_junk.append(end)

                #print('junk', mod_junk[0], mod_junk[-1])
                if mod_junk[0] == mod_junk[-1]:
                    smoothed_geometry = catmull_rom_smooth(mod_junk)
                else:
                    smoothed_geometry = chaikin_smooth(mod_junk, keep_ends = True)
                if smoothed_geometry[0] == smoothed_geometry[1]:
                    del smoothed_geometry[1]
                if smoothed_geometry[-1] == smoothed_geometry[-2]:
                    del smoothed_geometry[-2]
               
                ##print(smoothed_geometry)

                self.main_stor.append(smoothed_geometry)
                ##print(self.point_stor)
                self.junk_degrees.append(0)

                self.point_stor.append(self.main_stor[self.play - 1][round(len(self.main_stor[self.play - 1])/2)])
                if self.play >= 1:  
                    #print('degt', self.point_stor)
                    for i in range(len(self.junk_degrees)):
                        self.junk_degrees[i] = 0  
                    
                    for line in self.main_stor:
                        ##print(line)
                        for i in range(len(self.point_stor)):
                            #print('testpoint', self.point_stor[i])
                            if self.point_stor[i] in line:
                                if line[0] == line[-1] and self.point_stor[i] == line[0]:
                                    self.junk_degrees[i] += 2
                                elif self.point_stor[i] == line[0] or self.point_stor[i] == line[-1]:
                                    self.junk_degrees[i] += 1
                                elif line.index(self.point_stor[i]) == round(len(line)/2):
                                    #print('of')
                                    self.junk_degrees[i] += 2
                    
                    #print('close', self.junk_degrees)
                    #print('close', self.degrees)
                    if max(self.junk_degrees) <= 3:
                        self.degrees = copy.deepcopy(self.junk_degrees)
                    else:
                        del self.junk_degrees[-1]
                        del self.main_stor[-1]
                        del self.point_stor[-1]
                        self.play = self.play - 1
                        #print('bad ')
                        return                    
                    #print(self.junk_degrees)
                self.line_stor.append(self.canvas.create_line(self.main_stor[self.play - 1][0][0], self.main_stor[self.play - 1][0][1], self.main_stor[self.play - 1][0][0], self.main_stor[self.play - 1][0][1], width = 1.5))               
                for point in self.main_stor[self.play - 1]:
                    self.canvas.coords(self.line_stor[self.play - 1], self.canvas.coords(self.line_stor[self.play - 1]) + [point[0], point[1]])
                x, y = self.point_stor[-1][0], self.point_stor[-1][1]
                self.disp_point_stor.append((self.canvas.create_oval(x - self.detection/2, y - self.detection/2, x + self.detection/2, y + self.detection/2, fill = 'red')))
               
                if len(self.main_stor) > 0:
                    draw_bound(self)

            else:
                if self.good_start == True:
                    #print('deletion 1')
                    self.play = self.play - 1
        else:
            if self.good_start == True:
                #print('deletion 2')
                self.play = self.play - 1

        #print(self.play, len(self.line_stor), len(self.main_stor))
        redraw_p(self)

    def point_view(self, event):
        if self.point_toggle == False:
            for view in self.disp_point_stor:
                self.canvas.itemconfig(view, state = 'hidden')
            self.point_toggle = True
        else:
            for view in self.disp_point_stor:
                self.canvas.itemconfig(view, state= 'normal')
            self.point_toggle = False
    
    def text_view(self, event):
        if self.text_toggle == False:
            for view in self.disp_text_stor:
                self.canvas.itemconfig(view, state = 'hidden')
            self.text_toggle = True
        else:
            for view in self.disp_text_stor:
                self.canvas.itemconfig(view, state= 'normal')
            self.text_toggle = False
    
    def image_grab(self, event):
        print(self.degrees)
        self.image_points = []
        self.spec_image_points = []
        for i in range(len(self.point_stor)):
            if self.degrees[i] <= 2:
                self.image_points.append(self.point_stor[i])
                if self.degrees[i] <= 1:
                    self.spec_image_points.append((self.point_stor[i][0] - self.left_x, self.point_stor[i][1] - self.top_y))


        if self.play >= 0:
            image_x= root.winfo_rootx() + self.left_x
            image_y=root.winfo_rooty() + self.top_y
            x1= root.winfo_rootx() + self.right_x
            y1= root.winfo_rooty() + self.bottom_y
            ImageGrab.grab().crop((image_x,image_y,x1,y1)).save(r"C:\Users\zm03701\Desktop\600x600 Sprouts\sprouts_img.png")

            field = ['Deg Points', 'Deg 1', 'All Points']
            final_image_points = []
            all_points = []
            for point in self.image_points:
                final_image_points.append((point[0] - self.left_x, point[1] - self.top_y))
            for point in self.point_stor:
                all_points.append((point[0] - self.left_x, point[1] - self.top_y))
            print(final_image_points)
            with open(r'C:\Users\zm03701\Desktop\600x600 Sprouts\sprouts_points.csv', 'a') as f_object:
                writer_object = writer(f_object)
            
                writer_object.writerow([str(final_image_points), str(self.spec_image_points), str(all_points)])
                f_object.close()
                
root = tk.Tk()
app = smooth_fix(root)
root.mainloop()
