import hou, sys, os, glob
from os import listdir
from os.path import isfile, join

def getVersion(filename):
    versionString = filename.split("_")[-1] if filename.split("_")[-1].startswith("v") else ""
    version = versionString.split(".")[0]
    if len(version) != 0:
            version = int("".join(i for i in versionString if i.isdigit()))
    else:
            version = ""
    return version,versionString    
    
def parseFileName(filename):
    sceneFolder = hou.getenv("hip")  
    version = getVersion(filename)
    baseName = filename.rstrip(version[1]).rstrip("_")  
    #baseName = filename.rstrip("filename.split("_")-1
    print(f"""
    Scene Folder: {sceneFolder}
    Full Name: {filename}
    Base Name: {baseName}
    Version: {version[0]}
    """)

    if filename == "untitled":
       hou.ui.displayMessage("Your scene is currently untitled")
       sys.exit()     

    if version[0] == "":
        nov = hou.ui.displayMessage("No version detected. Add one?", buttons=('Yes','No'))
        if nov == 0:            
            saveScene(sceneFolder, baseName, version) 
            sys.exit()
        if nov == 1:
            sys.exit()
    return (filename, sceneFolder, baseName, version)    

def findOtherVersions(sceneName):
    versions = []
    hipDir = hou.getenv('hip')
    hipFiles = list(glob.glob(f"{hipDir}*/*{sceneName}_*.hip"))
    print(f"Found Versions in {hipDir}:")
    for file in hipFiles:
        ext = os.path.splitext(file)[1]
        if ext == ".hip":
            filename = os.path.split(file)[1]
            print(f" {filename}")
            versions.append(filename)
    return versions

def saveScene(shotFolder, sceneName, version):
    newHipname = f"{sceneName}_v{format(int(version),'03d')}"
    hou.hipFile.setName(f"{shotFolder}/{newHipname}.hip")
    hou.hipFile.save() 
    print(f"Saved as {shotFolder}/{newHipname}.hip")
 
def incrementVersion(version):
    return format(int(version[0]) + 1, '03d')
    
def __main__():            
    hipname = hou.getenv("hipname")
    fullName, sceneFolder, baseName, version = parseFileName(hipname)
    versions = findOtherVersions(baseName)
    newVersion = incrementVersion(version)
    newName = f"{baseName}_v{newVersion}.hip"
    
    if newName in versions:
        duplicateFound = hou.ui.displayMessage("Next version already exists.", buttons=('Save as Latest','Overwrite', 'Cancel'))
        if duplicateFound == 0:
            newMaxVersion = format(int(getVersion(versions[-1])[0]) + 1,'03d')
            newName = f"{baseName}_v{newMaxVersion}.hip"
            saveScene(sceneFolder, baseName, getVersion(newName)[0])
            sys.exit()
            
        if duplicateFound == 1:
            saveScene(sceneFolder, baseName, getVersion(newName)[0])
            sys.exit()

            
    if newName not in versions:
        saveScene(sceneFolder, baseName, getVersion(newName)[0])
        sys.exit()


__main__()
