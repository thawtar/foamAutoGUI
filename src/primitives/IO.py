# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# The main purpose of this module is to generate default values for various dictionary
# files. These values will be updated in the GUI.

import sys
import yaml
import json

# To print all items in a list line by line.
def printLineByLine(data):
    for anItem in data:
        print(anItem)


# Read YAML setting file
def readYAML(fileName="control.yaml"):
    print("Reading file: ",fileName)
    try:
        with open(fileName) as file:
            data = yaml.safe_load(file)
            print(data)
            return data
    except Exception as e:
        print("Exception occurred while loading YAML...", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

def writeYAML(data={"a":1,"b":2},fileName="control2.yaml"):
    try:
        with open(fileName, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        print("Exception occurred while writing YAML...", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

def readJSON(fileName="control.json"):
    print("Reading file: ",fileName)
    try:
        with open(fileName) as json_file:
            data = json.load(json_file)
            #print(data)
            return data
    except Exception as e:
        print("Exception occurred while loading JSON...", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

def writeJSON(data={"a":1,"b":2},fileName="control2.json"):
    try:
        with open(fileName, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print("Exception occurred while writing JSON...", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

# This function will read all the contents in a file and store the lines in a list.
# This will reduce the hustle of having to write try-except brackets everytime.
# However, this is not recommended for very large files (CFD mesh or result fields) because
# it will fill the RAM in no time.
def readFile(fileName="aFile"):
    data = []
    try:
        f = open(fileName,"r")
        for x in f:
            x = x[:-1] # skip the last letter in each line because it is a newline symbol
            data.append(x)
        f.close()
    except:
        print("Error while opening file: ",fileName)
    if(len(data)>0):
        return data
    else:
        return -1
    

def clearComments(data=["//asdf","24t34","/*this is start","end of a comment*/"," restart the body"]):
    clearData = []
    isInsideComments = 0 # flag to mark lines inside long comments
    isItComment = 0 # to mark current line is a comment
    
    for x in data:
        #print(x[0:2],x[-2:])
        isItComment = 0 # the default assumption is the current line is not a comment
        if(x=="\n" or x==""  or x=="\t\n"): # if the line is a blank line
            continue
        if(x[0:2]=="//"):
            isItComment = 1
        if(x[0:2]=="/*"):
            isInsideComments=1
        if(isInsideComments==1 and x[-2:]=="*/"):
            isInsideComments=0
            continue
        if(not isItComment and not isInsideComments):
            clearData.append(x)
    return clearData
    

def read_boundary(file="c:/Users/mrtha/Desktop/GitHub/foamAutoGUI/src/primitives/boundary"):
    data = readFile(fileName=file)
    clearData = clearComments(data)
    clearData = clearData[8:]
    printLineByLine(clearData)
    

# This function reads STL file and extracts the surface patch names.
def readSTL(stlFileName="cylinder.stl"):
    surfaces = [] # to store the surfaces in the STL file
    try:
        f = open(stlFileName, "r")
        for x in f:
            
            items = x.split(" ")
            if(items[0]=='solid'):
                surfaces.append(items[1][:-1])
                #print(items[1][:-1])
        f.close()
    except:
        print("Error while opening file: ",stlFileName)
    return surfaces
    

#data = readSTL("c:/Users/mrtha/Desktop/GitHub/foamAutoGUI/src/primitives/cylinderBox.stl")
#print(data)
while(1):
    boundaryFile = input("Enter a boundary file: ")
    read_boundary(file=boundaryFile)
#clearComments()   



data = {"castellatedMesh":"true","snap":"true","addLayers":"true",
"geometry":[{"pipe.stl":{"type":"triSurfaceMesh"}},{"refinementBox":{"type":"box","min":"0.4 0.25 0.65","max":"0.8 0.75 1.35"}}],
"castellatedMeshControls":{"maxLocalCells":20000, "maxGlobalCells":5000}}

#obj = readYAML(fileName="controlYAML.yaml")
#writeJSON(data=data,fileName="snappyJSON.json")
#obj = readJSON(fileName="myJSON.json")
#print("Writing yaml data file")
#writeYAML(data=data,fileName="snappyYAML.yaml")
