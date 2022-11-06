# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# The main purpose of this module is provide fundamental IO functionalities to deal with 
# OpenFOAM files. This includes definition of default values which will be updated in the GUI.

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QDialog
from PyQt5 import QtWidgets
from PyQt5 import uic
import vtk
import primitives.IO as IO
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from foamCaseCreator import foamCase
#from foamCLI import *
import foamCLI
import shutil

# global values to store the case name and directory path
# should not be abused!
caseName = None
caseDirectoryPath = None
caseCreated = 0 # flag to show that the case is already created

class cfMeshDialog(QMainWindow):
    def __init__(self, ):
        super().__init__()
        uic.loadUi("cfMeshDialog.ui", self)
        self.setWindowTitle("cfMesh GUI")
        self.prepare_vtk()
        self.prepare_events()
        self.prepare_subWindows()
    
    def __del__(self):
        pass

    # manage sub windows
    def prepare_subWindows(self):
        self.createCaseWindow = None

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
        self.action_CreateProject.triggered.connect(self.createCase)
 
    def updateStatusBar(self,message="Go!"):
        self.statusbar.showMessage(message)

    def surfaceChosen(self):
        item = self.listSurfaceList.currentItem()
        print(item.text())   

    def createCase(self):
        #print("Creating Case...")
        #if(self.createCaseWindow==None):
        self.createCaseWindow = createCase()
        self.createCaseWindow.show()  
        global caseCreated
        global caseName, caseDirectoryPath
        if(caseName is not None and caseDirectoryPath is not None):
            caseCreated = 1 # set the case created flag


    # this function will read STL file and show it in the VTK renderer
    def showSTL(self,stlFile=r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        # Read stl
        try:
            self.reader = vtk.vtkSTLReader()
            self.reader.SetFileName(stlFile)
            self.render3D()
        except:
            print("Reading STL not successful. Try again")
        
        
    def render3D(self):  # self.ren and self.iren must be used. other variables are local variables
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("SlateGray"))
        self.ren.AddActor(actor)
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        camera = vtk.vtkCamera()
        camera.SetPosition(0, 1, 0)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        camera.Azimuth(30)
        camera.Elevation(30)
        self.ren.SetActiveCamera(camera)
        self.ren.ResetCamera()
        self.ren.ResetCameraClippingRange()
        #renWin.Render()
        self.iren.Start()

    def loadSTL(self,stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        self.updateStatusBar("Loading STL file")
        #stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"
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
            #print("Current STL File: ",fname)
            return fname

    def copySTL(self,stlFileName):
        if(caseCreated and os.getcwd()!=caseDirectoryPath):
            try:
                os.chdir(caseDirectoryPath)
            except:
                print("Error changing directory..")
        stlFileOnly = foamCLI.extractFileName(stlFileName)
        dst_file = os.getcwd()+"/constant/triSurface/"+stlFileOnly
        try:
            shutil.copy(src=stlFileName,dst=dst_file)
            return dst_file
        except:
            print("File copy failed..")
            return -1
        
    def importFile(self,startLocation="c:\\",fileType="*.brep *.igs *.iges"):
        fname,ftype = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"CAD files (*.brep *.igs *.iges)")
        if(fname==""):
            return -1 # CAD file not loaded
        else:
            print("Current CAD File: ",fname)
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
            print("Copying stl file")
            stl = self.copySTL(stlFileName=stlFileName)
            if(stl!=-1):
                self.showSTL(stlFile=stl)
                self.loadSTL(stlFile=stl)

    def splitSurfaces(self):
        self.updateStatusBar("Spliting surfaces")

    def importCAD(self):
        cadFileName = self.openCADDialog()
        if(cadFileName==-1):
            pass #print("CAD file not found...")
        else:
            self.updateStatusBar("CAD File imported: "+cadFileName)

    def defineBackgroundDomain(self):
        self.updateStatusBar("Creating background domain")

    def createMesh(self):
        print("Creating Cartesian Mesh...")

class createCase(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("createCaseDialog.ui", self)
        self.setWindowTitle("Create OpenFOAM Case")
        self.caseDirectoryPath = None
        self.caseName = None
        self.prepare_events()

    def __del__(self):
        pass #print("Exiting")

    def prepare_events(self):
        # Initiate the button click maps
        self.pushButtonCreate.clicked.connect(self.createACase)
        self.pushButtonCancel.clicked.connect(self.cancel)
        self.pushButtonOpen.clicked.connect(self.OpenPath)

    # Events
    def createACase(self):
        self.caseName = self.textEditCaseName.toPlainText()
        self.caseDirectoryPath = self.textEditCasePath.toPlainText()
        
        if(self.caseName=="" ):
            print("Error... Case name required.")
        elif(self.caseDirectoryPath==""):
            print("Error... Case directory path required.")
        else:
            print("Created case: ",self.caseName)
            print("Case Directory: ",self.caseDirectoryPath)
            global caseName 
            caseName = self.caseName
            global caseDirectoryPath 
            caseDirectoryPath = self.caseDirectoryPath
            aFoamCase = foamCase()
            aFoamCase.createCase(caseName=caseName,casePath=caseDirectoryPath)
            aFoamCase.createSystem()
            self.close()
        return 1
    
    def cancel(self):
        #print("Closing create case directory dialog")
        self.close()
        return 0

    def OpenPath(self):
        tmpPath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if(tmpPath!=""):
            #self.caseDirectoryPath = tmpPath
            self.textEditCasePath.setPlainText(tmpPath)
        else:
            pass
    
def main():
    app = QApplication(sys.argv)
    mainWindow = cfMeshDialog()
    mainWindow.show()  
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing")


def testCreateCase():
    app = QApplication(sys.argv)
    createCaseWindow = createCase()
    createCaseWindow.show() 
    try:
        sys.exit(app.exec_())
        
    except SystemExit:
        pass
    global caseName
    global caseDirectoryPath
    #print(caseName,caseDirectoryPath)
    

if __name__ == '__main__':
    main()
    #testCreateCase()
    

