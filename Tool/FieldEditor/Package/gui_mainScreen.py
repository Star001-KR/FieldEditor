from Package.tool_manager import *
from tkinter import *

class MainScreen():
    # tool manager.
    FieldEditorManager = ToolManager()

    # window ui setting value.
    Title = "Field Editor"
    Geometry = (900, 500)
    Resizable = (True, True)

    def __init__(self, winodw):
        # window default ui setting initialize.
        winodw.title(self.Title)
        winodw.geometry("{0}x{1}".format(self.Geometry[0], self.Geometry[1]))
        winodw.resizable(self.Resizable[0], self.Resizable[1])

        # window variable initialize.
        self._selectGroupNum = 0
        self._isPushStartBtn = False
        self._isPushGoalBtn = False
        self.btn_tileList = [[0 for _ in range(FieldGroup.GetTileSize()[1])] for _ in range(FieldGroup.GetTileSize()[0])]
        self.noNameText = "input new field name.."

    # [ Frame Group - Field List ]
        self.frameGroup_FieldList = LabelFrame(winodw, text = "Field List")
        self.frameGroup_FieldList.grid(row = 0, column = 0)

        # Field List (0, 0) - Change Position.
        self.frame_ChangePos = Frame(self.frameGroup_FieldList)
        self.frame_ChangePos.grid(row = 0, column = 0)

        self.btn_changePosUp = Button(self.frame_ChangePos, text = "▲", width = 10,
            command = lambda isUp = True : self.__Press_btn_changePos(isUp))
        self.btn_changePosUp.grid(row = 0, column = 0)

        self.btn_changePosDown = Button(self.frame_ChangePos, text = "▼", width = 10,
            command = lambda isUp = False : self.__Press_btn_changePos(isUp))
        self.btn_changePosDown.grid(row = 0, column = 1)

        # Field List (1, 0) - Field List.
        self.frame_fieldList = Frame(self.frameGroup_FieldList)
        self.frame_fieldList.grid(row = 1, column = 0)

        self.list_fieldGroup = Listbox(self.frame_fieldList)
        self.list_fieldGroup.grid(row = 0, column = 0)

        self.__Refresh_FieldGroupList()

        self.btn_selectField = Button(self.frame_fieldList, text = "Select Field", width = 20, command = self.__Press_btn_selctField)
        self.btn_selectField.grid(row = 1, column = 0)

        # Field List (2, 0) - Add Field Group.
        self.frame_AddField = LabelFrame(self.frame_fieldList, text = "Add Field")
        self.frame_AddField.grid(row = 2, column = 0)

        self.text_addFieldName = Entry(self.frame_AddField)
        self.text_addFieldName.insert(0, self.noNameText)
        self.text_addFieldName.grid(row = 0, column = 0)

        self.btd_addField = Button(self.frame_AddField, text = "Add Field", width = 20, height = 2, command = self.__Press_btn_addField)
        self.btd_addField.grid(row = 1, column = 0)

        # Field List (3, 0) - Delete Field Group.
        self.frame_DelField = LabelFrame(self.frameGroup_FieldList, text = "Del Field")
        self.frame_DelField.grid(row = 3, column = 0)

        btd_delField = Button(self.frame_DelField, text = "Delete Field", width = 20, height = 2, command = self.__Press_btn_delField, fg = "red")
        btd_delField.grid(row = 0, column = 0)


    # [ Frame Group - Field State. ]
        self.frameGroup_FieldState = LabelFrame(winodw, text = "Field State")
        self.frameGroup_FieldState.grid(row = 0, column = 1, sticky = N+E+W+S)

        # Field State (0, 0) - Change Field Group.
        self.frame_changeFieldGroup = Frame(self.frameGroup_FieldState)
        self.frame_changeFieldGroup.grid(row = 0, column = 0)

        btn_beforeGroup = Button(self.frame_changeFieldGroup, text = "<", width = 5, 
            command = lambda isBefore = True : self.__Press_btn_beforeGroup(isBefore))
        btn_beforeGroup.grid(row = 0, column = 0) 

        self.label_groupName = Label(
            self.frame_changeFieldGroup, width = 20, justify = CENTER,
            text = self.FieldEditorManager.Get_FieldGroupCount() and self.FieldEditorManager._fieldGroup[self._selectGroupNum].Get_FieldGroupName() or "")
        self.label_groupName.grid(row = 0, column = 1, columnspan = 4)

        self.btn_afterGroup = Button(self.frame_changeFieldGroup, text = ">", width = 5, 
            command = lambda isBefore = False : self.__Press_btn_beforeGroup(isBefore))
        self.btn_afterGroup.grid(row = 0, column = 5)

        # Field State (1, 0) - Spawn, Goal Point Setting.
        self.frame_spawnGoalSet = LabelFrame(self.frameGroup_FieldState, text = "Start / Goal Setting")
        self.frame_spawnGoalSet.grid(row = 1, column = 0)

        self.btn_Start = Button(self.frame_spawnGoalSet, width = 20, height = 2, text = "Start", command = self.__Press_btn_Start)
        self.btn_Start.grid(row = 0, column = 0)

        self.btn_Goal = Button(self.frame_spawnGoalSet, width = 20, height = 2, text = "Goal", command = self.__Press_btn_Goal)
        self.btn_Goal.grid(row = 0, column = 1)

        # Field State (3, 0) - Validate Check.
        self.frame_validate = Frame(self.frameGroup_FieldState)
        self.frame_validate.grid(row = 3, column = 0)

        self.label_validateText = Label(self.frame_validate, width = 20, anchor = E, text = "Validate Check : ")
        self.label_validateText.grid(row = 0, column = 0, columnspan = 3)

        self.label_validateResult = Label(self.frame_validate, width = 20, anchor = W, 
            text = str(self.FieldEditorManager._fieldGroup[self._selectGroupNum].Is_RightTileSetting()),
            fg = self.FieldEditorManager._fieldGroup[self._selectGroupNum].Is_RightTileSetting() and "black" or "red")
        self.label_validateResult.grid(row = 0, column = 3, columnspan = 3)

        # Field State (2, 0) - Tile State.
        self.frame_tileState = Frame(self.frameGroup_FieldState)
        self.frame_tileState.grid(row = 2, column = 0)
        for posX in range(0, FieldGroup.tileSize[0]):
            for posY in range(0, FieldGroup.tileSize[1]):
                self.btn_tileList[posX][posY] = Button(self.frame_tileState, width = 5, height = 3,
                    command = lambda x = posX, y = posY : self.__Press_btn_tile(x, y))
                self.btn_tileList[posX][posY].grid(row = posY, column = posX)
                
                self.__Set_TileTextSet(posX, posY)


    # [ Frame Group - Buttons. ]
        self.frameGroup_Buttons = LabelFrame(winodw, text = "Buttons")
        self.frameGroup_Buttons.grid(row = 0, column = 2, sticky = N+E+W+S)

        # Buttons (0, 0) - Buttons.
        self.frame_Buttons = Frame(self.frameGroup_Buttons)
        self.frame_Buttons.grid(row = 0, column = 0)

        self.btn_Reset = Button(self.frame_Buttons, text = "Reset", width = 20, height = 2, fg = "red", command = self.__Press_btn_Reset)
        self.btn_Reset.grid(row = 0, column = 0)

        self.btn_Save = Button(self.frame_Buttons, text = "Save", width = 20, height = 2, command = self.__Press_btn_Save)
        self.btn_Save.grid(row = 1, column = 0)


    [classmethod]
    def Get_ToolManager(cls):
        return cls.FieldEditorManager


    def __Press_btn_changePos(self, isUp):
        if not self.list_fieldGroup.curselection():
            return

        if isUp:
            if self.list_fieldGroup.curselection()[0] == 0:
                return

            else:
                tempList = self.list_fieldGroup.get(self.list_fieldGroup.curselection()[0] - 1)
                tempPos = self.list_fieldGroup.curselection()[0]

                self.list_fieldGroup.delete(self.list_fieldGroup.curselection()[0] - 1)
                self.list_fieldGroup.insert(tempPos, tempList)

                self.FieldEditorManager.Swap_FieldGroupPos(self.list_fieldGroup.curselection()[0], self.list_fieldGroup.curselection()[0] + 1)
            
        else:
            if self.list_fieldGroup.curselection()[0] == self.list_fieldGroup.size() - 1:
                return

            else:
                tempList = self.list_fieldGroup.get(self.list_fieldGroup.curselection()[0] + 1)
                tempPos = self.list_fieldGroup.curselection()[0]

                self.list_fieldGroup.delete(self.list_fieldGroup.curselection()[0] + 1)
                self.list_fieldGroup.insert(tempPos, tempList)

                self.FieldEditorManager.Swap_FieldGroupPos(self.list_fieldGroup.curselection()[0], self.list_fieldGroup.curselection()[0] - 1)


    def __Refresh_FieldGroupList(self):
        for _ in range(0, self.list_fieldGroup.size()):
            self.list_fieldGroup.delete(0)

        for listNum in range(0, self.FieldEditorManager.Get_FieldGroupCount()):
            self.list_fieldGroup.insert(listNum, self.FieldEditorManager._fieldGroup[listNum].Get_FieldGroupName())


    def __Press_btn_selctField(self):
        if not self.list_fieldGroup.curselection():
            return

        else:
            self._selectGroupNum = self.list_fieldGroup.curselection()[0]

        self.label_groupName.destroy()

        self.label_groupName = Label(
            self.frame_changeFieldGroup, width = 20, justify = CENTER,
            text = self.FieldEditorManager.Get_FieldGroupCount() and self.FieldEditorManager._fieldGroup[self._selectGroupNum].Get_FieldGroupName() or "")
        self.label_groupName.grid(row = 0, column = 1, columnspan = 4)

        for posX in range(0, FieldGroup.tileSize[0]):
            for posY in range(0, FieldGroup.tileSize[1]):
                self.__Set_TileTextSet(posX, posY)


    def __Press_btn_addField(self):
        if self.text_addFieldName.get() == self.noNameText:
            return

        elif self.text_addFieldName.get() in self.FieldEditorManager.Get_FieldGroupKeyList():
            return

        else:
            self.FieldEditorManager.Add_FieldGroup(self.text_addFieldName.get())

        self.__Refresh_FieldGroupList()


    def __Press_btn_delField(self):
        if not self.list_fieldGroup.curselection():
            return

        else:
            self.FieldEditorManager.Del_FieldGroup(self.list_fieldGroup.curselection()[0])

        self.__Refresh_FieldGroupList()


    def __Press_btn_beforeGroup(self, isBefore):
        if isBefore:
            if not self._selectGroupNum:
                return

            else:
                self._selectGroupNum -= 1

        else:
            if self._selectGroupNum == self.FieldEditorManager.Get_FieldGroupCount() - 1:
                return

            else:
                self._selectGroupNum += 1

        self.list_fieldGroup.activate(self._selectGroupNum)

        self.label_groupName.destroy()

        self.label_groupName = Label(
            self.frame_changeFieldGroup, width = 20, justify = CENTER,
            text = self.FieldEditorManager.Get_FieldGroupCount() and self.FieldEditorManager._fieldGroup[self._selectGroupNum].Get_FieldGroupName() or "")
        self.label_groupName.grid(row = 0, column = 1, columnspan = 4)

        for posX in range(0, FieldGroup.tileSize[0]):
            for posY in range(0, FieldGroup.tileSize[1]):
                self.__Set_TileTextSet(posX, posY)


    def __Press_btn_Start(self):
        # button state change.
        if self._isPushStartBtn:
            self._isPushStartBtn = False

        elif self._isPushGoalBtn:
            self._isPushStartBtn = True
            self._isPushGoalBtn = False

        else:
            self._isPushStartBtn = True

        # button color setting.
        self.__SpawnGoalColorSet()


    def __Press_btn_Goal(self):
        # button state change.
        if self._isPushGoalBtn:
            self._isPushGoalBtn = False

        elif self._isPushStartBtn:
            self._isPushGoalBtn = True
            self._isPushStartBtn = False

        else:
            self._isPushGoalBtn = True

        # button color setting.
        self.__SpawnGoalColorSet()


    def __Press_btn_tile(self, posX, posY):
        # if start button state is 'on press' change tile state to monster - goal tile.
        if self._isPushStartBtn:
            self._isPushStartBtn = False
            
            self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_TileType(ETileType.Monster)
            self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_MonsterTileType(EMonsterTileType.Start)

            self.__SpawnGoalColorSet()
        
        # if goal button state is 'on press' change tile state to monster - goal tile.
        elif self._isPushGoalBtn:
            self._isPushGoalBtn = False
            
            self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_TileType(ETileType.Monster)
            self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_MonsterTileType(EMonsterTileType.Goal)

            self.__SpawnGoalColorSet()

        # tile type change.(rotation : empty > object > monster > empty)
        else:
            tileType = self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Get_TileType()[0]
            
            if tileType == ETileType.Empty:
                self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_TileType(ETileType.Object)
                self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_MonsterTileType(EMonsterTileType.Null)
            
            elif tileType == ETileType.Object:
                self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_TileType(ETileType.Monster)
                self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_MonsterTileType(EMonsterTileType.Normal)

            elif tileType == ETileType.Monster:
                self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_TileType(ETileType.Empty)
                self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Set_MonsterTileType(EMonsterTileType.Null)
        
        self.__Set_TileTextSet(posX, posY)


    def __Press_btn_Reset(self):
        self.FieldEditorManager.Init_ExcelData()

        self.__Refresh_FieldGroupList()

        for posX in range(0, FieldGroup.tileSize[0]):
            for posY in range(0, FieldGroup.tileSize[1]):
                self.__Set_TileTextSet(posX, posY)


    def __Press_btn_Save(self):
        self.FieldEditorManager.Save_ToolDataToExcel()


    def __SpawnGoalColorSet(self):
        # start button color.
        if self._isPushStartBtn:
            self.btn_Start["fg"] = "red"

        else:
            self.btn_Start["fg"] = "black"

        # goal button color.
        if self._isPushGoalBtn:
            self.btn_Goal["fg"] = "red"

        else:
            self.btn_Goal["fg"] = "black"

    
    def __Set_TileTextSet(self, posX, posY):
        (tileType, monsterTileType) = self.FieldEditorManager._fieldGroup[self._selectGroupNum]._tilelist[posX][posY].Get_TileType()

        if tileType == ETileType.Empty:
            self.btn_tileList[posX][posY]["text"] = "Empty"
            self.btn_tileList[posX][posY]["fg"] = "black"

        elif tileType == ETileType.Object:
            self.btn_tileList[posX][posY]["text"] = "obj"
            self.btn_tileList[posX][posY]["fg"] = "blue"

        elif tileType == ETileType.Monster:
            self.btn_tileList[posX][posY]["fg"] = "red"

            if monsterTileType == EMonsterTileType.Start:
                self.btn_tileList[posX][posY]["text"] = "Start"

            elif monsterTileType == EMonsterTileType.Goal:
                self.btn_tileList[posX][posY]["text"] = "Goal"

            else:
                self.btn_tileList[posX][posY]["text"] = "Mon"

        self.label_validateResult["text"] = str(self.FieldEditorManager._fieldGroup[self._selectGroupNum].Is_RightTileSetting())

        if self.FieldEditorManager._fieldGroup[self._selectGroupNum].Is_RightTileSetting():
            self.label_validateResult["fg"] = "black"

        else:
            self.label_validateResult["fg"] = "red"