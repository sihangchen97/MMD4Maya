from MMD4Maya.Scripts.Utils import *
import re
from pykakasi import kakasi

class FBXModifier:

    def __init__(self, mainWindow = None):
        self.mainWindow = mainWindow
        self.kakasi = kakasi()
        self.kakasi.setMode('H', 'a')
        self.kakasi.setMode('K', 'a')
        self.kakasi.setMode('J', 'a')
        self.kakasi.setMode('E', 'a')
        self.conv = self.kakasi.getConverter()

        self.rMayaNaming = re.compile("[^a-zA-Z0-9_]")
        self.rBeginWithNum = re.compile("^[0-9]+")

    def FormatMaterialName(self, name):
        newName = ''
        if '.' in name:
            nPos = name.find('.')
            newName = 'mat_' + name[0:nPos]
        else:
            newName = 'mat_' + name
        return newName

    def FormatName(self, name):
        newName = name
        newName = newName.replace('!', '')
        newName = newName.replace('+', '_Plus')
        newName = self.rMayaNaming.sub("_", self.conv.do(newName))
        if self.rBeginWithNum.match(newName)!=None:
            newName = "_" + newName
        return newName

    def ModifyMaterialName(self, fbxFilePath):
        inputFbxFile = open(fbxFilePath, 'r', encoding='UTF-8')
        inputFbxLines = inputFbxFile.readlines()
        inputFbxFile.close()
        outputFbxFile = open(fbxFilePath, 'w', encoding='UTF-8')
        tag1 = 'Material::'
        tag2 = ';Material::'
        for line in inputFbxLines:
            if not line:
                break
            if tag2 in line:
                nPos1 = line.find(tag2)
                temp1 = line[0:nPos1]
                temp2 = line[nPos1+len(tag2):len(line)]
                nPos2 = temp2.find(', Model::')
                temp3 = temp2[nPos2:len(temp2)]
                materialName = self.FormatMaterialName(temp2[0:nPos2])
                temp = temp1 + tag2 + materialName + temp3
                outputFbxFile.write(temp)
            elif tag1 in line:
                nPos1 = line.find(tag1)
                temp1 = line[0:nPos1]
                temp2 = line[nPos1+len(tag1):len(line)]
                nPos2 = temp2.find('"')
                temp3 = temp2[nPos2:len(temp2)]
                materialName = self.FormatMaterialName(temp2[0:nPos2])
                temp = temp1 + tag1 + materialName + temp3
                outputFbxFile.write(temp)
            else:
                outputFbxFile.write(line)
        outputFbxFile.close()
    
    def ModifyName(self, inFbxFilePath, outFbxFilePath=None):
        if outFbxFilePath==None:
            outFbxFilePath = inFbxFilePath

        inFbxFile = open(inFbxFilePath, 'r', encoding='UTF-8')
        fbxContent = inFbxFile.read()
        inFbxFile.close()

        segs = fbxContent.split("::")
        processIndexList = [i for i in range(len(segs)-1)]
        nameMapping = {}
        MAX_LEN = len(fbxContent)

        self.mainWindow.Log(f"--- collecting modify info ...")
        for index in processIndexList:
            start = max(segs[index].rfind("\""),segs[index].rfind(";"),segs[index].rfind(" "))
            tag = segs[index][start+1:]
            if tag not in ['NodeAttribute', 'Model', 'SubDeformer', 'Geometry']:
                processIndexList.remove(index)
                continue
            if tag not in ["NodeAttribute", 'Geometry']:
                continue

            def nonNegativeMin(a,b):
                return min(a,b) if a>=0 and b>=0 else a if a>=0 else b if b>=0 else MAX_LEN

            end = nonNegativeMin(segs[index+1].find(","),nonNegativeMin(segs[index+1].find("\n"),segs[index+1].find("\"")))
            name = segs[index+1][:end]
            if name not in nameMapping.keys():
                newName = self.FormatName(name)
                while newName in nameMapping.values():
                    newName = newName + "_"
                if name!=newName:
                    nameMapping[name] = newName
        
        total = len(processIndexList)
        for i, index in enumerate(processIndexList):
            if i%10000==0:
                self.mainWindow.Log(f"--- modifying names: %d/%d"%(i,total))
            start = max(segs[index].rfind("\""),segs[index].rfind(";"),segs[index].rfind(" "))
            tag = segs[index][start+1:]
            end = nonNegativeMin(segs[index+1].find(","),nonNegativeMin(segs[index+1].find("\n"),segs[index+1].find("\"")))
            name = segs[index+1][:end]
            if tag in ['NodeAttribute', 'Model', 'SubDeformer', 'Geometry'] and name in nameMapping.keys():
                segs[index+1] = segs[index+1].replace(name, nameMapping[name],1)

        self.mainWindow.Log(f"--- modifying names: %d/%d finish!"%(total,total))
        fbxContent = "::".join(segs)
        self.mainWindow.Log("--- writing temp file")
        outFbxFile = open(outFbxFilePath, 'w', encoding='UTF-8')
        outFbxFile.write(fbxContent)
        outFbxFile.close()

    def ModifyXmlFile(self, xmlFilePath):
        extraTextureDir = GetExtraTextureDir()
        textureDir = GetDirFormFilePath(xmlFilePath) + "../"
        ReplaceAllStringInFile(xmlFilePath, '<materialName>', '<materialName>mat_')
        ReplaceAllStringInFile(xmlFilePath, '<fileName>', '<fileName>' + textureDir)
        ReplaceAllStringInFile(xmlFilePath, '<fileName>' + textureDir + 'toon', '<fileName>' + extraTextureDir + 'toon')

    def Process(self, fbxFilePath):
        xmlFilePath = GetDirFormFilePath(fbxFilePath) + GetFileNameFromFilePath(fbxFilePath) + ".xml"
        self.ModifyMaterialName(fbxFilePath)
        self.ModifyName(fbxFilePath)
        self.ModifyXmlFile(xmlFilePath)
        self.mainWindow.Log('modify process completed!')
