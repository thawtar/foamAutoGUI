import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
import primitives.IO as IO

class cfMeshDialog(QMainWindow):
    def __init__(self, ):
        super().__init__()
        uic.loadUi("cfMeshDialog.ui", self)
        self.setWindowTitle("cfMesh GUI")
        self.pushButtonSTLImport.clicked.connect(self.loadSTL)
        self.pushButtonCreateMesh.clicked.connect(self.createMesh)
        self.listSurfaceList.clicked.connect(self.surfaceChosen)

    def surfaceChosen(self):
        item = self.listSurfaceList.currentItem()
        print(item.text())
        
    
    def loadSTL(self):
        print("Loading STL file")
        stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\primitives\cylinderBox.stl"
        surfaces=IO.readSTL(stlFileName=stlFile)
        print(surfaces)
        for (i,aSurface) in enumerate(surfaces):
            self.listSurfaceList.insertItem(i,aSurface)
        
        

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

