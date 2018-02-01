# python -m local_executable.battleshippy

import common.game.grid as Gr
import common.game.ship as Sh
import common.game.player as Pl
import common.interface.cli as CL, common.interface.gui as GU
from common.utils.grid import slotsWithShips
##import common.interface.menu as ME
##import common.data.db as DB, common.data.file as FI 

import threading
from random import seed,choice
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

def shipSlots(ships):
    count = 0
    for spam in ships:
        for i in range(0,spam[1]):
            count+=spam[2]
    return count
games = {
        MatchType.VERSUS_PC: [Pl.PlayerType.HUMAN, Pl.PlayerType.PC],
        MatchType.VERSUS_HUMAN:[Pl.PlayerType.HUMAN,Pl.PlayerType.HUMAN],
        MatchType.AI_BATTLE: [Pl.PlayerType.PC,Pl.PlayerType.PC]
    }
ships = {
    10:[
        ["destroyer",1,2], #name,num,len
        #["cruiser",1,3],
        #["submarine",1,3],
        #["battleship",1,4],
        ["carrier",1,5]
    ]
} #loaded from config, normally includes or loads names (yaml parse)
turn = 0
cv = threading.Condition()

class Action(threading.Thread):
    def __init__(self, index:int, grids:list, players:set, uiMode:InterfaceType, dataMode:StorageType, distance:int, radius:int, LetCol:bool, outputPC:bool): 
        threading.Thread.__init__(self) 
        self.index = index
        self.myGrid, self.enemyGrid = grids[index], grids[1-index] #deve puntare all'array di 2 griglie
        if(uiMode is InterfaceType.CLI):
            self.ui=CL.CLI()
        elif(uiMode is InterfaceType.GUI):
            self.ui=CL.GUI()
        else:
            exit(1)#better an exception 
##       if(dataMode=="localDB" || dataMode=="remoteDB"):
##            self.data=DataDb()
##        else:
##            self.data=DataFile()
        self.me, self.enemy = players[index], players[1-index]
        self.isPC =  players[index].nature is Pl.PlayerType.PC
        self.output = outputPC or not self.isPC #may be different, e.g. in a 2 pc battle one wants to see what happens (consider introducing a delay)
        self.minShipDistance = distance
        self.shotRadius = radius
        self.letCol = LetCol
    def shipsAutoPositioning(self,strategy):
        shipsToGive = ships[self.myGrid.dim]
        vett = []
        for elem in shipsToGive: #elem = ship,dim
            for i in range(0,elem[1]): #there can be more ships with the same name/type
                pos = self.me.computerShip(elem[2],strategy,self.minShipDistance,self.myGrid.slots,self.myGrid.ships)
                self.myGrid.addShip(Sh.Ship(elem[0],len(pos)), pos, True)
    def shipsManualPositioning(self):
        side = self.myGrid.dim
        shipsToGive = ships[side]
        for elem in shipsToGive: #elem = Ship
            vessel = Sh.Ship(elem[0],elem[2])
            while True:
                coords = self.ui.askSingleShip(side,vessel)
                if (self.myGrid.posChecker(self.minShipDistance,coords)):
                    break
            self.myGrid.addShip(vessel, coords, False)
    def verifyPositioning(self):
        return slotsWithShips(self.myGrid) == shipSlots(ships[self.myGrid.dim])
    def checkFlag(self):
        global turn
        return self.index==(turn%2)
    def changeFlag(self):
        global turn
        turn += 1
    def currentTurn(self):
        global turn
        return int(turn/2)
    def run(self):
        UI = self.ui
        
            #no direct printing in prod
        for i in range(1,4):#while not self.myGrid.allSinked():
 
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
##            if () : #fails if this player's enemy wins
##                  cv.notify()
##                    cv.release()
##                break
            while not self.checkFlag():
                print(str(self.me.name) + " waits for its turn\n")
                cv.wait()
            print("I AM "+str(self.me.name) + " and this is turn " + str(self.currentTurn()) +" \n")
            if self.currentTurn()==0: #"turn 0": ship positioning
                UI.startSplash(self.me.name)
                if self.isPC :
                    self.shipsAutoPositioning("basic")
                #self.myGrid.shipsPositioning(vett,True)
            #if self.output:
                    #UI.renderGrid(self.myGrid,True,False)
                else:
                #vett = self.getShipNamesAndCoord(shipsToGive, 0) #ships to give depend on config
                    self.shipsManualPositioning()
                if self.output:
                    UI.renderGrid(self.myGrid,True,False)
                if not self.verifyPositioning():
                    raise Exception('Ship positioning failed')
            else: #"normal turn"
                if self.currentTurn()>1:
                    UI.shotUpcome(self.myGrid.lastShotInfo,False,self.letCol) #enemy's last shot info
                    UI.renderGrid(self.myGrid,True,True)
                pos = None
                if self.isPC :
                    pos = self.me.computerTarget(self.enemyGrid.slots,"basic")
                    OnlyNum = True
                else: 
                    pos = UI.askTarget(self.enemyGrid.dim) #gestione radius, da fare
                    OnlyNum = False
                self.enemyGrid.shoot(pos,self.shotRadius,OnlyNum)
                if self.output:
                    UI.shotUpcome(self.enemyGrid.lastShotInfo,True,self.letCol)
                    UI.renderGrid(self.enemyGrid,False,True)
            self.changeFlag()
            cv.notify()
            cv.release()
            #if self.enemyGrid.allSinked():
             #   break
##        UI.showResults()
##        UI.render(self.myGrid,True,False)
##        UI.render(self.enemyGrid,True,False)
##        UI.finishSplash()


def initGame (side:int, playerNames:list, matchType:MatchType,storageType:StorageType):
    gridArray = [Gr.Grid(side), Gr.Grid(side)]
    PlayerTypes = games[matchType]
    playerArray=[]
    for i in (0,1):
        playerArray.append(Pl.Player(PlayerTypes[i],playerNames[i]))
    seed()
    l = [lambda x: x[::-1], lambda x: x]
    choice(l)(playerArray) #randomly choose which player will start (has index 0), but can be decided before (look config) givin prio
    return gridArray, playerArray #two arrays of 2 elements each
def updateGlobalStats(stats):
    pass

if __name__ == "__main__":#this will be also the shape of the main thread on the django server
    uiMode = InterfaceType.CLI #args or ask prompt..
    dataMode = StorageType.FILE_LOCAL    
    #in case of start..
    grids, players = initGame(10,["andrea","computer"],MatchType.VERSUS_PC,StorageType.FILE_LOCAL)
    # all above args of init are taken from config files or others, not hardcoded
    distance = 1 # taken from config
    radius = 0 # taken from config, too
    LetCol = True # idem as above
    outputPC = True
    gameEnded = False
    stats = None #global stats 
    threads=[None,None]
    #workers (in django assigned to clients..)
    threads[0] =  Action(0, grids, players, uiMode, dataMode,distance, radius, LetCol, outputPC) #mettere un po' di roba in un dcit o altro x ridurre args?
    threads[1] =  Action(1, grids, players, uiMode, dataMode,distance, radius, LetCol, outputPC) #notnecessarily args are equal, in case always sintetizza..
    threads[0].start()
    threads[1].start()
    for x in threads: 
        x.join()
    updateGlobalStats(stats)
