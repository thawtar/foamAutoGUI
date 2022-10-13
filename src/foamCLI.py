# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# This code is the command line implementation to create OpenFOAM case files from GUI input
# Only core operations are included here.
# Therefore, there is no import libraries.

#from typing import IO
from email.headerregistry import ContentDispositionHeader
import primitives.IO as IO
import primitives.defaultValues as df
import sys
import os


#Primitives
#IO
def writeDictFile(data="",dictFile="blockMesh"):
    try:
        f=open(dictFile,mode='w')
        try:
            f.write(data)
        except:
            print("Something went wrong when writing to the file "+dictFile)
        finally:
            f.close()
    except:
        print(dictFile+" already open. Please close it and retry.")
        print("Exiting...")
        exit(-1)


# to create a case inside a directed path.
def createCaseDirectory(caseDir="/casePath",caseName="testCase"):
    print("Creating Case Directory...")
    try:
        os.chdir(caseDir)
    except:
        print("Error entering the path... Check the path again")
        print("Exiting...")
        exit(-1)
    pwd = os.getcwd()
    caseFullPath = pwd+caseName+"/"
    try:
        os.mkdir(caseFullPath)
    except:
        print("Error creating directory")
        exit(-1)
    # Create OpenFOAM default directories 0, constant, system
    

# add "toAdd" to main text "text"
def addText(text,toAdd="a"):
    text = text + "\n" + toAdd
    return text

# add an item to the main text "text"
def addItem(text,itemName,value,tab=0):
    tabs = "\t"*tab
    data=tabs+itemName+" "+str(value)+";"
    text=addText(text=text,toAdd=data)
    return text

# Dictionary structure should be like this. 
# Keywords are OpenFOAM dictionary keywords such as "castellatedMesh".
# Values are -1 for default values and other values for modified ones.
# If value equals -1, we will put default values to it.
# Eg. snappyHexSteps = ["castellatedMesh":"-1","snap":"true","addLayers":"false"]
def addItemGroup(data,defaultValues,tab=0):
    keywords = data.keys()
    output = ""
    if(len(keywords)==0):
        return output # if the group is empty, just return no text
    for anItem in keywords:
        if(data[anItem]==-1): # if it is default values, 
            itemValue = defaultValues[anItem] # just put default value into it
        else:
            itemValue = data[anItem]
        output=addItem(text=output,itemName=anItem,value=itemValue,tab=tab)
    return output

def addDictionary(name,data,defaultValues):
    dataGroup = addItemGroup(data=data,defaultValues=defaultValues,tab=1)
    dict = name+"\n{"+dataGroup+"\n}\n"
    return dict

def addFunctionObjects(functionObjectSwitches):
    # functionObjectSwitches contains whether certain function objects
    # will be added or not
    keys = functionObjectSwitches.keys()
    values = functionObjectSwitches.values()
    output = "\nfunctions{\n"
    functionList = ""
    for aKey in keys:
        if(functionObjectSwitches[aKey]):
            functionName = "\t#includeFunc\t"+"\""+aKey+"\""
            functionList = addText(functionList,toAdd=functionName)
    output = "\nfunctions{\n"+functionList+"\n}"
    print(output)
    return output

# create header of each file
#def createFoamHeader(itemClass="dictionary",object="surf"):
#    output = "FoamFile {\nversion 2.0;\nformat ascii;\nclass "
#    output = output+itemClass+";\nobject "+object+";\n}\n"
#    return output

def createFoamHeader(itemClass="dictionary",object="surf"):
    dict = {"version":"2.0","format":"ascii"}
    dict["class"] = itemClass
    dict["object"]= object
    output=addDictionary(name="FoamFile",data=dict,defaultValues=dict)
    return output
#=============================================================
# Create the setting files for OpenFOAM
# Create Control dict
def createControlDict(controlData,defaultValues,funcObj):
    foamHeader = createFoamHeader(itemClass="dictionary",object="controlDict")
    data = addItemGroup(data=controlData,defaultValues=defaultValues)
    if(funcObj!=-1): # -1 is there is no function objects flag
        functionObj = addFunctionObjects(functionObjectSwitches=funcObj)
        output = foamHeader+data+functionObj
    else:
        output = foamHeader+data
    print(output)
    return output
    #writeDictFile(data=controlData,dictFile="controlDict")




# To create surfaceExtractDict
def createSurfaceFeatureExtractDict(stlName="stlFile.stl",includedAngle=180):
    output=createFoamHeader(itemClass="dictionary",object="surfaceFeatureExtractDict")
    output=output+"\n"+stlName+"{\nextractionMethod extractFromSurface;\n"
    output=output+"includedAngle "+str(includedAngle)+";\nsubsetFeatures\n{nonManifoldEdges no;"
    output=output+"\nopenEdges yes;}\nwriteObj yes;}"
    return output
    #writeDict(data=output,dictFile="surfaceFeatureExtractDict")


def createSnappyHexDict(snappyData): 
    foamHeader = createFoamHeader(itemClass="dictionary",object="snappyHexMeshDict")
    (mainSteps, geometry, castellatedControls, snapControls, addLayerControls, meshQualityControls)=snappyData 
    #just unzip the tuple containing a lot of snappyHexMesh data
    mainSteps = addItemGroup(data=mainSteps,defaultValues=mainSteps)
    geometry = addDictionary(name="geometry",data=geometry,defaultValues=geometry)
    castellatedControls=addDictionary(name="castellatedMeshControls",data=castellatedControls,defaultValues=castellatedControls)
    snapControls=addDictionary(name="snapControls",data=snapControls,defaultValues=snapControls)
    addLayerControls=addDictionary(name="addLayersControls",data=addLayerControls,defaultValues=addLayerControls)
    meshQualityControls=addDictionary(name="meshQualityControls",data=meshQualityControls,defaultValues=meshQualityControls)
    mergeTolerance = addItem(text="",itemName="mergeTolerance",value=1.0e-6)
    snappyHexData = foamHeader+mainSteps+geometry+castellatedControls+snapControls
    snappyHexData = snappyHexData+addLayerControls+meshQualityControls+mergeTolerance
    print(snappyHexData)

def createBox(name,minPoint,maxPoint):
    data = {"type":"searchableBox"}
    data["min"] = "("+str(minPoint[0])+" "+str(minPoint[1])+" "+str(minPoint[2])+")"
    data["max"] = "("+str(maxPoint[0])+" "+str(maxPoint[1])+" "+str(maxPoint[2])+")"
    output=addDictionary(name=name,data=data,defaultValues=data)
    return output

def createCone(name,inputData):
    (point1, point2, radius1,radius2,innerRadius1,innerRadius2)=inputData
    data = {"type":"searchableCone","radius1":radius1,"radius2":radius2,
    "innerRadius1":innerRadius1,"innerRadius2":innerRadius2}
    data["point1"] = "("+str(point1[0])+" "+str(point1[1])+" "+str(point1[2])+")"
    data["point2"] = "("+str(point2[0])+" "+str(point2[1])+" "+str(point2[2])+")"
    output=addDictionary(name=name,data=data,defaultValues=data)
    return output

def createSphere(name,centre, radius):
    (x,y,z) = centre
    centre = "("+str(centre[0])+" "+str(centre[1]+" "+str(centre[2]))+")"
    data = {"type":"searchableSphere"}
    data["centre"] = centre
    data["radius"] = radius
    output = addDictionary(name=name,data=data,defaultValues=data)


def createFvSchemes(schemes):
    foamHeader = createFoamHeader(itemClass="dictionary",object="fvSchemes")
    (ddtS, gradS, divS, laplacianS, interpolationS,snGradS) = schemes # this tuple contains data about numerical schemes to be used
    ddt = addDictionary("ddtSchemes",ddtS,ddtS)
    grad= addDictionary("gradSchemes",gradS,gradS)
    div = addDictionary("divSchemes",divS,divS)
    lap = addDictionary("laplacianSchemes",laplacianS,laplacianS)
    inter=addDictionary("interPolationSchemes",interpolationS,interpolationS)
    snG = addDictionary("snGradSchemes",snGradS,snGradS)
    output=foamHeader+ddt+grad+div+lap+inter+snG
    return output

def fvSchemeTest():
    ddt = {"default":"Euler"}
    grad = {"default":"Gauss linear"}
    div = {"default":"none", "div(phi,U)":"bounded Gauss upwind"}
    lap = {"default":"Gauss linear orthogonal"}
    inter={"default":"linear"}
    snGra={"default":"corrected"}
    schemes = (ddt,grad,div,lap,inter,snGra)
    output=createFvSchemes(schemes=schemes)
    writeDictFile(data=output,dictFile="fvSchemes")
    print(output)


def createFvSolutions():
    foamHeader = createFoamHeader(itemClass="dictionary",object="fvSolutions")

def controlDictTest():
    (data,dv) = getControlDictData()
    data["application"]="icoFoam"
    data["deltaT"]=0.005
    data["endTime"]=0.5
    cdict = createControlDict(controlData=data,defaultValues=data,funcObj=-1)
    writeDictFile(data=cdict,dictFile="controlDict")

def readJSN():
    data = IO.readJSON(fileName="snappyJSON.json")
    return data


def dictDataToText(data):
    keys = data.keys()
    values = data.values()
    text = ""
    for anItem in keys:
        # if the value is a nested dictionary, treat as a nested dictionary
        if(isinstance(data[anItem],dict)):
            text = text+"\n"+anItem +"\n{" +dictDataToText(data=data[anItem])+"\n}"
        # if the value is a list of multiple dictionaries, loop on the list, treat each dictionary
        elif(isinstance(data[anItem],list)):
            # first, add the name of the object
            text = text+"\n" +anItem +"{"
            for i in data[anItem]:
                #text = text+"\n"+i
                if(isinstance(i,dict)):
                    #text = text+"\n" + dictDataToText(data=i)
                    dictName = list(i.keys())[0]# the name of the sub dictionary
                    
                    #text = text+"\n"+str(dictName) +"\n{" +dictDataToText(data=i)+"\n}"
                    text = text+dictDataToText(data=i)
                #else:
                #    text = text+"\n" + str(i)
            text = text +"}\n"
        # othewise, it would be a value. add as a value.
        else:
            text = text+"\n"+anItem+" " + str(data[anItem])+";"
    #print(text)
    return text
    #print(keys)
    #print(values)


def controlDictTest():
    data = df.generateControlDictData()
    print(data)
    text = createFoamHeader(itemClass="dictionary",object="controlDict")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile="controlDict")
    print(text)

def fvSchemesTest():
    data = df.generateFvSchemesData()
    print(data)
    text = createFoamHeader(itemClass="dictionary",object="fvSchemes")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile="fvSchemes")
    print(text)

def fvSolutionsTest():
    data = df.generateFvSolutionData()
    print(data)
    text = createFoamHeader(itemClass="dictionary",object="fvSolution")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile="fvSolution")
    print(text)

def snappyTest():
    data = df.generateSnappyHexMeshData()
    print(data)
    text = createFoamHeader(itemClass="dictionary",object="snappyHexMeshDict")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile="snappyHexMeshDict")
    print(text)

#controlDictTest()
#fvSchemesTest()
snappyTest()
#fvSolutionsTest()
#=============================================================
"""******************************************************
snappyHexMeshDict variables
******************************************************"""



#(c,d) = getControlDictData()
#fvSchemeTest()
#controlDictTest()


#functionObjList = {"sample":1,"forces":0,"wallShearStress":1}
#createControlDict(c,d,functionObjList)
#addFunctionObjects(functionObjectSwitches=functionObjList)