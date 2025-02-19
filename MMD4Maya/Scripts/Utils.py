import os, sys
import unicodedata
import MMD4Maya.Scripts.Chardet as chardet
import codecs

def ConvertToUnixPath(path = ""):
    return path.replace("\\", "/")

def GetScriptsRootDir():
    return ConvertToUnixPath(os.path.split(os.path.realpath(__file__))[0]) + "/"

def GetExtraTextureDir():
    return GetScriptsRootDir() + "../Textures/"

def GetExtFromFilePath(filePath = ""):
    nPos = filePath.rfind('.')
    return filePath[nPos+1:len(filePath)]

def GetDirFormFilePath(filePath = ""):
    nPos = filePath.rfind('/')
    return filePath[0:nPos+1]

def GetFileNameFromFilePath(filePath = ""):
	nPos = filePath.rfind('/')
	return filePath[nPos+1:filePath.rfind('.')]

def CreateDirInParentDir(parentDir = "", newDirName = ""):
    if not parentDir.endswith("/"):
        parentDir += "/"

    newDirPath = parentDir + newDirName
    if not os.path.isdir(newDirPath):
        os.makedirs(newDirPath)
    newDirPath += '/'
    print(newDirPath)

    if not os.path.exists(newDirPath):
        print(newDirPath + ' does not exist!')
        return ''
    return newDirPath

def ReplaceAllStringInFile(filePath, sourceStr, targetStr):
    print('ReplaceAllStringInFile ' + filePath + ' from ' + sourceStr + ' to ' + targetStr)
    inputFile = codecs.open(filePath, 'r', encoding=CheckCharset(filePath))
    lines = inputFile.readlines()
    inputFile.close()

    outputFile = codecs.open(filePath, 'w', encoding=CheckCharset(filePath))
    for line in lines:
        if not line:
            break
        if sourceStr in line and not targetStr in line:
            nPos = line.find(sourceStr)
            temp1 = line[0:nPos]
            temp2 = line[nPos+len(sourceStr):len(line)]
            temp = temp1 + targetStr + temp2
            outputFile.write(temp)
        else:
            outputFile.write(line)

    outputFile.close()

def IsContainEastAsianWord(text = ''):
    result = False
    for ch in text:
        if isinstance(ch, str):
            if unicodedata.east_asian_width(ch) != 'Na':
                result = True
                break
            else:
                continue
    return result

def CheckCharset(filePath):
    with codecs.open(filePath, "rb") as f:
        data = f.read(4)
        charset = chardet.detect(data)['encoding']
    return charset