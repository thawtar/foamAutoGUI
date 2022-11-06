# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# This code is the command line implementation to create OpenFOAM case files from GUI input
# Only core operations are included here.
# Therefore, there is no import libraries.

import os
from foamCLI import *


class foamCase():
    def __init__(self) -> None:
        self.caseDirectory = "" # the absolute path of the OpenFOAM case
        self.isInCaseDirectory = 0 # The flag to confirm whether current path is in OpenFOAM case
        self.caseName = ""
        self.originalDirectory=os.getcwd() # to store current directory at the start of the program
        self.dir_0 = "0"
        self.dir_constant = "constant"
        self.dir_system = "system"
        self.dir_triSurface = "constant/triSurface"
        self.caseCreated = 0

    # this function returns 0 if directory already exists, -1 if there is error, 1 if successful
    def createDirectory(self,directory):
        if(os.path.exists(directory)):
            print("Directory already exists.. Skipping")
            return 0
        else:
            try:
                os.makedirs(directory) # this will make intermediate directories too
                return 1
            except:
                print("Error creating directory...")
                return -1
        
    
    def setDirectory(self,casePath):
        self.caseDirectory=casePath

    def createCase(self,casePath,caseName):
        self.caseDirectory = os.path.join(casePath,caseName)
        print("Case Directory: ",self.caseDirectory)
        status = self.createDirectory(self.caseDirectory)
        self.caseName = caseName
        
        # to create the case directory,
        
        self.dir_0 = os.path.join(self.caseDirectory,self.dir_0)
        self.dir_constant = os.path.join(self.caseDirectory,self.dir_constant)
        self.dir_system = os.path.join(self.caseDirectory,self.dir_system)
        try:
            os.chdir(self.caseDirectory)
            self.isInCaseDirectory = 1 # Set the flag
        except:
            print("Error changing to directed directory...")
            exit(-1)
        # After changing the path to case directory, create the directories
        try:
            self.createDirectory(self.dir_0)
            self.createDirectory(self.dir_constant)
            self.createDirectory(self.dir_system)
            self.createDirectory(self.dir_triSurface)
            self.caseCreated = 1
            #os.mkdir(dir_0)
            #os.mkdir(dir_constant)
            #os.mkdir(dir_system)
        except:
            print("Error creating case directories for 0, constant and system...")
            exit(-1)
        print("Creating directory successful...")

    def createSystem(self):
        if(self.isInCaseDirectory):
            createBlockMeshDict()
            createControlDict()
            createfvSchemesDict()
            createfvSolutionDict()
            createSnappyHexMeshDict()


#def main():
#    aCase = foamCase()
#    casePath = r"C:\Users\mrtha\Desktop"
#    caseName = "test1"
#    aCase.createCase(casePath=casePath,caseName=caseName)


#if __name__=="__main__":
#    main()


    



