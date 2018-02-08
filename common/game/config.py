import common.utils.enums

def buildTerminalCodes():

    res = {
        "Reset":,
        "Void":,
        "Ship":
        "Sinked":
        "Shot":
        "LastShot":
    }
class GameConfig():
    def __init__(self,interface:InterfaceType ,  storage:StorageType, shipDistance:int, shotRadius:int, LetCol:bool, outputPC:bool, clear:bool=:
        self.data=storage,
        self.distance=shipDistance,
        self.area= shotRadius, # taken from config, too
        self.LetCol=LetCol,
        self.viewPCoutput=outputPC,
        self.clear=clear
    def load(self):
        pass
    def save(self):
        pass
