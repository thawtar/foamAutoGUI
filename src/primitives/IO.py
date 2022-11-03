# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# The main purpose of this module is provide fundamental IO functionalities to deal with 
# OpenFOAM files. This includes definition of default values which will be updated in the GUI.

import sys
import yaml
import json

# To print all items in a list line by line.
def printLineByLine(data):
    for anItem in data:
        print(anItem)

# To print nested dictionaries with keys in a easy to view manner. Useful for data visualization
def printDictionary(aDictionary={"asdf":2}):
    keys = aDictionary.keys()
    for anItem in keys:
        if(isinstance(aDictionary[anItem],dict)):
            print()
            print(anItem)
            printDictionary(aDictionary=aDictionary[anItem])
        else:
            print(anItem,aDictionary[anItem])
        

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

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
    

testBoundary = ['    movingWall', '    {', '        type            wall;',
 '        inGroups        1(wall);', '        nFaces          20;',
  '        startFace       760;', '    }', '    fixedWalls',
   '    {', '        type            wall;', '        inGroups        1(wall);', '        nFaces          60;', '        startFace       780;', '    }', '    frontAndBack', '    {', '        type            empty;', '        inGroups        1(empty);', '        nFaces          800;', '        startFace       840;', '    }'] 

# TODO: Read dictionary data and put all these contents to a list of dictionaries.
# This function reads the RAW dictionary data and creats a dictionary based on it.
# Can be used for ALL general purpose OpenFOAM dictionaries WITHOUT NESTED dictionaries.
def read_dictionary(data=testBoundary):
    dictionaries = {} # To store the processed dictionary data.
    subDictionaries = {} # to store sub-dictionaries
    insideDictionary = 0 # Flag to mark whether currently inside a dictionary.
    #print(data)
    # A dictionary contains the dictionary header name, { } and contents inside it.
    # So, the idea is to find the header, each curly brackets and confirm that we are inside 
    # the dictionary. For the contents of OpenFOAM dictionary, there is key and value.
    # Thus, if there is TWO 
    for aData in data:
        dictionaryValue = []
        
        items = aData.split(" ")
        #print(items)
        for anItem in items:
            if(anItem!=""and anItem!="\n"):
                dictionaryValue.append(anItem)
        if(len(dictionaryValue)==1 and dictionaryValue[0]!="{" 
        and dictionaryValue[0]!="}"): # this must be the key of the dictionary
            key = dictionaryValue[0]
        if(dictionaryValue[0]=="{"): # this must be start of a dictionary
            insideDictionary = 1
        if(dictionaryValue[0]=="}"): # this must be the end of the dictionary
            insideDictionary = 0
            dictionaries[key]=subDictionaries # put data into main dictionary
            subDictionaries = {} # clear up the sub dictionaries
        # Check everything and put into dictionary
        if(insideDictionary and len(dictionaryValue)==2):
            subDictionaryValue = dictionaryValue[1][:-1] # remove the semicolon
            if(subDictionaryValue.isdigit()): # check whether an integer or not
                subDictionaryValue = int(subDictionaryValue)
            elif(isFloat(subDictionaryValue)): # then whether a float or not
                subDictionaryValue = float(subDictionaryValue)
            else:
                pass
            subDictionaries[dictionaryValue[0]]=subDictionaryValue
    if(len(dictionaries.keys())):
        return dictionaries
    return -1 # it has no dictionaries


# TODO: Read boundary file for boundary patches. Return a list of boundary dictionaries
def read_boundary(file="c:/Users/mrtha/Desktop/GitHub/foamAutoGUI/src/primitives/boundary"):
    data = readFile(fileName=file)
    if(data==-1):
        print("Error... No data found... Exiting")
        exit(-1)
    clearData = clearComments(data)
    clearData = clearData[8:]
    boundaryCount = 0
    #printLineByLine(clearData)
    # Check the number of patches
    if(clearData[0].isdigit()):
        boundaryCount = int(clearData[0])
    
    boundaryData = clearData[2:-1]
    print("boundaryCount:\t",boundaryCount)
    dictionariesFromBoundaryFile = read_dictionary(data=boundaryData)
    #printLineByLine(boundaryData)
    print(boundaryData)
    if(dictionariesFromBoundaryFile!=-1):
        print(dictionariesFromBoundaryFile)
        printDictionary(dictionariesFromBoundaryFile)


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
#while(1):
#    boundaryFile = input("Enter a boundary file: ")
#    read_boundary(file=boundaryFile)
#clearComments() 
#read_dictionary()  



data = {"castellatedMesh":"true","snap":"true","addLayers":"true",
"geometry":[{"pipe.stl":{"type":"triSurfaceMesh"}},{"refinementBox":{"type":"box","min":"0.4 0.25 0.65","max":"0.8 0.75 1.35"}}],
"castellatedMeshControls":{"maxLocalCells":20000, "maxGlobalCells":5000}}

#obj = readYAML(fileName="controlYAML.yaml")
#writeJSON(data=data,fileName="snappyJSON.json")
#obj = readJSON(fileName="myJSON.json")
#print("Writing yaml data file")
#writeYAML(data=data,fileName="snappyYAML.yaml")
