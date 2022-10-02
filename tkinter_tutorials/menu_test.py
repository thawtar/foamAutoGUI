#from doctest import master
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox 
import os


class Window(tk.Frame):
    def __init__(self,master=None):
        super().__init__()
        self.master = master
        self.isInCaseDirectory = 0
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label='Open',command=self.openCase)
        fileMenu.add_command(label='Exit',command=self.exitProgram)
        menu.add_cascade(label='File',menu=fileMenu)

        helpMenu = tk.Menu(menu)
        helpMenu.add_command(label="About")
        helpMenu.add_command(label="Help")
        menu.add_cascade(label="Help", menu=helpMenu)

    def exitProgram(self):
        exit(0)

    def openCase(self):
        #global isInCaseDirectory

        previousDir = os.getcwd() # to temporarily store path of previous directory
        directoryPath=fd.askdirectory()

        print("Opening Case Directory:"+directoryPath)
        if (directoryPath != ""):
            os.chdir(directoryPath)
        directoryPath = os.getcwd()
        print("Current directory path: ",directoryPath)
        parent_dir = directoryPath
        dir_0 = "0"
        dir_constant = "constant"
        dir_system = "system"
        dir_0 = os.path.join(parent_dir, dir_0)
        dir_constant = os.path.join(parent_dir, dir_constant)
        dir_system = os.path.join(parent_dir, dir_system)
        # confirm before creating the directories

        if (os.path.exists(dir_0) and os.path.exists(dir_constant) and os.path.exists(dir_system)):
            print("Found 0, constant and system directories")
            isInCaseDirectory = 1
        else:
            print("Not an OpenFOAM directory. Choose another directory")
            isInCaseDirectory = 0

root = tk.Tk()
app = Window(root)
root.wm_title("Menu test")
root.mainloop()
