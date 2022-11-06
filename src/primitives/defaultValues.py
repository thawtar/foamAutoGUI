# Copyright (C) 2022 by Thaw Tar. All rights reserved.
#
# Developed at Zoro-CAE Solutions Inc. 
# Permission to use, copy, modify, and distribute this
# software is freely granted, provided that this notice 
# is preserved.

# The main purpose of this module is to generate default values for various dictionary
# files. These values will be updated in the GUI.


def generateSnappyHexMeshData(): # to generate default values for snappyHexMesh
    mainControls = {"castellatedMesh":"true","snap":"false","addLayers":"false"}
    geometry = {"geometry":[{"pipe.stl":{"type":"triSurfaceMesh"}},{"refinementBox":{"type":"box","min":"0.4 0.25 0.65","max":"0.8 0.75 1.35"}}],}
    castellatedMeshControls = {"castellatedMeshControls":{"maxLocalCells":20000, "maxGlobalCells":5000,"minRefinementCells":1,
    "maxLoadUnbalance":0.10,"nCellsBetweenLevels":3,"refinementSurfaces":[],"resolveFeatureAngle":30,
    "refinementRegions":[],"locationInMesh":"(0 0 0)","allowFreeStandingZoneFaces":"true"}}
    snapControls = {"snapControls":{"noSmoothPatch":5,"tolerance":2.0,"nSolveIter":50,"nRelaxiter":7, "nFeatureSnapIter":15,
    "implicitFeatureSnap":"false","explicitFeatureSnap":"true","multiRegionFeatureSnap":"false"}}
    addLayersControls = {"addLayerControls":{"relativeSizes":"true","layers":[],"expansionRatio":1.15, "finalLayerThickenss":0.3,
    "minThickness":0.1,"nGrow":0,"featurAngle":60,"slipFeatureAngle":30,"nRelaxIter":3,"nSmoothSurfaceNormals":1,
    "nSmoothThickness":10,"maxFaceThicknessRatio":0.5,"maxThicknessToMedialRatio":0.3,"minMedialAxisAngle":90,
    "nBufferCellsNoExtrude":0,"nLayerIter":50}}
    meshQualityControls = {}

    snappyHexMeshDict = {}
    snappyHexMeshDict.update(mainControls)
    snappyHexMeshDict.update(geometry)
    snappyHexMeshDict.update(castellatedMeshControls)
    snappyHexMeshDict.update(snapControls)
    snappyHexMeshDict.update(addLayersControls)
    #snappyHexMeshDict.update(meshQualityControls)
    return snappyHexMeshDict

def generateControlDictData():
    controlData={"application":"simpleFoam"}
    timeControls={"startFrom":"startTime","startTime":0,"stopAt":"endTime",
    "endTime":10,"deltaT":1,"timeFormat":"general","timePrecision":6,
    "runTimeModifiable":"true"}
    writeControls={"witeControl":"timeStep","writeInterval":1,"purgeWrite":5,
    "writeFormat":"ascii","writePrecision":6,"writeCompression":"off"}
    controlData.update(timeControls)
    controlData.update(writeControls)
    return controlData

def generateFvSchemesData():
    ddt = {"ddtSchemes":{"default":"Euler"}}
    grad = {"gradSchemes":{"default":"Gauss linear"}}
    div = {"divSchemes":{"default":"none", "div(phi,U)":"bounded Gauss upwind"}}
    lap = {"laplacianSchemes":{"default":"Gauss linear orthogonal"}}
    inter={"interpolationSchemes":{"default":"linear"}}
    snGra={"snGradSchemes":{"default":"corrected"}}
    schemes = {}
    schemes.update(ddt)
    schemes.update(grad)
    schemes.update(div)
    schemes.update(lap)
    schemes.update(inter)
    schemes.update(snGra)
    return schemes


def generateFvSolutionData():
    p = {"p":{"solver":"PCG","preconditioner":"DIC","tolerance":1e-06,"relTol":0}}
    p_Final = {"pFinal":{"solver":"PCG","preconditioner":"DIC","tolerance":1e-06,"relTol":0}}
    U = {"U":{"solver":"smoothSolver","smoother":"symGaussSeidel","tolerance":1e-5,"relTol":0}}
    U_Final = {"UFinal":{"solver":"smoothSolver","smoother":"symGaussSeidel","tolerance":1e-5,"relTol":0}}
    PISO = {"PISO":{"nCorrectors":2,"nNonOrthogonalCorrectors":0,"pRefCell":0,"pRefValue":0}}
    fvSolution = {}
    solvers = {"solvers":[p,p_Final,U,U_Final]}
    
    fvSolution.update(solvers)
    fvSolution.update(PISO)
    return fvSolution



    


# default values should be used when the value of an item in the dictionary is -1
def setDefaultValues(inputDictionary,defaultDictionary): # inputs are dictionaries
    inputKeys = inputDictionary.keys()
    defaultKeys = defaultDictionary.keys()
    for aKey in inputKeys:
        if(inputDictionary[aKey]==-1): # we need to replace the value with a default value
            # first, check the default dictionary whether it has the required key
            if(aKey in defaultKeys):
                # then replace it
                inputDictionary[aKey] = defaultDictionary[aKey]
            else:
                print("Necessary key not found in dictionary... Exiting..")
                exit(-1)
    return inputDictionary


def test():
    print(generateControlDictData())
    print()
    print(generateSnappyHexMeshData())
    print()
    print(generateFvSchemesData())
    