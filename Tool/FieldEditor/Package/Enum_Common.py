from enum import Enum, auto

class EDirectoryType(Enum):
    inputDir = auto()
    outputDir = auto()

class EDataTable(Enum):
    FieldGroup = auto()
    Tile = auto()

class EColumnProperty(Enum):
    NormalColumn = auto()
    DesignColumn = auto()
    NullableColumn = auto()
    UniqueColumn = auto()

class ETileType(Enum):
    Empty = auto()
    Object = auto()
    Monster = auto()

class EMonsterTileType(Enum):
    Null = auto()
    Normal = auto()
    Start = auto()
    Goal = auto()

def StringToEnum(_string):
    if _string == "Empty":
        return ETileType.Empty
    
    elif _string == "Object":
        return ETileType.Object

    elif _string == "Monster":
        return ETileType.Monster

    else:
        return _string