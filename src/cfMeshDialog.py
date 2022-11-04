# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# The main purpose of this module is provide fundamental IO functionalities to deal with 
# OpenFOAM files. This includes definition of default values which will be updated in the GUI.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5 import uic
import vtk
import primitives.IO as IO
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor



class cfMeshDialog(QMainWindow):
    def __init__(self, ):
        super().__init__()
        uic.loadUi("cfMeshDialog.ui", self)
        self.setWindowTitle("cfMesh GUI")
        self.prepare_vtk()
        self.prepare_events()

    def prepare_vtk(self):
        # Prepare the VTK widget to show the STL
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.widget)
        self.vl.addWidget(self.vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.vtkWidget.resize(520,310)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

    def prepare_events(self):
        # Initiate the button click maps
        self.pushButtonSTLImport.clicked.connect(self.openSTL)
        self.pushButtonCreateMesh.clicked.connect(self.createMesh)
        self.listSurfaceList.clicked.connect(self.surfaceChosen)
        self.pushButtonBackground.clicked.connect(self.defineBackgroundDomain)
        self.pushButtonSplitSTL.clicked.connect(self.splitSurfaces)
        self.pushButtonCAD_Import.clicked.connect(self.importCAD)
        self.statusbar.showMessage("Ready") # initial status bar message
 
    def updateStatusBar(self,message="Go!"):
        self.statusbar.showMessage(message)

    def surfaceChosen(self):
        item = self.listSurfaceList.currentItem()
        print(item.text())   

    # this function will read STL file and show it in the VTK renderer
    def showSTL(self,stlFile=r"pipe.stl"):
        # Read stl
        try:
            reader = vtk.vtkSTLReader()
            reader.SetFileName(stlFile)
        except:
            print("Reading STL not successful. Try again")
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.iren.Initialize()

    def loadSTL(self,stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        self.updateStatusBar("Loading STL file")
        stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"
        surfaces=IO.readSTL(stlFileName=stlFile)
        print(surfaces)
        for (i,aSurface) in enumerate(surfaces):
            self.listSurfaceList.insertItem(i,aSurface)
        message = "Loaded STL file: "+stlFile
        self.updateStatusBar(message)  

    def openSTLDialog(self):
        fname,ftype = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"STL files (*.stl *.obj)")
        if(fname==""):
            return -1 # STL file not loaded
        else:
            print("Current STL File: ",fname)
            return fname

    def openCADDialog(self):
        fname,ftype = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"CAD files (*.brep *.igs *.iges)")
        if(fname==""):
            return -1 # CAD file not loaded
        else:
            print("Current CAD File: ",fname)
            return fname

    def openSTL(self):
        stlFileName = self.openSTLDialog()
        if(stlFileName==-1):
            pass
        else:
            self.showSTL(stlFile=stlFileName)
            self.loadSTL()

    def splitSurfaces(self):
        self.updateStatusBar("Spliting surfaces")

    def importCAD(self):
        cadFileName = self.openCADDialog()
        if(cadFileName==""):
            pass #print("CAD file not found...")
        else:
            self.updateStatusBar("CAD File imported: ",cadFileName)

    def defineBackgroundDomain(self):
        self.updateStatusBar("Creating background domain")

    def createMesh(self):
        print("Creating Cartesian Mesh...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = cfMeshDialog()
    mainWindow.show()  
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing")

