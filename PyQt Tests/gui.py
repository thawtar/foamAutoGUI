import tkinter as tk
import os
from PIL import Image, ImageTk

def gui():
    root = tk.Tk()
    root.title('foamAuto Case Creator')
    root.resizable(False, False)
    root.geometry('800x600')
    ico = Image.open("gear.png")
    photo=ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False,photo)
    root.mainloop()

gui()

