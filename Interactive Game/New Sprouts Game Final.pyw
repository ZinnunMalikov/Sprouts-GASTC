import tkinter as tk
from tkinter import ttk, Misc
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
from PIL import ImageGrab, ImageDraw, ImageFont, ImageTk
from csv import writer
import numpy as np
import ctypes
import opening_module
import saving_module
import computer_module
import warnings
import ctypes
import sys
import os
import mouse
import pandas as pd
from threading import Thread
from tkPDFViewer import tkPDFViewer as pdf 
import pyautogui as pg
sys.path.append(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Path-Finding Notebooks")
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

global open_cond
open_cond = False

class smooth_fix:
    global curve_dist, dist, abs_mouse, redraw_p, open_cond
    print(open_cond)

    def __init__(self, root):
        # initialize self variables
        self.root = root
        self.root.title('Game of Sprouts' + ' - unsaved graph')
        self.bound = 800
        self.root.geometry('%dx%d+%d+%d' % (self.bound, self.bound, 200, 100))
        self.canvas = tk.Canvas(self.root, width = self.bound, height = self.bound, relief = 'sunken')
        self.analysis_window = 0
        self.path_canvas = 0
        self.saved = False
        self.ret_save = 0
        self.comp_path = 0
        self.temp_state = 'placehold'
        self.mult_save = False
        self.comp_debug = 0
        self.main_about_area = None
        self.main_help_area = None
        self.v2 = None
        self.v4 = None
        self.player_turn = False

        self.root.resizable(False, False)
        self.canvas.pack()
        self.canvas.focus_set()
        self.img = tk.PhotoImage(file = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts New Logo.png")          
        
        root.iconbitmap(True, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts New Logo.ico")

        menubar = tk.Menu(self.root)

        self.file = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='File', menu = self.file)
        self.file.add_command(label ='New File',command = self.reset_graph, compound= 'right')
        self.file.add_command(label ='Open', command = self.open_graph,  compound= 'right')
        self.file.add_command(label ='Save', command = self.save_graph, compound='right')
        
        self.file.add_separator()
        self.file.add_command(label ='Exit', command = root.destroy)

        self.home = tk.Menu(menubar, tearoff= 0)
        menubar.add_cascade(label ='Home', menu = self.home)
        self.home.add_command(label ='Home', command = self.homepage, compound='right')

        path_a = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Graph Analysis', menu = path_a)
        path_a.add_command(label ='Open Analysis', command = self.open_path_analysis, compound= 'right')

        comp = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Computer', menu = comp)
        comp.add_command(label ='Start Computer', command = self.start_computer, compound= 'right')
        comp.add_command(label ='Kill Computer', command = self.end_computer, compound= 'right')
        
        help_ = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Help', menu = help_)
        help_.add_command(label ='Game Rules', command = self.main_help)
        help_.add_separator()
        help_.add_command(label ='About Sprouts', command = self.main_about)


        self.root.config(menu = menubar)
        self.homepage() 
        self.home_window.lift(self.root)


        self.canvas.bind('<ButtonPress-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<Motion>', self.cursor)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        self.canvas.bind('<Control-p>', self.point_view)
        self.canvas.bind('<Control-t>', self.text_view)
        # self.canvas.bind('<Control-i>', self.image_grab)
        self.canvas.bind('<Control-s>', self.save_graph)
        self.canvas.bind('<Control-o>', self.open_graph)
        self.canvas.bind("<Control-r>", self.reset_graph)
        self.canvas.bind("<FocusIn>", self.run_comp)


        self.is_drawing = False
        self.good_start = False
        self.line_id = None
        self.length = False
        self.main_stor = []
        self.line_stor = []
        self.freq = 1
        self.computer = False
        self.computer_play = 0
        self.c_left = 0
        
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
 

    # mouse position
    def abs_mouse(self, x, y):
        self.canvas.event_generate('<Motion>', warp = True, x = x, y= y)

   
    def dist(tupl1, tupl2):
        return ((tupl2[0] - tupl1[0]) ** 2 + (tupl2[1] - tupl1[1]) ** 2) ** 0.5

    def curve_dist(inp):
        curve_dist = 0
        for i in range(len(inp) - 1):
            curve_dist += ((inp[i + 1][0] - inp[i][0]) ** 2 + (inp[i + 1][1] - inp[i][1]) ** 2) ** 0.5
        return curve_dist
   
    # redraw points
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

    def an_info(self, *event):
        an_info_area = tk.Toplevel()
        an_info_area.title("Analysis Information")
        an_info_area.geometry('%dx%d+%d+%d' % (600, 300, 1050, 400))

        v= tk.Scrollbar(an_info_area, orient='vertical')
        v.pack(side='right', fill='y')

        text_widget = tk.Text(an_info_area, height=20, width=300, wrap = 'word', yscrollcommand=v.set)

        v.config(command=text_widget.yview)
        text_widget.pack(padx=20, pady=20)

        # Insert the rule text
        text_widget.insert(tk.END, "Graph Analyis Information\n\n")
        text_widget.insert(tk.END, "This tool provides two distinct features to help you analyze graphs.\n\n")
        text_widget.insert(tk.END, "+ Graph Properties and Region Analysis\n")
        text_widget.insert(tk.END, "  - View properties of graphs (connectedness, components, etc.)\n") 
        text_widget.insert(tk.END, "  - See details of each region formed by the graph\n\n")
        text_widget.insert(tk.END, "+ Path Analysis \n")
        text_widget.insert(tk.END, "  - See information about all possible paths in the current state.\n\n")
        text_widget.config(state='disabled')
    
    
    
    def main_help(self, *event):
        if self.main_about_area:
            self.main_about_area.destroy()
        if self.main_help_area:
            self.main_help_area.destroy()
        self.main_help_area = tk.Toplevel()
        self.main_help_area.title("Game Rules")
        self.main_help_area.geometry('%dx%d+%d+%d' % (600, 800, 1000, 120))

        # if self.v2:
        #     self.v2.destroy()

        self.v1 = pdf.ShowPdf() 
        self.v1.img_object_li.clear()
  
        # Adding pdf location and width and height. 
        self.v2 = self.v1.pdf_view(self.main_help_area, pdf_location = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts Rules.pdf",
                         width = 85, height = 110) 
        
        # Placing Pdf in my gui. 
        self.v2.pack() 

        # v= tk.Scrollbar(self.main_help_area, orient='vertical')
        # v.pack(side='right', fill='y')

        # text_widget = tk.Text(self.main_help_area, height=20, width=300, wrap = 'word', yscrollcommand=v.set)

        # v.config(command=text_widget.yview)
        # text_widget.pack(padx=20, pady=20)

        # # Insert the rule text
        # text_widget.insert(tk.END, "Sprouts Game Rules\n\n")
        # text_widget.insert(tk.END, "Sprouts is played by two players, starting with a few spots drawn on a plane. Players take turns, where each turn consists of drawing a line between two spots (or from a spot to itself) and adding a new spot somewhere along the line.\n\n")
        # text_widget.insert(tk.END, "Rules:\n\n")
        # text_widget.insert(tk.END, "  - The line may be straight or curved, but must not touch or cross itself or any other line.\n\n")
        # text_widget.insert(tk.END, "  - The new spot cannot be placed on top of one of the endpoints of the new line. Thus the new spot splits the line into two shorter lines.\n\n")
        # text_widget.insert(tk.END, "  - No spot may have more than three lines attached to it. For the purposes of this rule, a line from the spot to itself counts as two attached lines and new spots are counted as having two lines already attached to them.\n\n")
        # text_widget.insert(tk.END, "  - You cannot touch a dot twice with one line then connect it to another.\n\n")
        # text_widget.insert(tk.END, "In normal play, the player who makes the last move wins.\n")
        # text_widget.config(state='disabled')

    def main_about(self, *event):
        if self.main_about_area:
            self.main_about_area.destroy()
        if self.main_help_area:
            self.main_help_area.destroy()
        self.main_about_area = tk.Toplevel()
        self.main_about_area.title("About Sprouts")
        self.main_about_area.geometry('%dx%d+%d+%d' % (600, 800, 1000, 120))

        # if self.v4:
        #     print('up')
        #     self.v4.destroy()
        self.v3 = pdf.ShowPdf() 
        self.v3.img_object_li.clear()
        
        # Adding pdf location and width and height. 
        self.v4 = self.v3.pdf_view(self.main_about_area, pdf_location = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts Overview.pdf",
                         width = 85, height = 110) 
        
        # Placing Pdf in my gui. 
        self.v4.pack() 
        # self.main_about_area = tk.Toplevel()
        # self.main_about_area.title("About Sprouts")
        # self.main_about_area.geometry('%dx%d+%d+%d' % (700, 500, 150, 400))

        # v= tk.Scrollbar(self.main_about_area, orient='vertical')
        # v.pack(side='right', fill='y')

        # text_widget = tk.Text(self.main_about_area, height=20, width=300, wrap = 'word', yscrollcommand=v.set)

        # v.config(command=text_widget.yview)
        # text_widget.pack(padx=20, pady=20)

        # text_widget.insert(tk.END, "Welcome to Sprouts: Your Combinatorics Playground!\n\n")
        # text_widget.insert(tk.END, "This program combines the engaging game of Sprouts with powerful graph analysis tools, making it perfect for students of combinatorics and graph theory.\n\n")
        # text_widget.insert(tk.END, "Main Window:\n\n")
        # text_widget.insert(tk.END, "Play Sprouts: Play the game of Sprouts against a friend or play against the computer.\n\n")
        # text_widget.insert(tk.END, "+ File Functions:\n")
        # text_widget.insert(tk.END, "    - Save Graph: Save your game for later analysis or continuation.\n")
        # text_widget.insert(tk.END, "    - Open Graph: Load a previously saved game.\n")
        # text_widget.insert(tk.END, "    - New Graph: Clear the current game and start fresh.\n\n")
        # text_widget.insert(tk.END, "+ Graph Analysis:\n\n")
        # text_widget.insert(tk.END, "    - Gain insight into your game's structure with this dedicated feature.\n")
        # text_widget.insert(tk.END, "    - Analyze various graph properties like connectivity, components, and more.\n\n")
        # text_widget.insert(tk.END, "+ Computer Player:\n\n")
        # text_widget.insert(tk.END, "    - Play aganst a computer opponent.\n")

    
    def start_computer(self, *event):
        print('Botting up the op')
        self.computer = True
        self.computer_play = self.play %2 + 1

    def run_comp(self, *event):
        # if self.computer == True:
        # print('cyclic debug')
        # print(self.computer)
        # print(self.comp_debug)
        # print(self.play)
        # print(self.play %2 + 1)
        # print(self.computer_play)
        # print(self.is_drawing)
        if self.computer == True and self.player_turn == True and self.comp_debug == 0 and (self.play %2 + 1) != self.computer_play:
            print('*************')
            print('My turn')
            print('*************')
            # self.draw_bound()
            # computer_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y)

            # self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Computer Junk\Computer Data\Graph.png")
            # self.point_view(event)
            # self.text_view(event)
            # self.canvas.update()
            # self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Computer Junk\Computer Data\Plain.png")
            # self.point_view(event)
            # self.text_view(event)
            # self.canvas.update()

            # print('* * * * * * * *')
            # print('* * * * * * * *')
            # print('* * * * * * * *')
            # if not (sprouts_path.main(0, 2)):
            #     print('hopjit')
            #     self.computer = False
            #     self.comp_debug = 0
            #     time.sleep(0.25)
            #     self.computer = False
            #     messagebox.showerror('No Move', 'Game is finished! \nWinner: ' + 'Computer')  
            #     return
            self.comp_debug = 1
        elif (self.computer == True) and self.player_turn == False and (self.play %2 + 1) == self.computer_play and not self.is_drawing:
            self.comp_debug = 1
            print('*************')
            print('Comp Turn')
            print('*************')
            self.play += 1

            self.draw_bound()
            computer_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y)

            self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Computer Junk\Computer Data\Graph.png")
            self.point_view(event)
            self.text_view(event)
            self.canvas.update()
            self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Computer Junk\Computer Data\Plain.png")
            self.point_view(event)
            self.text_view(event)
            self.canvas.update()

            cbar_area = tk.Toplevel()
            cbar_area.title("Computing Move")
            cbar_area.geometry('%dx%d+%d+%d' % (400, 50, 150, 400))
            cprogress = ttk.Progressbar(cbar_area, mode = 'indeterminate', length=250)
            cprogress.pack()
            cprogress.start()
            cbar_area.update()
            self.comp_path, cf, ci, cc, self.c_left = 0,0,0,0,0
            def ctask():
                self.comp_path, cf, ci, cc, self.c_left = sprouts_path.main(0, 1)

            cthread = Thread(target=ctask)
            cthread.setDaemon(True)
            cthread.start()
            while self.comp_path == 0:
                cbar_area.update()
                continue

            cprogress.stop()
            cprogress.destroy()
            cbar_area.destroy()
            
            # print(list(comp_path.items())[0][-1])
            self.comp_path = list(self.comp_path.items())
            if len(self.comp_path) > 0:  
                cpath_points = []
                cmidpoints = []
                cdata = self.comp_path[0][-1]
                cs_inds = []
                ce_inds = []

                for col, info in cdata.items():
                    cpath_points.append(info['path'])
                    cmidpoints.append(info['midpoint'])
                    cs_inds.append(info['start'])
                    ce_inds.append(info['end'])

                
                cpath_points = cpath_points[0]
                cmidpoints = [cmidpoints[0]]

                # plt.plot(cx_val,cy_val, color = 'black')
                cpath_points[0][0] = self.point_stor[cs_inds[0]]
                cpath_points[1][-1] = self.point_stor[ce_inds[0]]
                
                self.main_stor.append(cpath_points[0])
                self.main_stor.append(cpath_points[1])
                self.point_stor.append(cmidpoints[0])

                self.junk_degrees.append(0)
                print('opop')
                print(self.degrees)

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
                redraw_p(self)
                computer_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y)
                self.canvas.update()

                if self.saved:
                    self.root.title('Game of Sprouts' + ' - Graph ' + str(self.ret_save) + ' - Unsaved Changes')
                    self.saved = False

                print('yolo')
                print(self.c_left)
                time.sleep(0.3)
                self.draw_bound()
                computer_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y)

                self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Computer Junk\Computer Data\Graph.png")
                self.point_view(event)
                self.text_view(event)
                self.canvas.update()
                self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Computer Junk\Computer Data\Plain.png")
                self.point_view(event)
                self.text_view(event)
                self.canvas.update()

                print('* * * * * * * *')
                print('* * * * * * * *')
                print('* * * * * * * *')
                cbar_area2 = tk.Toplevel()
                cbar_area2.title("Checking State")
                cbar_area2.geometry('%dx%d+%d+%d' % (400, 50, 150, 400))
                cprogress2 = ttk.Progressbar(cbar_area2, mode = 'indeterminate', length=250)
                cprogress2.pack()
                cprogress2.start()
                cbar_area2.update()
                self.temp_state = 'placehold'
                def ctask2():
                    self.temp_state = sprouts_path.main(0, 2)

                cthread2 = Thread(target=ctask2)
                cthread2.setDaemon(True)
                cthread2.start()
                while self.temp_state == 'placehold':
                    cbar_area2.update()
                    continue

                cprogress2.stop()
                cprogress2.destroy()
                cbar_area2.destroy()


                if not (self.temp_state):
                    print('hopjit')
                    self.computer = False
                    self.comp_debug = 0
                    time.sleep(0.25)
                    self.computer = False
                    messagebox.showerror('No Move', 'Game is finished! \nWinner: ' + 'Computer')  
                    plt.figure(100)
                    return
                
                self.comp_debug = 0
                plt.figure(100)
                self.player_turn = True
                time.sleep(0.2)
            else:
                print('meepsqueak')
                self.computer = False
                self.comp_debug = 0
                time.sleep(0.25)
                self.computer = False
                messagebox.showerror('No Move', 'Game is finished! \nWinner: ' + 'You')
                plt.figure(100)
                return

        # if self.computer:
        root.after(1000, self.run_comp)

    def end_computer(self, *event):
        self.computer = False
        self.comp_debug = 0
        

    # initialize when user clicks on point
    def start_drawing(self, event):
        self.length = False
        self.canvas.focus_set()
        if not (self.computer and (self.play %2 + 1) == self.computer_play):
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
                
            #Valid length
            if curve_dist(self.junk_stor[-1]) > 1.5*self.detection:
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

            if (((self.point_stor.index(self.junk_stor[-1][0]) == self.point_stor.index(self.min_buff)) and (self.degrees[self.point_stor.index(self.min_buff)] <= 1)) or ((self.point_stor.index(self.junk_stor[-1][0]) != self.point_stor.index(self.min_buff))) and (self.degrees[self.point_stor.index(self.min_buff)] <= 2)) and (dist((event.x, event.y), self.min_buff) <= self.detection * 1.7):
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
                full_length = curve_dist(mod_junk)
                for ij in range(len(mod_junk)):
                    if curve_dist(mod_junk[:ij]) >= 0.5 * full_length:
                        pre_mid_j = mod_junk[ij]
                        break


                # pre_mid_j = mod_junk[round(len(mod_junk)/2)]
                mid_dists_j = []

                if mod_junk[0] == mod_junk[-1]:
                    smoothed_geometry = catmull_rom_smooth(mod_junk)
                else:
                    smoothed_geometry = chaikin_smooth(mod_junk, keep_ends = True)
                if smoothed_geometry[0] == smoothed_geometry[1]:
                    del smoothed_geometry[1]
                if smoothed_geometry[-1] == smoothed_geometry[-2]:
                    del smoothed_geometry[-2]

                # for jobj in smoothed_geometry:
                #     mid_dists_j.append((jobj[0]-pre_mid_j[0])**2+(jobj[1]-pre_mid_j[1])**2)
                # midpoint = smoothed_geometry[mid_dists_j.index(min(mid_dists_j))]

                for ij in range(len(smoothed_geometry)):
                    if curve_dist(smoothed_geometry[:ij]) >= 0.5 * full_length:
                        midpoint= smoothed_geometry[ij]
                        break
                

                print('midp calc')
                # midpoint = smoothed_geometry[mid_dists_j.index(min(mid_dists_j))]
                


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
                self.is_drawing = False

                if self.computer:
                    self.player_turn = False

                if self.saved:
                    self.root.title('Game of Sprouts' + ' - Graph ' + str(self.ret_save) + ' - Unsaved Changes')
                    self.saved = False

            else:
                if self.good_start == True:
                    self.is_drawing = False
                    self.play = self.play - 1
        else:
            if self.good_start == True:
                self.is_drawing = False
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
        global abs_mouse
        ipos_x, ipos_y = pg.position()
        mouse.release()
        abs_mouse(self, 0, 0)
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
        
        pg.moveTo(ipos_x, ipos_y)

    def save_graph(self, *event):
        # #play, self.main_stor, self.point_stor, self.degrees
        # print('* * * * * Saving * * * * ')
        # print(self.play + 1)
        # print(self.main_stor)
        # print(self.point_stor)
        # print(self.degrees)
        if len(self.main_stor) >= 0:
            self.draw_bound()
            if not self.mult_save:
                self.ret_save = saving_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y, False, 0)
            else:
                self.ret_save = saving_module.save_g(self.play, self.main_stor, self.point_stor, self.degrees, self.left_x, self.top_y, True, self.ret_save)
            print('Saved as Graph ' + str(self.ret_save))
            self.root.title('Game of Sprouts' + ' - Graph ' + str(self.ret_save))

            self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\Graph " + str(self.ret_save) + r"\Graph.png")
            self.point_view(event)
            self.text_view(event)
            self.canvas.update()
            self.image_grab(event, r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\Graph " + str(self.ret_save) + r"\Plain.png")
            self.point_view(event)
            self.text_view(event)
            self.canvas.update()

            self.saved = True
            self.mult_save = True
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

    def reset_graph(self, *event, **kwargs):
        cond = kwargs.get('cond', False)
        if cond!= False:
            self.canvas.focus_set()
            self.home_window.destroy()
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
        self.computer = False
        self.computer_play = 0
        self.player_turn = False
        self.c_left = 0
        self.mult_save = False
        self.comp_debug = 0

        self.comp_path = 0
        self.temp_state = 'placehold'
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


    def open_graph(self, *event, **kwargs):
        global open_cond
        cond = kwargs.get('cond', False)
        overide = kwargs.get('overide', None)
        self.root.focus()
        print('* * * * * * *')
        print(cond)
        if cond == False:
            graph_path = askdirectory(title='Select Folder', initialdir = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs")
        elif cond == True:
            print('testcase')
            # self.home_window.lower(self.root)
            self.home_window.destroy()
            graph_path = overide.replace('\\', '/')
        elif cond == 'Alt':
            self.canvas.focus_set()
            self.home_window.destroy()
            graph_path = askdirectory(title='Select Folder', initialdir = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs")
        
        self.canvas.focus_set()
        if len(graph_path) == 0:
            return
        print(graph_path)
        self.canvas.delete('all')
        self.is_drawing = False
        self.good_start = False
        self.line_id = None
        self.length = False
        self.main_stor = []
        self.line_stor = []
        self.freq = 1
        self.computer = False
        self.computer_play = 0
        self.player_turn = False
        self.comp_path = 0
        self.temp_state = 'placehold'
        self.c_left = 0
        self.mult_save = False
        self.comp_debug = 0

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
        self.root.title('Game of Sprouts - ' + graph_path.split('/')[-1] + ' - opened')
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
        if not self.saved:
            messagebox.showerror('Graph Analysis Error', 'Error: Please save the graph or open a saved graph!')
        else:
            self.analysis_window = tk.Toplevel(self.root)
            self.analysis_window.geometry('%dx%d+%d+%d' % (700, 800, 1005, 100))
            self.analysis_window.resizable(False, False)
            self.analysis_window.title('Graph Analysis')
            self.path_computed = False
            self.valid_paths, self.throw1, self.throw2, self.path_colors = 0, 0, 0, 0
            self.prev_path_tab = 0
            self.prev_prop_tab = 0
            

            a_menubar = tk.Menu(self.analysis_window)    

            a_help_ = tk.Menu(a_menubar, tearoff = 0)
            a_menubar.add_cascade(label ='Help', menu = a_help_)
            a_help_.add_command(label ='Info', command = self.main_about)

            selec = self.ret_save

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

            fig = plt.figure(num= 100, figsize=(3, 3), facecolor='#F0F0F0')
            # self.fig
            # = plt.figure(figsize=(3, 3), facecolor='#F0F0F0')
            def redraw_colored():
                plt.imshow(fill_image)
                for i, point in enumerate(rp_stor):
                    x, y = point
                    plt.scatter(x , y, marker='o', color="red", edgecolors='black', s = 15, zorder = 5)
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

            canvas = FigureCanvasTkAgg(fig, master = self.analysis_window)   
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

                        # print(current_live)
                        # print(another_live)
                        if len(current_live) + len(another_live) - len(check_live) >= 2:
                            associations.append("Region " + str(x + 1))
                

                alive_L = tk.Label(iframe, text="Live Points: " + str(alive))
                dead_L = tk.Label(iframe, text="Dead Points: " + str(dead))
                interact_L = tk.Label(iframe, text="Possible Interactions: " + str(associations), wraplength=604, anchor='w', justify="left")
                alive_L.grid(row = 1, column = 0, sticky = "W", pady = 2)
                dead_L.grid(row = 2, column = 0, sticky = "W", pady = 2)
                # interact_L.grid(row = 5, column = 0, sticky = "W", pady = 2)

            # print(dict_rep)

            def prop_tab_change(event):
                plt.clf()
                redraw_colored()

                if str(event.widget.tab('current')['text']) != 'General':
                    tab = int(str(event.widget.tab('current')['text']).split(' ')[-1]) - 1
                    self.prev_prop_tab = tab
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
                            plt.scatter(x , y, marker='o', color="lime", edgecolors='black', s = 15, zorder = 6)
                        else:
                            plt.scatter(x , y, marker='o', color="grey", edgecolors='black', s = 15, zorder = 6)

                    # plt.scatter(20 + 20 * tab, 20 * tab)
                    canvas.draw()
                else:
                    self.prev_prop_tab = -1
                    redraw_colored()
                    canvas.draw()

            def outer_tab_change(event):
                print('changed')
                if str(event.widget.tab('current')['text']) == 'Path Analysis':
                    if  not self.path_computed:
                        print("OMG START")
                        self.path_computed = True

                        bar_area = tk.Toplevel()
                        bar_area.title("Computing Paths")
                        bar_area.geometry('%dx%d+%d+%d' % (400, 50, 1150, 400))
                        progress = ttk.Progressbar(bar_area, mode = 'indeterminate', length=250)
                        progress.pack()
                        progress.start()
                        bar_area.update()

                        def task():
                             self.valid_paths, self.throw1, self.throw2, self.path_colors, cc1 = sprouts_path.main(selec, 0)

                        thread = Thread(target=task)
                        thread.setDaemon(True)
                        thread.start()
                        while self.valid_paths == 0:
                            self.analysis_window.update()
                            continue

                        progress.stop()
                        progress.destroy()
                        bar_area.destroy()

                        # self.valid_paths, self.throw1, self.throw2 = sprouts_path.main(selec)
                        plt.figure(fig.number)
                        print(plt.gcf())

                        self.valid_paths = list(self.valid_paths.items())
                        # for obj in self.valid_paths:
                        #     print(obj)
                        #     print(' ')
                        if len(self.valid_paths) > 0:
                            for i in range(len(self.valid_paths)):
                                if self.valid_paths[i][-1] != 0:
                                    ipath_top = tk.Frame(path_note)
                                    ipath_top.pack(side="top", expand=1, fill="both")

                                    ipf = ScrolledFrame(ipath_top, width=380, height=240)
                                    ipframe = ipf.display_widget(tk.Frame)
                                    ipf.pack(side="top", expand=1, fill="both")

                                    ipf.bind_arrow_keys(ipath_top)
                                    ipf.bind_scroll_wheel(ipath_top)

                                    # ibound_L = tk.Label(ipframe, text="Boundary Points: " + str(set_rep[i]), wraplength=604, anchor='w', justify="left")
                                    # ibound_L.grid(row = 0, column = 0, sticky = "W", pady = 2)
                                    
                                    current_path_start = self.valid_paths[i][0][0]
                                    current_path_end = self.valid_paths[i][0][1]
                                    current_routes = []
                                    start_let = names[rp_stor.index(current_path_start) + 1]
                                    end_let = names[rp_stor.index(current_path_end) + 1]
                                    ptype = 0

                                    for col, info in self.valid_paths[i][-1].items():
                                        current_routes.append('Region ' + str(self.path_colors.index(col) + 1))

                                    if start_let == end_let:
                                        ptype = 'Loop'
                                    elif len(current_routes) > 1:
                                        ptype = 'Multiple-Route Path'
                                    else:
                                        ptype = 'Generic Path'  
                                        
                                    type_L = tk.Label(ipframe, text="Path Type: " + ptype, wraplength=604, anchor='w', justify="left")
                                    type_L.grid(row = 0, column = 0, sticky = "W", pady = 2)
                                    
                                    start_L = tk.Label(ipframe, text="Start Point: " + start_let, wraplength=604, anchor='w', justify="left")
                                    start_L.grid(row = 1, column = 0, sticky = "W", pady = 2)
                                    
                                    end_L = tk.Label(ipframe, text="End Point: " + end_let, wraplength=604, anchor='w', justify="left")
                                    end_L.grid(row = 2, column = 0, sticky = "W", pady = 2)

                                    rou_L = tk.Label(ipframe, text="Routes: " + str(current_routes), wraplength=604, anchor='w', justify="left")
                                    rou_L.grid(row = 3, column = 0, sticky = "W", pady = 2)

                                    path_note.add(ipath_top, text=f"Path {i+1}")
                        else:
                            ipath_top = tk.Frame(path_note)
                            ipath_top.pack(side="top", expand=1, fill="both")

                            ipf = ScrolledFrame(ipath_top, width=380, height=240)
                            ipframe = ipf.display_widget(tk.Frame)
                            ipf.pack(side="top", expand=1, fill="both")

                            warn_L = tk.Label(ipframe, text="No possible moves", wraplength=604, anchor='w', justify="left")
                            warn_L.grid(row = 0, column = 0, sticky = "W", pady = 2)

                            path_note.add(ipath_top, text=f"Complete Game")

                    else:
                        plt.clf()
                        redraw_colored()
                        if len(self.valid_paths) > 0:
                            path_points = []
                            midpoints = []
                            data = self.valid_paths[self.prev_path_tab][-1]

                            for col, info in data.items():
                                path_points.append(info['path'])
                                midpoints.append(info['midpoint'])
                            
                            for path in path_points:
                                x_val = [x[0] for x in path]
                                y_val = [x[1] for x in path]
                                plt.plot(x_val,y_val, color = 'black')

                            for midp in midpoints:
                                plt.scatter(midp[0], midp[1], marker='o', color="red", edgecolors='black', s = 15, zorder = 6)
                            
                        canvas.draw()
                else:
                    if self.path_computed:
                        plt.clf()
                        redraw_colored()
                        if self.prev_prop_tab >= 0:
                            if len(dict_inds[self.prev_prop_tab]['inner']) > 0:
                                for path in dict_inds[self.prev_prop_tab]['inner']:
                                    # print(path)
                                    for ind in path:
                                        x_val = [x[0] for x in rl_stor[ind]]
                                        y_val = [x[1] for x in rl_stor[ind]]
                                        plt.plot(x_val, y_val, color = 'red', linewidth = 2, zorder = 2)
                            
                            if len(dict_inds[self.prev_prop_tab]['boundary']) > 0:
                                for ind in dict_inds[self.prev_prop_tab]['boundary']:
                                        x_val = [x[0] for x in rl_stor[ind]]
                                        y_val = [x[1] for x in rl_stor[ind]]
                                        plt.plot(x_val, y_val, color = 'red', linewidth = 2, zorder = 2)
                            
                            # print(set_rep[tab])
                            for point in set_rep[self.prev_prop_tab]:
                                x, y = rp_stor[names.index(point) - 1]
                                if rdeg[names.index(point) - 1] < 3:
                                    plt.scatter(x , y, marker='o', color="lime", edgecolors='black', s = 15, zorder = 6)
                                else:
                                    plt.scatter(x , y, marker='o', color="grey", edgecolors='black', s = 15, zorder = 6)

                        # plt.scatter(20 + 20 * tab, 20 * tab)
                        canvas.draw()

            def path_tab_change(event):
                plt.clf()
                redraw_colored()
                if len(self.valid_paths)> 0:
                    tab = int(str(event.widget.tab('current')['text']).split(' ')[-1]) - 1
                    self.prev_path_tab = tab
                    path_points = []
                    midpoints = []
                
                    data = self.valid_paths[tab][-1]

                    for col, info in data.items():
                        path_points.append(info['path'])
                        midpoints.append(info['midpoint'])
                    
                    for path in path_points:
                        x_val = [x[0] for x in path]
                        y_val = [x[1] for x in path]
                        plt.plot(x_val,y_val, color = 'black')
                    
                    for midp in midpoints:
                        plt.scatter(midp[0], midp[1], marker='o', color="red", edgecolors='black', s = 15, zorder = 6)
                    
                canvas.draw()                  
            
            outer_note.bind('<<NotebookTabChanged>>', outer_tab_change)
            prop_note.bind(prop_tab_change)
            path_note.bind(path_tab_change)
            
            # Pack the notebook
            prop_note.pack(fill=tk.BOTH, expand = True)
            outer_note.pack(fill=tk.BOTH, expand=True)
            path_note.pack(fill=tk.BOTH, expand=True)

            # color_toggle = tk.Button(self.analysis_window)
            # color_toggle.pack(side='top')
    
    def open_image(self, image_path):
        print(image_path)
     
    def homepage(self, *event):
        self.home_window = tk.Toplevel(self.root)
        self.home_window.focus()
        # self.home_window.attributes('-topmost', 1)
        # self.home_window.wm_transient(self.root)
        self.home_window.title("Welcome - Game of Sprouts 2024")
        self.home_window.geometry('%dx%d+%d+%d' % (950, 600, 125, 250))
        self.home_window.resizable(False, False)
        
        tabControl = ttk.Notebook(self.home_window)
        tabControl.pack(expand=1, fill="both")
        
        home_frame = ttk.Frame(tabControl)
        recent_frame = ttk.Frame(tabControl)
        
        tabControl.add(home_frame, text="Home")
        tabControl.add(recent_frame, text="Recent")

        prev_label = tk.Label(home_frame, text="New")
        prev_label.pack(side=tk.TOP, anchor = 'w', pady=10, padx = 10)

        but_canvas = tk.Canvas(home_frame, bd=0, highlightthickness=0, height = 60)
        but_frame = tk.Frame(but_canvas)
        but_canvas.create_window((0, 0), window=but_frame, anchor=tk.NW)
        
        but_canvas.pack(side=tk.TOP, fill=tk.BOTH)


        open_img = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Open Part.png").convert('RGBA')      
        open_fld = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Open Folder.png").convert('RGBA')      
        I2 = ImageDraw.Draw(open_img)
        # myFont = ImageFont.truetype('FreeMono.ttf', 15)
        I2.text((60, 10), 'Graph', font = ImageFont.truetype("segoeui.ttf", 16), fill =(0, 0, 0))

        I3 = ImageDraw.Draw(open_fld)
        # myFont = ImageFont.truetype('FreeMono.ttf', 15)
        I3.text((60, 10), 'Open', font = ImageFont.truetype("segoeui.ttf", 16), fill =(0, 0, 0))
        open_img = ImageTk.PhotoImage(open_img)
        open_fld = ImageTk.PhotoImage(open_fld)
        
        open_btn = tk.Button(but_frame, image=open_img, bd=0, highlightthickness=0, command= lambda: self.reset_graph(cond = True))
        open_fld_btn = tk.Button(but_frame, image=open_fld, bd=0, highlightthickness=0, comman= lambda: self.open_graph(cond = "Alt"))

        open_btn.image = open_img
        open_fld_btn.image = open_fld
        open_btn.pack(side=tk.LEFT, padx=(40, 10), pady=(5, 10), anchor='w')
        open_fld_btn.pack(side=tk.LEFT, padx=(40, 10), pady=(5, 10), anchor='n')


        sep1 = ttk.Separator(home_frame, orient = 'horizontal')
        sep1.pack( fill='x')

        

        lab_canvas = tk.Canvas(home_frame, bd=0, highlightthickness=0, height = 50)
        lab_frame = tk.Frame(lab_canvas)
        lab_canvas.create_window((0, 0), window=lab_frame, anchor=tk.NW)
        
        lab_canvas.pack(side=tk.TOP, fill=tk.BOTH)

        gall_label = tk.Label(lab_frame, text="Recent Documents")
        gall_label.pack(side=tk.LEFT, anchor = 'n', pady=10, padx = 10)

        def switch_home_tab():
            tabControl.select(1)

        gall_button = tk.Button(lab_frame, text="View All", fg = 'blue', bd=0, highlightthickness=0,  command=lambda: switch_home_tab())
        gall_button.pack(side=tk.LEFT, anchor = 'ne', pady=7, padx = (650, 0))

        
        image_folder = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs"
        canvas = tk.Canvas(home_frame, bd=0, highlightthickness=0, height = 180)
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
        
        scrollbar = ttk.Scrollbar(home_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.pack(side=tk.TOP, fill=tk.BOTH)

        canvas.config(xscrollcommand=scrollbar.set)
        rec_dir = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs\recent.csv"

        #load recent

        rec_list = []
        try:
            rec_df = pd.read_csv(rec_dir, sep=',', header=None)
            rec_array = rec_df.to_numpy(dtype= str)[1:]
        except:
            pass
        else:
            print('recent meep test')
            rec_list = [[str(item[0])] for item in rec_array]
            print(rec_list)
            if len(rec_list) > 10:
                rec_list = rec_list[:10]




        # subdirectories = [d for d in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, d))]
        print('mydirs')
        # # print(subdirectories)
        ball_imgs = [os.path.join(image_folder, d) for d in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, d))]
        ball_imgs.sort(key=os.path.getmtime) 
        subdirectories = [d.split('\\')[-1] for d in ball_imgs]
        # print(subdirectories)
        
        
        
        # all_imgs.sort(key=os.path.getatime)
        # print([f.split('\\')[-1] for f in all_imgs])
        
        idx = 0
        gallery_images = []
        gallery_paths = []
        gallery_names = []
        for subdir in subdirectories:
            subdir_path = os.path.join(image_folder, subdir)
            images = [f for f in os.listdir(subdir_path) if f == "Graph.png"]
            if len(images) > 0:
                idx += 1
            for image in images:
                img_path = os.path.join(subdir_path, image)
                gallery_paths.append(subdir_path)
                gallery_names.append([subdir])
                img2 = Image.open(img_path)
                img2.thumbnail((120, 120))

                img = ImageOps.pad(img2, (120, 120), color=(240, 240, 240))
                img = ImageOps.expand(img, 20, fill=(240, 240, 240))
                img = img.convert('RGBA')
                graph_cover = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts Cover.png").convert('RGBA')      
                result = Image.alpha_composite(img, graph_cover)
             
                I1 = ImageDraw.Draw(result)
                # myFont = ImageFont.truetype('FreeMono.ttf', 15)
                
                I1.text((5, 5), subdir_path.split('\\')[-1], font = ImageFont.truetype("calibri.ttf", 12), fill =(0, 0, 0))
                img = ImageTk.PhotoImage(result)
                gallery_images.append(img)
        
        nidx = 0
        for i in range(len(rec_list)):
            rec_img = gallery_images[gallery_names.index(rec_list[i])]
            rec_path = gallery_paths[gallery_names.index(rec_list[i])]
                                            
            btn = tk.Button(frame, image=rec_img, bd=0, highlightthickness=0, command=lambda img_path=rec_path: self.open_graph(cond = True, overide = img_path))
            btn.image = rec_img

            if i == 0:
                lpad = 50
                rpad = 10
            elif i == len(rec_list) - 1:
                lpad = 10
                rpad = 50
            else:
                lpad = 10
                rpad = 10

                # if idx <=10:
            btn.pack(side=tk.LEFT, padx=(lpad, rpad), pady=5)

        # print(gallery_paths)
        # print(gallery_names)
        scrollbar.pack(side=tk.TOP, padx = 40, fill = tk.X)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        sep2 = ttk.Separator(home_frame, orient = 'horizontal')
        sep2.pack(fill='x', pady = 2)

        # Additional content under the gallery
        additional_label = tk.Label(home_frame, text="Resources")
        additional_label.pack(side=tk.TOP, pady=10, padx=10,  anchor = 'w')


        help_img = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Help Part.png").convert('RGBA')      
        info_img = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Info Part.png").convert('RGBA')      
        I5 = ImageDraw.Draw(help_img)
        I5.text((60, 10), 'Help', font = ImageFont.truetype("segoeui.ttf", 16), fill =(0, 0, 0))
        I6 = ImageDraw.Draw(info_img)
        I6.text((60, 10), 'Info', font = ImageFont.truetype("segoeui.ttf", 16), fill =(0, 0, 0))

        help_img = ImageTk.PhotoImage(help_img)
        info_img = ImageTk.PhotoImage(info_img)
        
        help_btn = tk.Button(home_frame, image=help_img, bd=0, highlightthickness=0, command= lambda: self.main_about())
        info_btn = tk.Button(home_frame, image=info_img, bd=0, highlightthickness=0, command= lambda: self.main_help())
        
        help_btn.image = help_img
        help_btn.pack(side=tk.LEFT, padx=(40, 10), pady=(5, 10), anchor='n')
        info_btn.image = info_img
        info_btn.pack(side=tk.LEFT, padx=(40, 10), pady=(5, 10), anchor='n')

        logo_img = Image.open(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts Logo Transparent.png").convert('RGBA')      
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_btn = tk.Button(home_frame, image=logo_img, bd=0, highlightthickness=0)
        logo_btn.image = logo_img
        logo_btn.pack(side=tk.RIGHT, padx=(40, 10), pady=(5, 10), anchor='s')
        # rec_canvas = tk.Canvas(recent_frame, bd=0, highlightthickness=0, bg = 'red', height = 550)
        # rec_scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=rec_canvas.yview)
        # rec_scrollbar.pack(side=tk.RIGHT, padx = 4, fill = tk.Y)
        # rec_canvas.pack(side = tk.TOP, fill=tk.BOTH)
        # rec_canvas.configure(yscrollcommand=rec_scrollbar.set)

        # for g_row in range(50): #range(math.ceil(len(gallery_images)/2)):
        #     meep = tk.Label(rec_frame, text='meep')
        #     meep.pack(side = tk.LEFT)
        #     # r_canvas = tk.Canvas(rec_frame, bd=0, highlightthickness=0, height = 180, bg = 'blue')
        #     # r_frame = tk.Frame(r_canvas)
        #     # r_canvas.create_window((0, 0), window=r_frame, anchor=tk.NW)
        #     # r_canvas.pack(side=tk.TOP)

        image_folder = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs"
        rec_canvas = tk.Canvas(recent_frame, bd=0, highlightthickness=0, height = 550)
        rec_frame = tk.Frame(rec_canvas)
        rec_canvas.create_window((0, 0), window=rec_frame, anchor=tk.NW)
        
        rec_scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=rec_canvas.yview)
        rec_scrollbar.pack(side=tk.RIGHT, padx = 4, fill = tk.Y)
        rec_canvas.pack(side=tk.TOP, fill=tk.BOTH)
        
        rec_canvas.config(yscrollcommand=rec_scrollbar.set)
        # subdirectories = [d for d in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, d))]
        

        for g_row in range(math.ceil(len(gallery_images)/5)):
            r_canvas = tk.Canvas(rec_frame, bd=0, highlightthickness=0, width = 900, height = 180)
            r_frame = tk.Frame(r_canvas)
            r_canvas.create_window((0, 0), window=r_frame, anchor=tk.NW)
            r_canvas.pack(side=tk.TOP, fill = tk.X, padx = 10, pady = 10)

            for add in range(min(5, len(gallery_images) - 5*g_row)):
                r_btn = tk.Button(r_canvas, image=gallery_images[add + 5*g_row], bd=0, highlightthickness=0, command=lambda img_path=gallery_paths[add + 5*g_row]: self.open_graph(cond = True, overide = img_path))
                r_btn.image = gallery_images[add + 5*g_row]
                r_btn.pack(side=tk.LEFT, padx=10, pady=5)

        rec_frame.update_idletasks()
        rec_canvas.config(scrollregion=rec_canvas.bbox("all"))
          
        def on_closing():
            self.canvas.focus_set()
            self.home_window.destroy()
        
        self.home_window.protocol("WM_DELETE_WINDOW", on_closing)
        # sep1.place(relx = 0, rely = 0.53, relwidth=1, relheight = 1)
root = tk.Tk()
app = smooth_fix(root)
root.mainloop()
