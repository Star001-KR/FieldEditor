from Package.directory import *
from Package.field_group import *
from Package.common_function import *
import shutil
import os

class ToolManager(Directory):
    dataSheetName = "Sheet1"

    def __init__(self):
        # init directory.
        super().__init__()
        
        # init excel file name, excel file full directory(original data, copy data).
        self._fileName = {
            EDataTable.FieldGroup : "FieldGroup.xlsx", 
            EDataTable.Tile : "FieldTile.xlsx"
        }
        self._fileFullName = {
            EDataTable.FieldGroup : self._directoryDic[EDirectoryType.inputDir] + self._fileName[EDataTable.FieldGroup],
            EDataTable.Tile : self._directoryDic[EDirectoryType.inputDir] + self._fileName[EDataTable.Tile]
        }
        self._tempFileFullName = {
            EDataTable.FieldGroup : self._directoryDic[EDirectoryType.inputDir] + "_" +self._fileName[EDataTable.FieldGroup],
            EDataTable.Tile : self._directoryDic[EDirectoryType.inputDir] + "_" + self._fileName[EDataTable.Tile]
        }

        # copy excel file. (use to initialize field group data.)
        shutil.copy2(self._fileFullName[EDataTable.FieldGroup], self._tempFileFullName[EDataTable.FieldGroup])
        shutil.copy2(self._fileFullName[EDataTable.Tile], self._tempFileFullName[EDataTable.Tile])

        # copy excel data in target sheet (self.dataSheetName).
        (self._fieldGroupDic,   self._fieldGroupKeyList)    = Copy_ExcelDataToLib(self._fileFullName[EDataTable.FieldGroup], self.dataSheetName)    
        (self._tileDic,         self._tileKeyList)          = Copy_ExcelDataToLib(self._fileFullName[EDataTable.Tile], self.dataSheetName)
        
        # excluding column name row and data tpye row. (=2)
        self._fieldGroupCount = len(self._fieldGroupKeyList) > 2 and len(self._fieldGroupKeyList) - 2 or False
        self._fieldGroup = []
        for fieldGroupNum in range(0, self._fieldGroupCount):
            self._fieldGroup.append(FieldGroup(self._fieldGroupKeyList[fieldGroupNum + 2]))
            self._fieldGroup[fieldGroupNum].Set_TileWithTableData(self._tileDic)


    # add new field group.
    def Add_FieldGroup(self, fieldGroupName):
        self._fieldGroupCount += 1

        if type(fieldGroupName) == str:
            self._fieldGroupKeyList.append(fieldGroupName)
            self._fieldGroup.append(FieldGroup(fieldGroupName))

        else:
            self._fieldGroupKeyList.append(str(fieldGroupName))
            self._fieldGroup.append(FieldGroup(str(fieldGroupName)))


    # delete selected field group.
    def Del_FieldGroup(self, fieldGroup):
        self._fieldGroupCount -= 1

        if type(fieldGroup) == int:
            if fieldGroup > len(self._fieldGroup):
                return "wrong field group number input at field group factor."

            self._fieldGroup.pop(fieldGroup)

        elif type(fieldGroup) == str:
            for _fieldGroupNum in range(0, len(self._fieldGroup)):
                if fieldGroup == self._fieldGroup[_fieldGroupNum].Get_FieldGroupName():
                    self._fieldGroupKeyList.pop(_fieldGroupNum)
                    self._fieldGroup.pop(_fieldGroupNum)
                    return

        elif type(fieldGroup) == FieldGroup:
            for _fieldGroupNum in range(0, len(self._fieldGroup)):
                if fieldGroup.Get_FieldGroupName() == self._fieldGroup[_fieldGroupNum].Get_FieldGroupName():
                    self._fieldGroupKeyList.pop(_fieldGroupNum)
                    self._fieldGroup.pop(_fieldGroupNum)
                    return

        else:
            self._fieldGroupCount += 1
            return "wrong data type input at field group factor."


    # field group position change. (selected direction)
    def Swap_FieldGroupPos(self, Pos1, Pos2):
        if (not type(Pos1) == int) | (not type(Pos2) == int):
            return

        else:
            _tempFieldGroup = self._fieldGroup[Pos1]

            self._fieldGroup[Pos1] = self._fieldGroup[Pos2]
            self._fieldGroup[Pos2] = _tempFieldGroup


    # return field group count.
    def Get_FieldGroupCount(self):
        return self._fieldGroupCount


    # return field group key list.
    def Get_FieldGroupKeyList(self):
        return self._fieldGroupKeyList


    # return tiletype. (selected tile position (posX, posY))
    def Get_FieldData(self, fieldGroup, posX, posY):
        if type(fieldGroup) == int:
            if fieldGroup > len(self._fieldGroup):
                return "wrong field group number input at field group factor."

            return self._fieldGroup[fieldGroup]._tilelist[posX - 1][posY - 1].Get_TileType()

        elif type(fieldGroup) == str:
            for _fieldGroup in self._fieldGroup:
                if fieldGroup == _fieldGroup.Get_FieldGroupName():
                    return _fieldGroup._tilelist[posX - 1][posY - 1].Get_TileType()
            
            return "wrong field group object input at field group factor"

        elif type(fieldGroup) == ToolManager:
            return fieldGroup._tilelist[posX - 1][posY - 1].Get_TileType()

        else:
            return "wrong data type input at field group factor."
        

    # save tool data to excel data.
    def Save_ToolDataToExcel(self):
        DATA_HEAD_ROW_COUNT = 2
        TILE_INPUT_ROW_NUM = 2

        _fieldGroupLib = {
            0 : ["ID", "#기획용 데이터", "CoverImagePath", "EmptyTilePath", "ObjectTilePath", "MonsterTilePath"],
            1 : ["key", "string",      "string?",       "string",           "string",       "string"]
        }

        _fieldTileLib = {
            0 : ["ID", "#기획용 데이터", "FieldGroupID", "TilePosX", "TilePosY", "TileType", "isTileSpawnPoint", "isTileGoalPoint"],
            1 : ["key","string",        "key",          "int",      "int",    "ETileType",      "bool",         "bool"]
        }

        for fieldGroupRow in range(0, self.Get_FieldGroupCount()):
            _fieldGroupLib[fieldGroupRow + DATA_HEAD_ROW_COUNT] = [
                self._fieldGroup[fieldGroupRow].Get_FieldGroupName(),
                "",
                self._fieldGroup[fieldGroupRow]._CoverImagePath,
                self._fieldGroup[fieldGroupRow]._EmptyTilePath,
                self._fieldGroup[fieldGroupRow]._ObjectTilePath,
                self._fieldGroup[fieldGroupRow]._MonsterTilePath
            ]

            for tilePosX in range(0, FieldGroup.GetTileSize()[0]):
                for tilePosY in range(0, FieldGroup.GetTileSize()[1]):
                    _fieldTileLib[TILE_INPUT_ROW_NUM] = [
                        "{0}_{1}_{2}".format(self._fieldGroup[fieldGroupRow].Get_FieldGroupName(), tilePosX + 1, tilePosY + 1),
                        "",
                        self._fieldGroup[fieldGroupRow].Get_FieldGroupName(),
                        tilePosX + 1,
                        tilePosY + 1,
                        str(self._fieldGroup[fieldGroupRow]._tilelist[tilePosX][tilePosY].Get_TileType()[0]).split(".")[1],
                        self._fieldGroup[fieldGroupRow]._tilelist[tilePosX][tilePosY].Get_TileType()[1] == EMonsterTileType.Start and True or False,
                        self._fieldGroup[fieldGroupRow]._tilelist[tilePosX][tilePosY].Get_TileType()[1] == EMonsterTileType.Goal and True or False
                    ]
                    
                    TILE_INPUT_ROW_NUM += 1

        Copy_LibToExcelData(self._fileFullName[EDataTable.FieldGroup], _fieldGroupLib, self.dataSheetName)
        Copy_LibToExcelData(self._fileFullName[EDataTable.Tile], _fieldTileLib, self.dataSheetName)


    # init excel data to tool start state. (use temp excel file.)
    def Init_ExcelData(self):
        os.remove(self._fileFullName[EDataTable.FieldGroup])
        os.remove(self._fileFullName[EDataTable.Tile])

        shutil.copy2(self._tempFileFullName[EDataTable.FieldGroup], self._fileFullName[EDataTable.FieldGroup])
        shutil.copy2(self._tempFileFullName[EDataTable.Tile], self._fileFullName[EDataTable.Tile])

        self._fieldGroupDic.clear()
        self._fieldGroupKeyList.clear()
        self._tileDic.clear()
        self._tileKeyList.clear()
        self._fieldGroup.clear()

        (self._fieldGroupDic,   self._fieldGroupKeyList)    = Copy_ExcelDataToLib(self._fileFullName[EDataTable.FieldGroup], self.dataSheetName)    
        (self._tileDic,         self._tileKeyList)          = Copy_ExcelDataToLib(self._fileFullName[EDataTable.Tile], self.dataSheetName)

        self._fieldGroupCount = len(self._fieldGroupKeyList) - 2
        self._fieldGroup = []
        for fieldGroupNum in range(0, self._fieldGroupCount):
            self._fieldGroup.append(FieldGroup(self._fieldGroupKeyList[fieldGroupNum + 2]))
            self._fieldGroup[fieldGroupNum].Set_TileWithTableData(self._tileDic)


    def __del__(self):
        # delete temp excel file.
        os.remove(self._tempFileFullName[EDataTable.FieldGroup])
        os.remove(self._tempFileFullName[EDataTable.Tile])