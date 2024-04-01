from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf

def open_pdf():
    """Opens a file dialog and displays the selected PDF in a new window."""
    filename=r"C:\Users\2000039241\OneDrive - Fulton County Schools\Desktop\Sprouts-main\Resources\Sprouts Rules.pdf"

    if filename:
        new_window = Toplevel(root)
        new_window.geometry('%dx%d+%d+%d' % (600, 800, 1000, 120))
        new_window.title("PDF Viewer")
        viewer = pdf.ShowPdf()
        view = viewer.pdf_view(new_window, pdf_location=filename)
        view.pack(fill=BOTH, expand=True)

root = Tk()
root.title("PDF Opener")

button = Button(root, text="Open PDF", command=open_pdf)
button.pack(padx=10, pady=10)

root.mainloop()
