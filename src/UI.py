import numpy as np
import tkinter as tk

class MainWindow:
    def __init__(self,root):
        super().__init__()
        self.root = root
        self.create_gui()

    def create_top_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Create Project")
        self.file_menu.add_command(label="Load Project")
        self.file_menu.add_command(label="Save Project")

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="Help")
        self.root.config(menu=self.menu_bar)
        

    def create_blockMesh_inputs(self):
        print("Creating blockMesh inputs")
        # Input items
        x1_get = tk.Entry(self.root)
        x2_get = tk.Entry(self.root)
        y1_get = tk.Entry(self.root)
        y2_get = tk.Entry(self.root)
        z1_get = tk.Entry(self.root)
        z2_get = tk.Entry(self.root)
        nx_get = tk.Entry(self.root)
        ny_get = tk.Entry(self.root)
        nz_get = tk.Entry(self.root)
        x1_get.insert(0,"0")
        x2_get.insert(0, "1")
        y1_get.insert(0, "0")
        y2_get.insert(0, "1")
        z1_get.insert(0, "0")
        z2_get.insert(0, "1")
        nx_get.insert(0, "1")
        ny_get.insert(0, "1")
        nz_get.insert(0, "1")
        label_x = tk.Label(self.root,text="x")
        label_y = tk.Label(self.root, text="y")
        label_z = tk.Label(self.root, text="z")
        label_from = tk.Label(self.root, text="From")
        label_to = tk.Label(self.root, text="To")
        label_elements = tk.Label(self.root, text="Elements")

        label_x.grid(row=1,column=0)
        label_y.grid(row=2, column=0)
        label_z.grid(row=3, column=0)
        label_from.grid(row=0,column=1)
        label_to.grid(row=0, column=2)
        label_elements.grid(row=0, column=3)
        x1_get.grid(row=1,column=1)
        x2_get.grid(row=1, column=2)
        nx_get.grid(row=1, column=3)
        y1_get.grid(row=2, column=1)
        y2_get.grid(row=2, column=2)
        ny_get.grid(row=2, column=3)
        z1_get.grid(row=3, column=1)
        z2_get.grid(row=3, column=2)
        nz_get.grid(row=3, column=3)


    def create_gui(self):
        self.create_top_menu()
        self.create_blockMesh_inputs()

if __name__ == '__main__':
    root = tk.Tk()
    MainWindow(root=root)
    root.mainloop()
        