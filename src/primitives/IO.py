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


def read_boundary(file="boundary"):
    try:
        f = open(file,"r")
    except:
        print("Error while opening file: ",file)
    



data = {"castellatedMesh":"true","snap":"true","addLayers":"true",
"geometry":[{"pipe.stl":{"type":"triSurfaceMesh"}},{"refinementBox":{"type":"box","min":"0.4 0.25 0.65","max":"0.8 0.75 1.35"}}],
"castellatedMeshControls":{"maxLocalCells":20000, "maxGlobalCells":5000}}

#obj = readYAML(fileName="controlYAML.yaml")
#writeJSON(data=data,fileName="snappyJSON.json")
#obj = readJSON(fileName="myJSON.json")
#print("Writing yaml data file")
#writeYAML(data=data,fileName="snappyYAML.yaml")
