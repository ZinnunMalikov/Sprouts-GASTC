import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from shapely import *
from shapelysmooth import *
import customtkinter as ctk
from tkscrolledframe import ScrolledFrame
import time
import math
import copy
import pickle
import itertools
from PIL import ImageGrab
from csv import writer
import numpy as np
import ctypes
import opening_module
import saving_module
import warnings
import ctypes
import sys
from threading import Thread
sys.path.append(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Path-Finding Notebooks")
rework_path = __import__("rework_path")
sprouts_regions = __import__("sprouts_regions")
sprouts_planarity = __import__("sprouts_planarity")
sprouts_path = __import__("sprouts_path_finder")
scroll = __import__("ScrollableNotebook")
from PIL import Image, ImageOps, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

warnings.filterwarnings("ignore")
ctypes.windll.shcore.SetProcessDpiAwareness(2)

class smooth_fix:
    global curve_dist, dist, abs_mouse, redraw_p

    def __init__(self, root):
        self.root = root
        self.root.title('Game of Sprouts' + ' - unsaved graph')
        self.bound = 800
        self.root.geometry('%dx%d+%d+%d' % (self.bound, self.bound, 200, 100))
        self.canvas = tk.Canvas(self.root, width = self.bound, height = self.bound, relief = 'sunken')
        self.analysis_window = 0
        self.path_canvas = 0
        self.saved = False
        self.ret_save = 0
        
        self.root.resizable(False, False)
        self.canvas.pack()
        self.canvas.focus_set()
        self.img = tk.PhotoImage(file = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\SproutsLogo.png")          
        root.img = self.img
        root.iconphoto(True, self.img)

        menubar = tk.Menu(self.root)

        self.file = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='File', menu = self.file)
        self.file.add_command(label ='New File', command = self.reset_graph, compound= 'right')
        self.file.add_command(label ='Open', command = self.open_graph,  compound= 'right')
        self.file.add_command(label ='Save', command = self.save_graph, compound='right')
        self.file.add_separator()
        self.file.add_command(label ='Exit', command = root.destroy)

        path_a = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Path Analysis', menu = path_a)
        path_a.add_command(label ='Open Analysis', command = self.open_path_analysis, compound= 'right')
        
        
        help_ = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Help', menu = help_)
        help_.add_command(label ='Tk Help', command = None)
        help_.add_command(label ='Demo', command = None)
        help_.add_separator()
        help_.add_command(label ='About Tk', command = None)


        self.root.config(menu = menubar)


        self.canvas.bind('<ButtonPress-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<Motion>', self.cursor)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        self.canvas.bind('<Control-p>', self.point_view)
        self.canvas.bind('<Control-t>', self.text_view)
        self.canvas.bind('<Control-i>', self.image_grab)
        self.canvas.bind('<Control-s>', self.save_graph)
        self.canvas.bind('<Control-o>', self.open_graph)
        self.canvas.bind("<Control-r>", self.reset_graph)

        self.is_drawing = False
        self.good_start = False
        self.line_id = None
        self.length = False
        self.main_stor = []
        self.line_stor = []
        self.freq = 1
        
        self.play = 0
        self.detection = 15
        self.inst = False
        self.temp_circle = 0
        self.buffer = 0
        self.min_buffer = 0
        self.break_case = False
        self.int_another_repeat = 0
        self.int_self_repeat = 0

        self.num_points = 3

        self.point_stor = [((self.bound/2) + (100*self.bound/500)*np.cos(pim * 2*np.pi/self.num_points), (self.bound/2) + (100*self.bound/500)*np.sin(pim * 2*np.pi/self.num_points)) for pim in range(self.num_points)]
        self.degrees = [0]*len(self.point_stor)
        self.junk_degrees = [0]*len(self.point_stor)
        self.disp_point_stor, self.junk_stor, self.disp_text_stor = [], [], []
        self.temp_deg_stor = []

        self.path_points = []
        self.rec_bound = 0
        self.pos_disp = self.canvas.create_text(5, 5,  font = ('Times', 10), text = str((0, 0)), anchor = 'nw')
        self.play_display = self.canvas.create_text(5, 30,  font = ('Times', 10), text = 'Play: 1', anchor = 'nw')
        self.turn_display = self.canvas.create_text(5, 50,  font = ('Times', 10), text = "Player 1's Turn", anchor = 'nw')
        self.text_toggle = False
        self.point_toggle = False

        self.left_x = min(self.point_stor)[0] - 50
        self.right_x = max(self.point_stor)[0] + 50
        self.top_y = min(self.point_stor)[1] - 50
        self.bottom_y = max(self.point_stor)[1] + 70

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
            self.disp_point_stor.append((self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = 'red')))
            self.disp_text_stor.append(self.canvas.create_text(x - 5, y + 5, font = ('Times', 10), text = str(self.degrees[i]), anchor = 'nw'))

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
            self.disp_point_stor.append((self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = 'red')))
            self.disp_text_stor.append(self.canvas.create_text(x - 5, y + 5, font = ('Times', 10), text = str(self.degrees[i]), anchor = 'nw'))
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

        self.left_x = min(left_x)- 20
        self.right_x = max(right_x)+ 20
        self.top_y = min(top_y)- 20
        self.bottom_y = max(bottom_y)+ 25
        # if self.rec_bound != 0:
        #     print('deleting')
        #     self.canvas.delete(self.rec_bound)
        # self.rec_bound = self.canvas.create_rectangle(self.left_x, self.top_y, self.right_x, self.bottom_y, width = 2)

    def start_drawing(self, event):
        print('yep')
        print('* * * * *')
        print('play: ', self.play + 1)
        print('points: ', self.point_stor)
        print('lines: ', len(self.main_stor))
        print('degrees: ', self.degrees)
        self.canvas.delete(self.play_display)
        self.play_display = self.canvas.create_text(5, 30,  font = ('Times', 10), text = 'Play: ' + str(self.play + 1), anchor = 'nw')
        self.canvas.delete(self.turn_display)
        self.turn_display = self.canvas.create_text(5, 50,  font = ('Times', 10), text = 'Player ' + str(self.play %2 + 1) + "'s Turn", anchor = 'nw')
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
            self.int_another_repeat, self.int_self_repeat = 0, 0
            x, y = start
            abs_mouse(self, x, y)
            self.is_drawing = True
            self.break_case = False
            self.junk_stor.append([start])
            self.play += 1
            self.line_id = self.canvas.create_line(x, y, x, y)
        else:
            print('Bad Start')
   
    def cursor(self, event):
        self.canvas.delete(self.pos_disp)
        self.pos_disp = self.canvas.create_text(5, 5,  font = ('Times', 10), text = str((event.x, event.y)), anchor = 'nw')
        self.canvas.update()

        if self.inst == False:
            self.buffer = [dist(point, (event.x, event.y)) for point in self.point_stor]
            self.min_buff = self.point_stor[self.buffer.index(min(self.buffer))]
            self.temp_circ = self.canvas.create_oval(self.min_buff[0]- self.detection, self.min_buff[1]- self.detection, self.min_buff[0]+ self.detection, self.min_buff[1]+ self.detection, outline = 'blue')
            self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
            self.inst = True
        
        if self.inst == True:
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
            self.temp_circ = self.canvas.create_oval(self.min_buff[0] - self.detection, self.min_buff[1]- self.detection, self.min_buff[0]+ self.detection, self.min_buff[1]+ self.detection, outline = 'blue')
            self.canvas.itemconfigure(self.temp_circ, state = tk.HIDDEN)
            self.inst = True
        
        if self.inst == True:
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
            self.freq += 1
            if event.x >= self.bound - 20:
                abs_mouse(self, self.bound - 20, event.y)
            if event.y >= self.bound - 20:
                abs_mouse(self, event.x, self.bound - 20)
            if self.junk_stor[-1][-1]!= (event.x, event.y) and self.freq % 5 == 0:
                self.canvas.coords(self.line_id, self.canvas.coords(self.line_id) + [event.x, event.y])
                self.junk_stor[-1].append((event.x, event.y))
                

            if curve_dist(self.junk_stor[-1]) > 2*self.detection:
                if self.break_case != True:
                    self.length = True
                if self.freq % 2 == 0:
                    line = LineString(self.junk_stor[-1])
                    if not line.is_simple:
                        if self.int_self_repeat == 0:
                            print('self-intersect')
                            self.int_self_repeat = 1
                        self.length = False
                        self.break_case = True
                        return
                    else:
                        pass
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

                                if len(temp_lst) > 0:
                                    if self.int_another_repeat == 0:
                                        print('intersect another')
                                        self.int_another_repeat = 1
                                    self.length = False
                                    self.break_case = True
                                    return
            else:
                self.length = False

    def stop_drawing(self, event):
        global curve_dist, dist
        self.canvas.delete(self.line_id)
        print(self.length)

        if self.length == True:
            good_end = False

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
                            good_end = False
                            break
           
            if good_end == True:
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

                if mod_junk[0] == mod_junk[-1]:
                    smoothed_geometry = catmull_rom_smooth(mod_junk)
                else:
                    smoothed_geometry = chaikin_smooth(mod_junk, keep_ends = True)
                if smoothed_geometry[0] == smoothed_geometry[1]:
                    del smoothed_geometry[1]
                if smoothed_geometry[-1] == smoothed_geometry[-2]:
                    del smoothed_geometry[-2]

                midpoint = smoothed_geometry[round(len(smoothed_geometry)/2)]
                seg1 = smoothed_geometry[:smoothed_geometry.index(midpoint) + 1]
                seg2 = smoothed_geometry[smoothed_geometry.index(midpoint):]
                self.main_stor.append(seg1)
                self.main_stor.append(seg2)

                self.junk_degrees.append(0)

                self.point_stor.append(midpoint)
                if self.play >= 1:  
                    for i in range(len(self.junk_degrees)):
                        self.junk_degrees[i] = 0  
                    
                    for line in self.main_stor:
                        for i in range(len(self.point_stor)):
                            if self.point_stor[i] in line:
                                if line[0] == line[-1] and self.point_stor[i] == line[0]:
                                    self.junk_degrees[i] += 2
                                elif self.point_stor[i] == line[0] or self.point_stor[i] == line[-1]:
                                    self.junk_degrees[i] += 1
                                elif line.index(self.point_stor[i]) == round(len(line)/2):
                                    self.junk_degrees[i] += 2
                    
                    if max(self.junk_degrees) <= 3:
                        self.degrees = copy.deepcopy(self.junk_degrees)
                    else:
                        del self.junk_degrees[-1]
                        del self.main_stor[-2:]
                        del self.point_stor[-1]
                        self.play = self.play - 1
                        return      

                for i in range(-2, 0):                
                    self.line_stor.append(self.canvas.create_line(self.main_stor[i][0][0], self.main_stor[i][0][1], self.main_stor[i][0][0], self.main_stor[i][0][1], width = 3))               
                    for point in self.main_stor[i]:
                        self.canvas.coords(self.line_stor[-1], self.canvas.coords(self.line_stor[-1]) + [point[0], point[1]])
                    
                x, y = self.point_stor[-1][0], self.point_stor[-1][1]
                self.disp_point_stor.append((self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = 'red')))
               
                if len(self.main_stor) > 0:
                    self.draw_bound()
                
                self.canvas.delete(self.play_display)
                self.play_display = self.canvas.create_text(5, 30,  font = ('Times', 10), text = 'Play: ' + str(self.play + 1), anchor = 'nw')
                self.canvas.delete(self.turn_display)
                self.turn_display = self.canvas.create_text(5, 50,  font = ('Times', 10), text = 'Player ' + str(self.play %2 + 1) + "'s Turn", anchor = 'nw')

            else:
                if self.good_start == True:
                    self.play = self.play - 1
        else:
            if self.good_start == True:
                self.play = self.play - 1

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
    
    def image_grab(self, event, location):
        print('image')
        self.draw_bound()
        #print(self.degrees)
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

            print(self.left_x, self.top_y, self.right_x, self.bottom_y)
            grImg = ImageGrab.grab().crop((image_x, image_y, x1, y1))
            expgrIMG = ImageOps.expand(grImg,border=100,fill= (240, 240, 240))
            expgrIMG.save(location)




            field = ['Deg Points', 'Deg 1', 'All Points']
            final_image_points = []
            all_points = []
            for point in self.image_points:
                final_image_points.append((point[0] - self.left_x, point[1] - self.top_y))
            for point in self.point_stor:
                all_points.append((point[0] - self.left_x, point[1] - self.top_y))
            print(final_image_points)
            with open(r'C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Data\sprouts_points.csv', 'a') as f_object:
                writer_object = writer(f_object)
            
                writer_object.writerow([str(final_image_points), str(self.spec_image_points), str(all_points)])
                f_object.close()

    def save_graph(self, *event):
        # #play, self.main_stor, self.point_stor, self.degrees
        # print('* * * * * Saving * * * * ')
        # print(self.play + 1)
        # print(self.main_stor)
        # print(self.point_stor)
        # print(self.degrees)
        if len(self.main_stor) >= 0:
            self.draw_bound()
            self.ret_save = saving_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y)
            print('Saved as Graph ' + str(self.ret_save))
            self.root.title('Game of Sprouts' + ' - Graph ' + str(self.ret_save))
            # image_x= root.winfo_rootx() + self.left_x
            # image_y=root.winfo_rooty() + self.top_y
            # x1= root.winfo_rootx() + self.right_x
            # y1= root.winfo_rooty() + self.bottom_y

            # #print(image_x, image_y, x1, y1)
            # ImageGrab.grab().crop((image_x, image_y, x1, y1)).save(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\Graph " + str(self.ret_save) + r"\Graph.png")
            self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\Graph " + str(self.ret_save) + r"\Graph.png")
            self.point_view(event)
            self.text_view(event)
            self.canvas.update()
            self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\Graph " + str(self.ret_save) + r"\Plain.png")
            self.point_view(event)
            self.text_view(event)
            self.canvas.update()

            self.saved = True
            # self.point_view(event)
            # self.text_view(event)
            
            r, g, b = 0,0,0
            save_label = self.canvas.create_text(5, 70, font = ('Times', 10), text = 'Saved as Graph ' + str(self.ret_save), fill = f'#{r:02x}{g:02x}{b:02x}', anchor = 'nw')
            for i in range(240):
                r += 1
                g += 1
                b +=1  
                self.canvas.itemconfig(save_label, fill = f'#{r:02x}{g:02x}{b:02x}')
                self.canvas.update()
                time.sleep(0.005)
        else:
            messagebox.showerror('Saving Error', 'Error: Cannot save empty graph!')

    def reset_graph(self, *event):
        try:
            temp_np = tk.simpledialog.askinteger(title='New Graph', prompt = 'Number of Starting Points', minvalue = 1, maxvalue = 10)
            temp_np = int(temp_np)
        except:
            return
        else:
            self.num_points = temp_np
        self.root.title('Game of Sprouts - unsaved graph')
        self.canvas.delete('all')
        self.is_drawing = False
        self.good_start = False
        self.line_id = None
        self.length = False
        self.main_stor = []
        self.line_stor = []
        self.freq = 1

        self.saved = False
        
        self.play = 0
        self.inst = False
        self.temp_circle = 0
        self.buffer = 0
        self.min_buffer = 0
        self.break_case = False
        self.int_another_repeat = 0
        self.int_self_repeat = 0

        self.point_stor = [((self.bound/2) + (100*self.bound/500)*np.cos(pim * 2*np.pi/self.num_points), (self.bound/2) + (100*self.bound/500)*np.sin(pim * 2*np.pi/self.num_points)) for pim in range(self.num_points)]
        self.degrees = [0]*len(self.point_stor)
        self.junk_degrees = [0]*len(self.point_stor)
        self.disp_point_stor, self.junk_stor, self.disp_text_stor = [], [], []
        self.temp_deg_stor = []

        self.path_points = []
        self.rec_bound = 0
        self.pos_disp = self.canvas.create_text(5, 5,  font = ('Times', 10), text = str((0, 0)), anchor = 'nw')
        self.play_display = self.canvas.create_text(5, 30,  font = ('Times', 10), text = 'Play: 1', anchor = 'nw')
        self.turn_display = self.canvas.create_text(5, 50,  font = ('Times', 10), text = "Player 1's Turn", anchor = 'nw')
        self.text_toggle = False
        self.point_toggle = False

        self.left_x = min(self.point_stor)[0] - 5
        self.right_x = max(self.point_stor)[0] + 5
        self.top_y = min(self.point_stor)[1] - 5
        self.bottom_y = max(self.point_stor)[1] + 5

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

        self.left_x = min(left_x) - 5
        self.right_x = max(right_x) + 5
        self.top_y = min(top_y) - 5
        self.bottom_y = max(bottom_y) + 5
        
        self.spec_image_points = []

        self.image_points = self.point_stor

        for i, point in enumerate(self.point_stor):
            x, y = point[0], point[1]
            self.disp_point_stor.append((self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = 'red')))
            self.disp_text_stor.append(self.canvas.create_text(x - 5, y + 5, font = ('Times', 10), text = str(self.degrees[i]), anchor = 'nw'))


    def open_graph(self, *event):
        graph_path = askdirectory(title='Select Folder', initialdir = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs")
        self.canvas.delete('all')
        self.is_drawing = False
        self.good_start = False
        self.line_id = None
        self.length = False
        self.main_stor = []
        self.line_stor = []
        self.freq = 1

        self.saved = True
        
        self.play = 0
        self.inst = False
        self.temp_circle = 0
        self.buffer = 0
        self.min_buffer = 0
        self.break_case = False
        self.int_another_repeat = 0
        self.int_self_repeat = 0

        self.point_stor = [((self.bound/2) + (100*self.bound/500)*np.cos(pim * 2*np.pi/self.num_points), (self.bound/2) + (100*self.bound/500)*np.sin(pim * 2*np.pi/self.num_points)) for pim in range(self.num_points)]
        self.degrees = [0]*len(self.point_stor)
        self.junk_degrees = [0]*len(self.point_stor)
        self.disp_point_stor, self.junk_stor, self.disp_text_stor = [], [], []
        self.temp_deg_stor = []

        self.path_points = []
        self.rec_bound = 0
        self.pos_disp = self.canvas.create_text(5, 5,  font = ('Times', 10), text = str((0, 0)), anchor = 'nw')
        self.play_display = self.canvas.create_text(5, 30,  font = ('Times', 10), text = 'Play: 1', anchor = 'nw')
        self.turn_display = self.canvas.create_text(5, 50,  font = ('Times', 10), text = "Player 1's Turn", anchor = 'nw')
        self.text_toggle = False
        self.point_toggle = False

        self.left_x = min(self.point_stor)[0] - 5
        self.right_x = max(self.point_stor)[0] + 5
        self.top_y = min(self.point_stor)[1] - 5
        self.bottom_y = max(self.point_stor)[1] + 5

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

        self.left_x = min(left_x) - 5
        self.right_x = max(right_x) + 5
        self.top_y = min(top_y) - 5
        self.bottom_y = max(bottom_y) + 5
        
        self.spec_image_points = []

        self.image_points = self.point_stor

        for i, point in enumerate(self.point_stor):
            x, y = point[0], point[1]
            self.disp_point_stor.append((self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = 'red')))
            self.disp_text_stor.append(self.canvas.create_text(x - 5, y + 5, font = ('Times', 10), text = str(self.degrees[i]), anchor = 'nw'))

        self.play, self.degrees, self.point_stor, self.main_stor, transforms = opening_module.open_graph(graph_path)
        self.junk_degrees = self.degrees
        for i in range(len(self.main_stor)):
            self.line_stor.append(self.canvas.create_line(self.main_stor[i][0][0], self.main_stor[i][0][1], self.main_stor[i][0][0], self.main_stor[i][0][1], width = 3))               
            for point in self.main_stor[i]:
                self.canvas.coords(self.line_stor[i], self.canvas.coords(self.line_stor[i]) + [point[0], point[1]])
        redraw_p(self)
        self.canvas.delete(self.play_display)
        self.play_display = self.canvas.create_text(5, 30,  font = ('Times', 10), text = 'Play: ' + str(self.play + 1), anchor = 'nw')
        self.canvas.delete(self.turn_display)
        self.turn_display = self.canvas.create_text(5, 50,  font = ('Times', 10), text = 'Player ' + str(self.play %2 + 1) + "'s Turn", anchor = 'nw')
        self.root.title('Game of Sprouts - ' + graph_path.split('/')[-1])
        self.ret_save = int(graph_path.split('/')[-1].split(' ')[-1])

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
        

    def open_path_analysis(self, *event):
        if True: #not self.saved:
            # messagebox.showerror('Path Analysis Error', 'Error: Please save the graph or open a saved graph!')
            self.analysis_window = tk.Toplevel(self.root)
            self.analysis_window.geometry('%dx%d+%d+%d' % (700, 800, 1050, 100))
            self.analysis_window.resizable(False, False)
            self.analysis_window.title('Path Analysis')
            self.path_computed = False
            self.valid_paths, self.throw1, self.throw2 = 0, 0, 0
            

            a_menubar = tk.Menu(self.analysis_window)    
            self.a_file = tk.Menu(a_menubar, tearoff = 0)
            a_menubar.add_cascade(label ='File', menu = self.a_file)
            self.a_file.add_command(label ='New File', command = None, compound= 'right')
            self.a_file.add_command(label ='Open', command = None,  compound= 'right')
            self.a_file.add_command(label ='Save', command = None, compound='right')
            self.a_file.add_separator()
            self.a_file.add_command(label ='Exit', command = root.destroy)

            a_help_ = tk.Menu(a_menubar, tearoff = 0)
            a_menubar.add_cascade(label ='Help', menu = a_help_)
            a_help_.add_command(label ='Tk Help', command = None)
            a_help_.add_command(label ='Demo', command = None)
            a_help_.add_separator()
            a_help_.add_command(label ='About Tk', command = None)

            selec = 8

            self.analysis_window.config(menu = a_menubar)
            fill_image, set_rep, dict_rep, dict_inds = sprouts_regions.main(selec) #self.ret_save)
            rp_stor, rl_stor, names, rdeg, rplay, redg,  = sprouts_planarity.main(selec ) #self.ret_save)

            live_set_rep = []
            for obj in set_rep:
                temp = []
                for point in obj:
                    if rdeg[names.index(point) - 1] < 3:
                        temp.append(point)
                live_set_rep.append(temp)

            self.fig = plt.figure(figsize=(3, 3), facecolor='#F0F0F0')
            # self.fig
            # = plt.figure(figsize=(3, 3), facecolor='#F0F0F0')
            def redraw_colored():
                plt.imshow(fill_image)
                for i, point in enumerate(rp_stor):
                    x, y = point
                    plt.scatter(x , y, marker='o', color="red", edgecolors='black', s = 10, zorder = 5)
                    orientations = [[15, 15], [-15, 15], [-15, -15], [15, -15]]
                    black_fill = []
                    for obj in orientations:
                        black_fill.append(0)
                        for m in range(min(0, obj[0]), max(0, obj[0])):
                            for n in range(min(0, obj[1]), max(0, obj[1])):
                                if fill_image.getpixel((x + m, y + n))[0:3] == (0, 0, 0):
                                    black_fill[-1] += 1
                    best_orient = orientations[black_fill.index(min(black_fill))]
                    plt.annotate(names[i + 1], (x + 1.3*best_orient[0], y + 1.3*best_orient[1]), ha = 'center', va = 'center')
            redraw_colored()

            canvas = FigureCanvasTkAgg(self.fig, master = self.analysis_window)   
            canvas.draw() 

            toolbar = NavigationToolbar2Tk(canvas, self.analysis_window) 
            toolbar.update() 
          
            canvas.get_tk_widget().pack()
            toolbar.pack(side='top')

            # Create the notebook with scrollbar
            outer_note = ttk.Notebook(self.analysis_window)
            outer_note.enable_traversal()
            # scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

            # Create and add tabs to the notebook
            oframes = []
            oframe = tk.Frame(outer_note)
            oframes.append(oframe)
            outer_note.add(oframe, text="Properties")

            oframe = tk.Frame(outer_note)
            oframes.append(oframe)
            outer_note.add(oframe, text="Path Analysis")

            prop_note = scroll.ScrollableNotebook(oframes[0], wheelscroll=True,tabmenu=True)
            prop_top = tk.Frame(prop_note)
            prop_top.pack(side="top", expand=1, fill="both")

            path_note = scroll.ScrollableNotebook(oframes[1], wheelscroll=True,tabmenu=True)
            path_top = tk.Frame(prop_note)
            path_top.pack(side="top", expand=1, fill="both")

            sf = ScrolledFrame(prop_top)#, width=380, height=240)
            gp_frame = sf.display_widget(tk.Frame)
            sf.pack(side="top", expand=1, fill="both")

            sf.bind_arrow_keys(prop_top)
            sf.bind_scroll_wheel(prop_top)

            prop_note.add(prop_top, text = "General")

            #General Properties
            vert_L = tk.Label(gp_frame, text="Vertices: " + str(names[1: len(rp_stor) + 1]), wraplength=604, anchor='w', justify="left")
            edge_L = tk.Label(gp_frame, text="Edges: " + str(redg), wraplength=604, anchor='w', justify="left")
            cvert_L = tk.Label(gp_frame, text="Vertex Count: " + str(len(rp_stor)), wraplength=604, anchor='w', justify="left")
            cedge_L = tk.Label(gp_frame, text="Edge Count: " + str(len(redg)), wraplength=604, anchor='w', justify="left") 
            face_L = tk.Label(gp_frame, text="Region Count: " + str(len(dict_rep)), wraplength=604, anchor='w', justify="left")
            comp_L = tk.Label(gp_frame, text="Component Count: " +  str(len(rp_stor)-len(redg)+len(dict_rep) - 1), wraplength=604, anchor='w', justify="left")
            deg_L = tk.Label(gp_frame, text="Degrees: " + str(rdeg), wraplength=604, anchor='w', justify="left")
            set_L = tk.Label(gp_frame, text="Set Representation: " + str(set_rep), wraplength=604, anchor='w', justify="left")
            dict_L = tk.Label(gp_frame, text="Dictionary: " + str(dict_rep))

            # empty_L = tk.Label(gp_frame, text="")
            
            vert_L.grid(row = 1, column = 0, sticky="W", pady=2)
            deg_L.grid(row = 2, column = 0, sticky="W", pady=2)
            edge_L.grid(row = 3, column = 0, sticky="W", pady=2)
            cvert_L.grid(row = 4, column = 0, sticky="W", pady=2)
            cedge_L.grid(row = 5, column = 0, sticky="W", pady=2)
            face_L.grid(row = 6, column = 0, sticky="W", pady=2)
            comp_L.grid(row = 7, column = 0, sticky="W", pady=2)
            set_L.grid(row = 8, column = 0, sticky="W", pady=2)
            # gp_frame

            for i in range(len(set_rep)):
                inner_top = tk.Frame(prop_note)
                inner_top.pack(side="top", expand=1, fill="both")

                inf = ScrolledFrame(inner_top, width=380, height=240)
                iframe = inf.display_widget(tk.Frame)
                inf.pack(side="top", expand=1, fill="both")

                inf.bind_arrow_keys(inner_top)
                inf.bind_scroll_wheel(inner_top)

                bound_L = tk.Label(iframe, text="Boundary Points: " + str(set_rep[i]), wraplength=604, anchor='w', justify="left")
                bound_L.grid(row = 0, column = 0, sticky = "W", pady = 2)
                if len(dict_rep[i]['inner']) > 0:
                    reg_inner_L = tk.Label(iframe, text="Inner Boundary: " + str(dict_rep[i]['inner']), wraplength=604, anchor='w', justify="left")
                    reg_inner_L.grid(row = 3, column = 0, sticky = "W", pady = 2)
                if len(dict_rep[i]['boundary']) > 0:
                    out_inner_L = tk.Label(iframe, text="Outer Boundary: " + str(dict_rep[i]['boundary']), wraplength=604, anchor='w', justify="left")
                    out_inner_L.grid(row = 4, column = 0, sticky = "W", pady = 2)
                
                
                prop_note.add(inner_top, text=f"Region {i+1}")

                alive = []
                dead = []
                
                for point in set_rep[i]:
                    if rdeg[names.index(point) - 1] < 3:
                        alive.append(point)
                    else:
                        dead.append(point)
                
                associations = []
                current_live = list(set(live_set_rep[i]))
                for x in range(len(live_set_rep)):
                    if not x == i:
                        
                        another_live = list(set(live_set_rep[x]))
                        check_live = list(set(current_live + another_live)) 
                        if len(current_live) + len(another_live) - len(check_live) >= 2:
                            associations.append("Region " + str(x + 1))
                

                alive_L = tk.Label(iframe, text="Live Points: " + str(alive))
                dead_L = tk.Label(iframe, text="Dead Points: " + str(dead))
                interact_L = tk.Label(iframe, text="Possible Interactions: " + str(associations), wraplength=604, anchor='w', justify="left")
                alive_L.grid(row = 1, column = 0, sticky = "W", pady = 2)
                dead_L.grid(row = 2, column = 0, sticky = "W", pady = 2)
                interact_L.grid(row = 5, column = 0, sticky = "W", pady = 2)

            
            # print(dict_rep)

            def prop_tab_change(event):
                plt.clf()
                redraw_colored()
                if str(event.widget.tab('current')['text']) != 'General':
                    tab = int(str(event.widget.tab('current')['text']).split(' ')[-1]) - 1
                    # print(tab)

                    if len(dict_inds[tab]['inner']) > 0:
                        for path in dict_inds[tab]['inner']:
                            # print(path)
                            for ind in path:
                                x_val = [x[0] for x in rl_stor[ind]]
                                y_val = [x[1] for x in rl_stor[ind]]
                                plt.plot(x_val, y_val, color = 'red', linewidth = 2, zorder = 2)
                    
                    if len(dict_inds[tab]['boundary']) > 0:
                        for ind in dict_inds[tab]['boundary']:
                                x_val = [x[0] for x in rl_stor[ind]]
                                y_val = [x[1] for x in rl_stor[ind]]
                                plt.plot(x_val, y_val, color = 'red', linewidth = 2, zorder = 2)
                    
                    # print(set_rep[tab])
                    for point in set_rep[tab]:
                        x, y = rp_stor[names.index(point) - 1]
                        if rdeg[names.index(point) - 1] < 3:
                            plt.scatter(x , y, marker='o', color="lime", edgecolors='black', s = 20, zorder = 6)
                        else:
                            plt.scatter(x , y, marker='o', color="grey", edgecolors='black', s = 20, zorder = 6)

                    # plt.scatter(20 + 20 * tab, 20 * tab)
                    canvas.draw()
                else:
                    redraw_colored()
                    canvas.draw()

            def outer_tab_change(event):
                print('changed')
                if str(event.widget.tab('current')['text']) == 'Path Analysis':
                    if  not self.path_computed:
                        print("OMG START")
                        self.path_computed = True
                        self.valid_paths, self.throw1, self.throw2 = sprouts_path.main(selec)
                        print('ok all done')
                        plt.figure(self.fig.number)

                        # print(plt.gcf())
                        # print("OMG START")
                        # self.path_computed = True
                        # bar_area = tk.Toplevel()
                        # bar_area.title("Computing Paths")
                        # bar_area.geometry('%dx%d+%d+%d' % (400, 50, 1150, 400))
                        # progress = ttk.Progressbar(bar_area, mode = 'indeterminate', length=250)
                        # progress.pack()
                        # progress.start()
                        # self.analysis_window.update()
 
                        # def task():
                        #     self.valid_paths, self.throw1, self.throw2 = sprouts_path.main(selec)
                        # #thread = Thread(target=sprouts_path.main, args=(selec,))
                        # thread = Thread(target=task)
                        # thread.setDaemon(True)
                        # thread.start()
                        # while self.valid_paths == 0:
                        #     self.analysis_window.update()
                        #     continue
                        # thread.join()
                        # progress.stop()
                        # progress.destroy()
                        # bar_area.destroy()
                        # plt.figure(self.fig.number)
                        # print(plt.gcf())
                        # redraw_colored()
                        # canvas.draw()
                        
                        # thread.join()

                        # valid_paths, throw1, throw2 = sprouts_path.main(selec)
                        # for i in range(len(self.valid_paths)):
                        #     ipath_top = tk.Frame(path_note)
                        #     ipath_top.pack(side="top", expand=1, fill="both")

                        #     ipf = ScrolledFrame(inner_top, width=380, height=240)
                        #     ipframe = ipf.display_widget(tk.Frame)
                        #     ipf.pack(side="top", expand=1, fill="both")

                        #     ipf.bind_arrow_keys(inner_top)
                        #     ipf.bind_scroll_wheel(inner_top)

                        #     bound_L = tk.Label(ipframe, text="Boundary Points: " + str(set_rep[i]), wraplength=604, anchor='w', justify="left")
                        #     bound_L.grid(row = 0, column = 0, sticky = "W", pady = 2)
                            
                            
                        #     path_note.add(ipath_top, text=f"Path {i+1}")

                        

                    
            
            outer_note.bind('<<NotebookTabChanged>>', outer_tab_change)
            prop_note.bind(prop_tab_change)
            











            # Pack the notebook
            prop_note.pack(fill=tk.BOTH, expand = True)
            outer_note.pack(fill=tk.BOTH, expand=True)

            # color_toggle = tk.Button(self.analysis_window)
            # color_toggle.pack(side='top')
    
            

            
root = tk.Tk()
app = smooth_fix(root)
root.mainloop()
