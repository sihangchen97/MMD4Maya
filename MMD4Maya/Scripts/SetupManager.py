import os
import sys
import subprocess

MAYA_PATH = sys.executable  # /xxx/xxx/bin/maya.exe
_suffix = os.path.splitext(MAYA_PATH)[-1]    # ".exe" on windows; "" on *nix
MAYAPY_PATH = "\"" + os.path.join(os.path.dirname(MAYA_PATH), "mayapy" + _suffix) + "\""
MAYAPY_VERSION = str(sys.version_info.major) + "." + str(sys.version_info.minor)
    
def RunCommand(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return True
    except:
        return False

def CheckPip():
    return RunCommand(MAYAPY_PATH + " -m pip -V")

def SetupPip():
    if CheckPip():
        return True
    getPipUrl = "https://bootstrap.pypa.io/pip/" + (MAYAPY_VERSION if MAYAPY_VERSION in ["2.6", "2.7", "3.2", "3.3", "3.4", "3.5", "3.6"] else "")  + "/get-pip.py"
    try:
        os.system("curl -sSL " + getPipUrl + " -o get-pip.py")
        os.system(MAYAPY_PATH + " get-pip.py")
        os.remove("get-pip.py")
    except:
        pass
    return CheckPip()

def CheckModule(name):
    return RunCommand(MAYAPY_PATH + " -c \"import " + name + "\"")

def SetupModule(name, version=None):
    if CheckModule(name):
        return True
    RunCommand(MAYAPY_PATH + " -m pip --no-cache-dir install " + name + ("" if version==None else "==" + str(version)))
    return CheckModule(name)
