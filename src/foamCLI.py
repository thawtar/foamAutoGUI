# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

#from typing import IO
#from email.headerregistry import ContentDispositionHeader
import primitives.IO as IO
import primitives.defaultValues as df
import sys
import os

insideOpenFOAMCase = 0

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
    global insideOpenFOAMCase
    insideOpenFOAMCase = 1
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
    filePath = "./system/controlDict"
    data = df.generateControlDictData()
    text = createFoamHeader(itemClass="dictionary",object="controlDict")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile=filePath)
    

def fvSchemesTest():
    filePath = "./system/fvSchemes"
    data = df.generateFvSchemesData()
    text = createFoamHeader(itemClass="dictionary",object="fvSchemes")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile=filePath)
    

def fvSolutionsTest():
    filePath = "./system/fvSolution"
    data = df.generateFvSolutionData()
    text = createFoamHeader(itemClass="dictionary",object="fvSolution")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile=filePath)
    

def snappyTest():
    filePath = "./system/snappyHexMesh"
    data = df.generateSnappyHexMeshData()
    text = createFoamHeader(itemClass="dictionary",object="snappyHexMeshDict")
    text = text+dictDataToText(data=data)
    writeDictFile(data=text,dictFile=filePath)


def testCreateCase():
    controlDictTest()
    fvSchemesTest()
    fvSolutionsTest()
    snappyTest()
    




"""
==========================================================
                    SOLVER CHOOSER
==========================================================
We have a 5-bit number to represent our solver: 00000
1st bit: steady or transient (Dec: 16)
2nd bit: incompressible or compressible (Dec: 8)
3rd bit: single phase or multiphase (Dec: 4)
4th bit: energy off or energy on (Dec: 2)
5th bit: turbulence off or turbulence on (Dec: 1)

Steady, incompressible, no energy, single phase = 00000 or 00001 (simpleFoam)
Steady, incompressible, energy, single phase = 00100 or 00101 (buoyantBoussinesqSimpleFoam)
Steady, incompressible, no energy, multiphase = 00010 or 00011 (interLTSFoam)
Steady, compressible, energy, single phase = 01100 or 01101 (rhoSimpleFoam)
Transient, incompressible, no energy, single phase = 10000 or 10001 (pimpleFoam)
Transient, incompressible, energy, single phase = 10100 or 10101 (buoyantBoussinesqPimpleFoam)
Transient, incompressible, no energy, multiphase = 10010 or 10011 (interFoam)
Transient, compressible, energy, single phase = 11100 or 11101 (rhoPimpleFoam)
"""

simpleFoam = int('0b00000',2)
buoyantBoussinesqSimpleFoam = int('0b00100',2)
interLTSFoam = int('0b00010',2)
rhoSimpleFoam = int('0b01100',2)
rhoPimpleFoam = int('0b11100',2)
pimpleFoam = int('0b10000',2)
buoyantBoussinesqPimpleFoam = int('0b10100',2)
interFoam = int('0b10010',2)

# turbulent versions of the above solvers
turbSimpleFoam = int('0b00001',2)
turbbBuoyantBoussinesqSimpleFoam = int('0b00101',2)
turbInterLTSFoam = int('0b00011',2)
turbRhoSimpleFoam = int('0b01101',2)
turbRhoPimpleFoam = int('0b11101',2)
turbPimpleFoam = int('0b10001',2)
turbBuoyantBoussinesqPimpleFoam = int('0b10101',2)
turbInterFoam = int('0b10011',2)


solvers ={simpleFoam:"simpleFoam",turbSimpleFoam:"simpleFoam",buoyantBoussinesqSimpleFoam:"buoyantBoussinesqSimpleFoam",
          turbbBuoyantBoussinesqSimpleFoam:"buoyantBoussinesqSimpleFoam",buoyantBoussinesqPimpleFoam:"buoyantBoussinesqPimpleFoam",
          turbBuoyantBoussinesqPimpleFoam:"buoyantBoussinesqPimpleFoam",turbInterLTSFoam:"interLTSFoam",interLTSFoam:"interLTSFoam",
          pimpleFoam:"pimpleFoam",turbPimpleFoam:"pimpleFoam",interFoam:"interFoam",turbInterFoam:"interFoam",
          rhoSimpleFoam:"rhoSimpleFoam",turbRhoSimpleFoam:"rhoSimpleFoam",rhoPimpleFoam:"rhoPimpleFoam",
          turbRhoPimpleFoam:"turbRhoPimpleFoam"}


def computeSolverKey(physicsData):
    transient,compressible,energy,multiphase,turbulence=physicsData
    if(transient):
        transient = 16
    if(compressible):
        compressible = 8
    if(energy):
        energy = 4
    if(multiphase):
        multiphase = 2
    if(turbulence):
        turbulence = 1 # is it even necessary?
    solverKey = transient|compressible|energy|multiphase|turbulence
    return solverKey

def test():
    transient = 0       # 0 means steady. if 1, transient
    compressible = 0    # 0 means incompressible. If 1, compressible
    energy = 0          # 0 means no energy equation. If 1, energy is considered
    multiphase = 0      # 0 means single phase. If 1, multiphase is considered
    turbulence = 0      # 0 means laminar. If 1, turbulence modeling used

    trans = input("Transient?[Y/n]")
    comp = input("Compressible?[Y/n]")
    en = input("Energy equation?[Y/n]")
    mphase=input("Multiphase?[Y/n]")
    turb = input("Turbulence modeling?[Y/n]")
    if(trans=="Y"):
        transient = 1
    if(comp=="Y"):
        compressible=1
        energy = 1 # compressible flows need energy term on. This will overwrite the energy on input
    if(en=="Y"):
        energy = 1
    if(mphase=="Y"):
        multiphase=1
    if(turb=="Y"):
        turbulence=1
    data = (transient,compressible,energy,multiphase,turbulence)
    solverKey = computeSolverKey(physicsData=data)
    print(solverKey)
    if(solverKey not in solvers.keys()):
        print("Error... No solver found. Exiting...")
        exit(-1)
    print("Solver: ",solvers[solverKey])


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