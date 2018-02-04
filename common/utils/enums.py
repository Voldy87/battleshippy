from enum import Enum,auto,unique

@unique
class MatchType(Enum):
    VERSUS_PC = auto()
    VERSUS_HUMAN = auto()
    AI_BATTLE = auto()
    
class InterfaceType(Enum):
    CLI = auto()
    GUI = auto()
    
class StorageType(Enum):
    DB_LOCAL = auto()
    FILE_LOCAL = auto()
    DB_REMOTE = auto()
    FILE_REMOTE = auto()

class ShootType(Enum):
    FIRST_MISS = auto()
    ALREADY_MISS = auto()
    FIRST_HIT = auto()
    ALREADY_HIT = auto()
    JUST_SINKED = auto()
    ALREADY_SINKED = auto()

class PlayerType(Enum):
    PC = auto()
    HUMAN = auto()
