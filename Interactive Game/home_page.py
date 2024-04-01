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
import computer_module
import warnings
import ctypes
import sys
from threading import Thread
sys.path.append(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Path-Finding Notebooks")
sprouts_regions = __import__("sprouts_regions")
sprouts_planarity = __import__("sprouts_planarity")
sprouts_path = __import__("sprouts_path_finder")
scroll = __import__("ScrollableNotebook")
from PIL import Image, ImageOps, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
from tkinter import *
from tkinter import ttk
import os
from PIL import Image, ImageTk

save_path = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs"
numb_saves = len(next(os.walk(save_path))[1])

from tkinter import *
from tkinter import ttk
import os
from PIL import Image, ImageTk


class ImageButton(Button):
    def __init__(self, master, image_path, command):
        super().__init__(master, image=None, command=command)
        self.image_path = image_path

        # Load image and resize it to fit the button
        image = Image.open(image_path)
        max_width = 100  # Change this to your desired maximum width
        image_ratio = image.width / image.height
        new_width = min(max_width, image_ratio * max_width)
        new_height = image.height * new_width / image.width
        image = image.resize((int(new_width), int(new_height)), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Set the image as the button's image
        self.config(image=photo)
        self.photo = photo

    def __del__(self):
        self.photo.close()


class ScrollableImageButtonFrame(Frame):
    def __init__(self, master, folder_path):
        super().__init__(master)
        self.folder_path = folder_path

        # Create a canvas and scrollbar
        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="bottom", fill="x")

        # Get all image paths in the folder
        self.image_paths = [os.path.join(folder_path, subfolder, image)
                           for subfolder, _, images in os.walk(folder_path)
                           for image in images if image.lower().endswith((".jpg", ".png"))]

        # Display images as buttons with margin
        self.margin = 100  # Change this to your desired margin
        self.display_images()

    def display_images(self):
        x = self.margin
        for image_path in self.image_paths:
            button = ImageButton(self.canvas, image_path, lambda: print(f"Clicked: {image_path}"))
            button.place(x=x, y=self.margin)
            x += button.winfo_width() + self.margin

        # Configure the canvas region to fit all buttons
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = Tk()
    root.title("Image Button Browser")

    # Replace this with your actual folder path
    folder_path = save_path

    # Create the scrollable image button frame
    frame = ScrollableImageButtonFrame(root, folder_path)
    frame.pack(fill="both", expand=True)

    root.mainloop()







