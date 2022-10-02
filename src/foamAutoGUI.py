import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox 
import os
from PIL import Image, ImageTk
import glob
import subprocess
import yaml

#class App(tk.Tk):
#

# Flags to confirm the status of the directory, file system, etc
isInCaseDirectory = 0 # whether the current directory is a case directory for openfoam

mainDirectory = "" # to store the main case directory path

def write_string(data, filename="blockMeshDict"):
    f=open(file=filename,mode="w")
    f.write(data)
    f.close()

def printWelcome():
    welcomeLogo = "===================================================\n \
                 Welcome to foamAuto       \n\
===================================================\n"
    #print("===================================================\n")
    #print("                 Welcome to foamAuto       \n")
    #print("===================================================\n")
    print(welcomeLogo)

def oflogo():
    logo = " /*--------------------------------*- C++ -*---------------------------------*\\\n \
| =========                |                                                 | \n \
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n \
|  \\    /   O peration     | Version:  v2012                                 | \n \
|   \\  /    A nd           | Website:  www.openfoam.com                      | \n \
|    \\/     M anipulation  |                                                 | \n \
\\*--------------------------------------------------------------------------*/ \n \
"
    return logo


def blockMeshCreator(data):
    def createVertices(x1, x2, y1, y2, z1, z2):
        s = " "
        # (x1,x2,y1,y2,z1,z2) = data
        x1, x2, y1, y2, z1, z2 = str(x1), str(x2), str(y1), str(y2), str(z1), str(z2)
        tmp = "\nvertices (\n"
        tmp = tmp + "\t(" + x1 + s + y1 + s + z1 + ")\n"
        tmp = tmp + "\t(" + x2 + s + y1 + s + z1 + ")\n"
        tmp = tmp + "\t(" + x2 + s + y2 + s + z1 + ")\n"
        tmp = tmp + "\t(" + x1 + s + y2 + s + z1 + ")\n"
        tmp = tmp + "\t(" + x1 + s + y1 + s + z2 + ")\n"
        tmp = tmp + "\t(" + x2 + s + y1 + s + z2 + ")\n"
        tmp = tmp + "\t(" + x2 + s + y2 + s + z2 + ")\n"
        tmp = tmp + "\t(" + x1 + s + y2 + s + z2 + ")\n"
        tmp = tmp + ");\n\n"
        return tmp

    def createBlocks(nx, ny, nz):
        s = " "
        tmp = "blocks\n(\n\thex (0 1 2 3 4 5 6 7) (" + str(nx) + s + str(ny) + s + str(nz)
        tmp = tmp + ") simpleGrading (1 1 1)\n);\n\n"
        return tmp

    def createEdges():
        tmp = "edges (\n);\n\n"
        return tmp

    def createMergePairs():
        tmp = "mergePatchPairs (\n);\n\n"
        return tmp

    def createBoundaries():
        tmp = "boundary\n(\n"
        tmp = tmp + "left\n{\n\ttype patch;\n\tfaces ((0 3 7 4));\n}\n"
        tmp = tmp + "right\n{\n\ttype patch;\n\tfaces ((1 2 6 5));\n}\n"
        tmp = tmp + "top\n{\n\ttype patch;\n\tfaces ((4 5 6 7));\n}\n"
        tmp = tmp + "bottom\n{\n\ttype patch;\n\tfaces ((0 1 2 3));\n}\n"
        tmp = tmp + "front\n{\n\ttype patch;\n\tfaces ((4 5 1 0));\n}\n"
        tmp = tmp + "back\n{\n\ttype patch;\n\tfaces ((7 6 2 3));\n}\n"
        tmp = tmp + ");\n\n"
        return tmp
    (x1,x2,y1,y2,z1,z2,nx,ny,nz) = data # extract the tuple of data
    lx,ly,lz = np.abs(x2-x1),np.abs(y2-y1),np.abs(z2-z1)
    scale = 1.0 # scale to be used
    blockMeshString = oflogo()
    blockMeshString = blockMeshString+ "FoamFile\n \
{ \n \
    version     2.0; \n \
    format      ascii; \n \
    class       dictionary;\n \
    object      blockMeshDict;\n \
}\n"
    blockMeshString = blockMeshString+"\nscale\t"+str(scale)+";\n"
    blockMeshString = blockMeshString+createVertices(x1,x2,y1,y2,z1,z2)
    blockMeshString = blockMeshString+createBlocks(nx,ny,nz)+createEdges()
    blockMeshString = blockMeshString+createBoundaries()+createMergePairs()
    print(blockMeshString)
    print(data)
    if(isInCaseDirectory):
        blockMeshPath = os.getcwd()+"/system/blockMeshDict"
        print("Writing blockMeshDict file")
        write_string(blockMeshString,blockMeshPath)
        #subprocess.run("wsl")
        #subprocess.run("blockMesh")
    else:
        
        #print("Error, not in an OpenFOAM case directory. Exiting...")
        messagebox.showinfo("FoamAuto", "Not in an OpenFOAM case directory.")
        #exit(-1)
    #px, py, pz = 0.0, 0.0, 0.0 # minimum point of the domain. the lengths count from here

def snappyHexMeshCreator(snappyData, dataFile="snappyMeshSettings.yaml"):
    print("Reading snappyHexMeshSettings.yaml file")



def storeYamlData(dataFile):
    print("Storing YAML Data...")



def gui():
    root = tk.Tk()
    root.title('foamAuto Case Creator')
    root.resizable(False, False)
    root.geometry('800x600')
    ico = Image.open("gear.png")
    photo=ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False,photo)


    def openCase():
        global isInCaseDirectory

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


    def createCase():
        global isInCaseDirectory
        okFlag = 0 # to store whether OK button was clciked in dialog box
        print("Create Case Directory clicked")
        directoryPath = fd.askdirectory()
        if (directoryPath != ""):
            os.chdir(directoryPath)
            okFlag = 1
        directoryPath = os.getcwd()
        print("Current directory path: ", directoryPath)

        parent_dir = directoryPath
        # to create the case directory,
        dir_0 = "0"
        dir_constant = "constant"
        dir_system = "system"
        dir_0 = os.path.join(parent_dir,dir_0)
        dir_constant = os.path.join(parent_dir,dir_constant)
        dir_system = os.path.join(parent_dir,dir_system)
        # confirm before creating the directories
        response = 0
        if(okFlag):
            response=messagebox.askyesno("foamAuto","Are you sure to create case files in: "+parent_dir)
        if(response):
            if(os.path.exists(dir_0)):
                print("Directory already exists")
            else:
                os.makedirs(name=dir_0)
                print("Directory created: " + dir_0)
            if (os.path.exists(dir_constant)):
                print("Directory already exists")
            else:
                os.makedirs(name=dir_constant)
                print("Directory created: " + dir_constant)

            if (os.path.exists(dir_system)):
                print("Directory already exists")
            else:
                os.makedirs(name=dir_system)
                print("Directory created: " + dir_system)
            isInCaseDirectory = 1

    def startBlockMesh():
        print("Creating file for blockMesh...")
        blockMeshDialog = tk.Toplevel()
        blockMeshDialog.resizable(False, False)
        blockMeshDialog.geometry('400x150')
        blockMeshDialog.wm_iconphoto(False, photo)
        blockMeshDialog.title('blockMesh File Creator')
        # Input items
        x1_get = tk.Entry(blockMeshDialog)
        x2_get = tk.Entry(blockMeshDialog)
        y1_get = tk.Entry(blockMeshDialog)
        y2_get = tk.Entry(blockMeshDialog)
        z1_get = tk.Entry(blockMeshDialog)
        z2_get = tk.Entry(blockMeshDialog)
        nx_get = tk.Entry(blockMeshDialog)
        ny_get = tk.Entry(blockMeshDialog)
        nz_get = tk.Entry(blockMeshDialog)
        x1_get.insert(0,"0")
        x2_get.insert(0, "1")
        y1_get.insert(0, "0")
        y2_get.insert(0, "1")
        z1_get.insert(0, "0")
        z2_get.insert(0, "1")
        nx_get.insert(0, "1")
        ny_get.insert(0, "1")
        nz_get.insert(0, "1")
        label_x = tk.Label(blockMeshDialog,text="x")
        label_y = tk.Label(blockMeshDialog, text="y")
        label_z = tk.Label(blockMeshDialog, text="z")
        label_from = tk.Label(blockMeshDialog, text="From")
        label_to = tk.Label(blockMeshDialog, text="To")
        label_elements = tk.Label(blockMeshDialog, text="Elements")


        # Inner functions for Button presses
        def OK():
            print("Pressed OK button")
            x1 = float(x1_get.get())
            x2 = float(x2_get.get())
            y1 = float(y1_get.get())
            y2 = float(y2_get.get())
            z1 = float(z1_get.get())
            z2 = float(z2_get.get())
            nx = int(nx_get.get())
            ny = int(ny_get.get())
            nz = int(nz_get.get())
            #print(x1,x2,y1,y2,z1,z2,nx,ny,nz)
            data = (x1,x2,y1,y2,z1,z2,nx,ny,nz)
            blockMeshCreator(data=data)
            blockMeshDialog.destroy()


        def cancel():
            print("Pressed Cancel button")
            blockMeshDialog.destroy()

        button_OK = tk.Button(blockMeshDialog,text="OK",command=OK)
        button_Cancel = tk.Button(blockMeshDialog, text="Cancel",command=cancel)
        # place the buttons and labels on the window
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
        button_OK.grid(row=4,column=1)
        button_Cancel.grid(row=4, column=2)


    def startSnappyHexMesh():
        print("Starting snappyHexMesh")

    openButton = tk.Button(root,text="Open Case Directory",command=openCase)
    createButton=tk.Button(root,text="Create Case Directory", command=createCase)
    createBlockMeshButton = tk.Button(root,text="blockMesh",command=startBlockMesh)
    createSnappyHexMeshButton = tk.Button(root, text="snappyHexMesh", command=startSnappyHexMesh)
    about = ImageTk.PhotoImage(Image.open("about.jpg"))
    aboutImg = tk.Label(image=about)
    openButton.grid(row=2,column=0,pady=1,ipady=30,ipadx=80)
    createButton.grid(row=3,column=0,pady=1, ipady=30,ipadx=80)
    createBlockMeshButton.grid(row=4,column=0,pady=1, ipady=30,ipadx=100)
    createSnappyHexMeshButton.grid(row=5, column=0, pady=1, ipady=30, ipadx=100)
    aboutImg.grid(row=3,column=2,ipady=20,ipadx=20)
    root.mainloop()

printWelcome()

gui()