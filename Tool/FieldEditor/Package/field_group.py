from Package.Enum_Common import *

class FieldGroup():
    tileSize = (6, 5)
    fieldGroupSet = set()

    def __init__(self, fieldGroupName):
        self._fieldGroupName = fieldGroupName
        #self._fieldTheme = fieldTheme

        self._CoverImagePath = "Resource Name"
        self._EmptyTilePath = "Resource Name"
        self._ObjectTilePath = "Resource Name"
        self._MonsterTilePath = "Resource Name"

        self._tilelist = [[0 for _ in range(self.tileSize[1])] for _ in range(self.tileSize[0])]
        for posX in range(0, self.tileSize[0]):
            for posY in range(0, self.tileSize[1]):
                self._tilelist[posX][posY] = Tile(ETileType.Empty)


    def Get_FieldGroupName(self):
        return self._fieldGroupName


    def Get_TileTypeCount(self, tileType):
        count = 0

        for posX in range(0, self.tileSize[0]):
            for posY in range(0, self.tileSize[1]):
                if self._tilelist[posX][posY].Get_TileType()[0] == tileType:
                    count += 1

        return count


    def Set_TileWithTableData(self, tileTableData):  
        for rowData in tileTableData:
            if not tileTableData[rowData][2].value == self._fieldGroupName:
                continue

            else:
                self._tilelist[tileTableData[rowData][3].value - 1][tileTableData[rowData][4].value - 1].Set_TileType(StringToEnum(tileTableData[rowData][5].value))

                # isTileSpawnPoint == True
                if tileTableData[rowData][6].value:
                    self._tilelist[tileTableData[rowData][3].value - 1][tileTableData[rowData][4].value - 1].Set_MonsterTileType(EMonsterTileType.Start)

                # isTileGoalPoint == True
                elif tileTableData[rowData][7].value:
                    self._tilelist[tileTableData[rowData][3].value - 1][tileTableData[rowData][4].value - 1].Set_MonsterTileType(EMonsterTileType.Goal)

                # tile type is monster
                elif self._tilelist[tileTableData[rowData][3].value - 1][tileTableData[rowData][4].value - 1].Get_TileType() == ETileType.Monster:
                    self._tilelist[tileTableData[rowData][3].value - 1][tileTableData[rowData][4].value - 1].Set_MonsterTileType(EMonsterTileType.Normal)

                else:
                    self._tilelist[tileTableData[rowData][3].value - 1][tileTableData[rowData][4].value - 1].Set_MonsterTileType(EMonsterTileType.Null)


    def Is_RightTileSetting(self):
        checkWaitingData = []
        checkCompleteData = []

        isFindStart = False
        isFindGoal = False

        # find monster spawn point tile and append in check waiting data list.
        for posX in range(0, self.tileSize[0]):
            for posY in range(0, self.tileSize[1]):
                if self._tilelist[posX][posY].Get_TileType() == (ETileType.Monster, EMonsterTileType.Start):
                    checkWaitingData.append((posX, posY))
                    isFindStart = True
                    break

        # if no spawn point tile in field group. / return false and error log.
        if not isFindStart:
            print("no start tile in [ {0} ] filed group.".format(self._fieldGroupName))
            
            return False

        while(True):
            if len(checkWaitingData):
                _tempPos = checkWaitingData.pop()
            
            else:
                break

            # left tile check.
            if _tempPos[0] > 0:
                _findTileResult = self.__FindNewCheckTile(checkWaitingData, checkCompleteData, isFindGoal, _tempPos[0] - 1, _tempPos[1])
                
                if (type(_findTileResult) == bool) & (not _findTileResult):
                    return False
                
                elif (type(_findTileResult) == tuple):
                    (checkWaitingData, isFindGoal) = (_findTileResult[0], _findTileResult[1])

            # right tile check.
            if _tempPos[0] < self.tileSize[0] - 1:
                _findTileResult = self.__FindNewCheckTile(checkWaitingData, checkCompleteData, isFindGoal, _tempPos[0] + 1, _tempPos[1])
                
                if (type(_findTileResult) == bool) & (not _findTileResult):
                    return False
                
                elif (type(_findTileResult) == tuple):
                    (checkWaitingData, isFindGoal) = (_findTileResult[0], _findTileResult[1])

            # under tile check.
            if _tempPos[1] > 0:
                _findTileResult = self.__FindNewCheckTile(checkWaitingData, checkCompleteData, isFindGoal, _tempPos[0], _tempPos[1] - 1)
                
                if (type(_findTileResult) == bool) & (not _findTileResult):
                    return False
                
                elif (type(_findTileResult) == tuple):
                    (checkWaitingData, isFindGoal) = (_findTileResult[0], _findTileResult[1])

            # upper tile check.
            if _tempPos[1] < self.tileSize[1] - 1:
                _findTileResult = self.__FindNewCheckTile(checkWaitingData, checkCompleteData, isFindGoal, _tempPos[0], _tempPos[1] + 1)
                
                if (type(_findTileResult) == bool) & (not _findTileResult):
                    return False
                
                elif (type(_findTileResult) == tuple):
                    (checkWaitingData, isFindGoal) = (_findTileResult[0], _findTileResult[1])

            checkCompleteData.append(_tempPos)

        # if no goal point tile in field group. / return false and error log.
        if not isFindGoal:
            print("no goal tile in [ {0} ] filed group.".format(self._fieldGroupName))
            
            return False

        # result.
        if len(checkCompleteData) == self.Get_TileTypeCount(ETileType.Monster):
            return True

        else:
            return False


    def __FindNewCheckTile(self, _checkWaitingData, _checkCompleteData, _isFindGoal, _posX, _posY):        
        if (_posX, _posY) in _checkCompleteData:
            return True

        elif self._tilelist[_posX][_posY].Get_TileType()[0] == ETileType.Monster:
            _checkWaitingData.append((_posX, _posY))

            if self._tilelist[_posX][_posY].Get_TileType()[1] == EMonsterTileType.Goal:
                if _isFindGoal:
                    return False

                _isFindGoal = True

            elif self._tilelist[_posX][_posY].Get_TileType()[1] == EMonsterTileType.Start:
                return False

            return (_checkWaitingData, _isFindGoal)
    

    @classmethod
    def GetTileSize(cls):
        return (cls.tileSize[0], cls.tileSize[1])


    @classmethod
    def AddFieldGroupSet(cls, self):
        if self._fieldGroupName in cls.fieldGroupSet:
            print("this field group already in field group set.")
            
            return

        cls.fieldGroupSet.add(self._fieldGroupName)


    @classmethod
    def RemoveFieldGroupSet(cls, self):
        if not self._fieldGroupName in cls.fieldGroupSet:
            return

        cls.fieldGroupSet.remove(self._fieldGroupName)


class Tile():
    def __init__(self, tileType):
        self._tileType = tileType
        self._monsterTileType = (self._tileType == ETileType.Monster) and EMonsterTileType.Normal or EMonsterTileType.Null


    def Get_TileType(self):
        return (self._tileType, self._monsterTileType)


    def Set_TileType(self, tileType):
        if self._tileType == tileType:
            return

        else:
            self._tileType = tileType
            self._monsterTileType = (self._tileType == ETileType.Monster) and EMonsterTileType.Normal or EMonsterTileType.Null


    def Set_MonsterTileType(self, monsterTileType):
        if (not self._tileType == ETileType.Monster) & (not monsterTileType == EMonsterTileType.Null):
            print("set monster tile type(except null) only be if tile tpye is monster")
            
            return

        else:
            self._monsterTileType = monsterTileType
