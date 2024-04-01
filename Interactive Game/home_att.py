import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import os

def open_image(image_path):
    print("Opening", image_path)

def main():
    root = tk.Tk()
    root.title("Homepage")
    root.geometry("800x600")
    
    tabControl = ttk.Notebook(root)
    tabControl.pack(expand=1, fill="both")
    
    home_frame = ttk.Frame(tabControl)
    recent_frame = ttk.Frame(tabControl)
    
    tabControl.add(home_frame, text="Home")
    tabControl.add(recent_frame, text="Recent")

    prev_label = tk.Label(home_frame, text="Additional Content")
    prev_label.pack(side=tk.TOP, pady=10)

    
    image_folder = r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Saved Graphs"
    canvas = tk.Canvas(home_frame, bd=0, highlightthickness=0, height=120)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)
    
    scrollbar = ttk.Scrollbar(home_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas.pack(side=tk.TOP, fill=tk.BOTH)
    
    canvas.config(xscrollcommand=scrollbar.set)
    subdirectories = [d for d in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, d))]
    
    for subdir in subdirectories:
        subdir_path = os.path.join(image_folder, subdir)
        images = [f for f in os.listdir(subdir_path) if f == "Graph.png"]
        for image in images:
            img_path = os.path.join(subdir_path, image)
            img2 = Image.open(img_path)
            img2.thumbnail((100, 100))

            ImageOps.pad(img2, (100, 100), color=(240, 240, 240)).save(r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\meep.png")
            img = ImageOps.pad(img2, (100, 100), color=(240, 240, 240))
            img = ImageTk.PhotoImage(img)
            
            
            btn = tk.Button(frame, image=img, command=lambda img_path=img_path: open_image(img_path))
            btn.image = img
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    scrollbar.pack(side=tk.TOP, fill=tk.X)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Additional content under the gallery
    additional_label = tk.Label(home_frame, text="Additional Content")
    additional_label.pack(side=tk.TOP, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()



