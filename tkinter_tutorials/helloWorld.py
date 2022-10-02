import tkinter as tk
from tkinter import ttk

class HelloView(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.name = tk.StringVar
        self.hello_string=tk.StringVar
        self.hello_string.set(self,value="Hello World!")
        name_label = ttk.Label(self,text="Name")
        name_entry=ttk.Entry(self,textvariable=self.name)
        ch_button = ttk.Button(self,text="Change",command=self.on_change)
        hello_label = ttk.Label(self,textvariable=self.hello_string,font=("TKDefaultFont",64),
        wraplength=600)
        name_label.grid(row=0,column=0,sticky=tk.W)
        name_entry.grid(row=0,column=1,sticky=(tk.W+tk.E))
        ch_button.grid(row=0,column=2,sticky=tk.E)
        hello_label.grid(row=1,column=0,columnspan=3)
        


root = tk.Tk()
app = HelloView(root)
root.wm_title("Menu test")
root.mainloop()
