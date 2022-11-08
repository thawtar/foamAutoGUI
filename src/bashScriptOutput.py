import os, sys

def headerLogo():
    logo = "#"+ "*"*30+"\n#        FOAM AUTO\n#"+"*"*30+"\n\n"
    return logo

def bashHeader():
    return "#!/bin/sh"

def source_file(of_path="/home/user/OpenFOAM",fileName="bashrc"):
    of_bashrc = os.path.join(of_path,fileName)
    if(os.path.exists(of_bashrc)):
        return "\nsource "+of_bashrc
    else:
        return -1

def run_of_application(of_application="blockMesh",args=""):
    return "\nrunApplication "+of_application+args

def run_parallel(of_application="snappyHexMesh",args=""):
    return "\nrunParallel " + of_application + args

def restore_0_dir():
    return "\nrestore0Dir"

def main():
    print("Hello")
    print(source_file("C:/Users/owner/Desktop/","bashScriptOutput.py"))
    script = headerLogo()+bashHeader()+run_of_application()+run_of_application("decomposePar")+run_parallel("snappyHexMesh")
    print(script)

if __name__=="__main__":
    main()