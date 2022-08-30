# MMD4Maya
[![](https://img.shields.io/badge/Autodesk_Maya-2018_|_2019_|_2020_|_2022-blue)](https://www.autodesk.com/products/maya)

This is maya plug-in which use for importing pmx/pmd model to maya.<br>
It is based on pmx2fbx.exe which is wrote by http://stereoarts.jp/<br>
Forked from: https://github.com/gameboy12615/MMD4Maya

## Install:
1. Copy `MMD4Maya.py` and `MMD4Maya` folder to your maya plug-ins folder.
    ```
    - Windows: C:\Users\<username>\Documents\maya\<version>\plug-ins
    - Mac: $HOME/Library/Preferences/Autodesk/maya/<version>/plug-ins
    - Linux: $HOME/maya/<version>/plug-ins
    ```
    OR add repository folder to `MAYA_PLUG_IN_PATH` in `Maya.env` or environment variables.

2. Enable MMD4Maya in maya Plug-in Manager.

## Steps to import:
1. Select a pmx/pmd file.
2. Select one or multiple vmd files.
3. Check the terms of use.
4. Click Process.

## Attention:
1. The support for Japanese or Chinese in file name or file path of fbx file and texture files may be limited.
2. You can only import one model at a time, please save your model as the standard fbx file, then create a new scene to import another one.
