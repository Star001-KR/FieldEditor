from Package.Enum_Common import *
import platform

class Directory():
    def __init__(self):
        self._directoryDic = {}

        if platform.system() == "Darwin": # Mac OS
            self._directoryDic[EDirectoryType.inputDir] = "Game/DataSheet/"
            self._directoryDic[EDirectoryType.outputDir] = "Game/DataSheet/"

        else: # other OS (Windows.)
            self._directoryDic[EDirectoryType.inputDir] = "Game\\DataSheet\\"
            self._directoryDic[EDirectoryType.outputDir] = "Game\\DataSheet\\"

    def Init_Directory(self):
        if platform.system() == "Darwin": # Mac OS
            self._directoryDic[EDirectoryType.inputDir] = "Game/DataSheet/"
            self._directoryDic[EDirectoryType.outputDir] = "Game/DataSheet/"

        else: # other OS (Windows.)
            self._directoryDic[EDirectoryType.inputDir] = "Game\\DataSheet\\"
            self._directoryDic[EDirectoryType.outputDir] = "Game\\DataSheet\\"

    def Get_Directory(self, _directoryType):
        try:
            if _directoryType in EDirectoryType:
                return self._directoryDic[_directoryType]
        
        except:
            print("invalid directory type error.")
            
            return

    def Set_Directory(self, _directoryType, _filepath):
        try:
            if _directoryType in EDirectoryType:
                self._directoryDic[_directoryType] = _filepath
                return

        except:
            print("invalid directory type error.")
            
            return