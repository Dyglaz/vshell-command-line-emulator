from zipfile import *
import os
import sys

def getPath(targetDir, curDir):
    if (targetDir == ""):
        return curDir
    elif (targetDir.startswith('/')):
        return ('/' + targetDir.strip('/')) or '/'
    elif (curDir == '/'):
        return '/' + (curDir + targetDir).strip('/')
    else:
        return '/' + (curDir + '/' + targetDir).strip('/')

def ls(zipObj, path):
    try:
        inf = "pass" if path == '/' else zipObj.getinfo(path.lstrip('/') + '/')
        nameList = []
        for name in zipObj.namelist():
            if (name.startswith(path.strip('/'))):
                name = name.replace(path.strip('/'), '').split('/')
                name = list(filter(None, name))
                name = name[0] if name else ""
                if name and name not in nameList:
                    nameList.append(name)
        if nameList:
            print(*nameList, sep='\n')
    except Exception as e:
        print(f"ls: cannot access '{path}': No such file or directory")

def pwd(curDir):
    print(curDir)

def cd(zipObj, path):
    if (path == '/'): return path
    try:
        inf = zipObj.getinfo(path.lstrip('/') + '/')
        if (not inf.is_dir()):
            print(f"cd: {path}: Not a directory")
            return None
        return path
    except KeyError:
        print(f"cd: {path}: No such file or directory")
    return None

def cat(zipObj, path):
    try:
        print(zipObj.open(path.strip('/')).read().decode('utf-8'))
    except:
        print(f"cat: {path}: No such file or directory")

def main():
    fileName = "shell.zip"
    myShell = ZipFile(fileName, 'r')
    curDir = "/"

    while True:
        print(f"[root@{os.getlogin()} {curDir.split('/')[-1] or '/'}]# ", end="")
        inp = input().split() + [""]
        if (len(inp) == 1): continue
        cmd, targetDir = inp[:2]
        if (cmd == "cd"):
            newDir = cd(myShell, getPath(targetDir, curDir))
            curDir = newDir if newDir else curDir
        elif (cmd == "cat"):
            cat(myShell, getPath(targetDir, curDir))
        elif (cmd == "ls"):
            ls(myShell, getPath(targetDir, curDir))
        elif (cmd == "pwd"):
            pwd(curDir)
        elif (cmd == "exit"):
            break
        else:
            print(f"{cmd[0]}: command not found")

if __name__ == "__main__":
    main()

