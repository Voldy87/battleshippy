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
        MatchType.VERSUS_PC: set([Pl.PlayerType.HUMAN, Pl.PlayerType.PC]),
        MatchType.VERSUS_HUMAN:set([Pl.PlayerType.HUMAN]),
        MatchType.AI_BATTLE: set([Pl.PlayerType.PC])
    }
ships = {
    10:[
        ["destroyer",1,2], #name,num,len
        ["cruiser",1,3],
        ["submarine",1,3],
        ["battleship",1,4],
        ["carrier",1,5]
    ]
} #loaded from config, normally includes or loads names (yaml parse)
turn = 1
cv = threading.Condition()

class Action(threading.Thread):
    def __init__(self, index:int, grids:list, players:set, uiMode:InterfaceType, dataMode:StorageType, distance:int): 
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
        self.output = not self.isPC #may be different, e.g. in a 2 pc battle one wants to see what happens (consider introducing a delay)
        self.minShipDistance = distance
        #currentPlayer=0 #always start first in Players array (random choice in main)
        #self.turn = 1 #in one turn each player takes a shot
        #self.cv = cv
    def shipsAutoPositioning(self):
        shipsToGive = ships[self.myGrid.dim]
        vett = []
        for elem in shipsToGive: #elem = ship,dim
            for i in range(0,elem[1]): #there can be more ships with the same name/type
                pos = self.me.computerShip(elem[2],"basic",self.minShipDistance,self.myGrid.slots,self.myGrid.ships)
                self.myGrid.addShip(Sh.Ship(elem[0],len(pos)), pos, True)
    def shipsManualPositioning(self):
        side = self.myGrid.dim
        shipsToGive = ships[side]
##        vett = self.ui.askAllShips(side, shipsToGive)
##        if (vett==None):
##            vett=[]
##        else:
##            return vett #e.g. django gui wait for positioning
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
        return self.index!=(turn%2)
    def changeFlag(self):
        global turn
        turn += 1
    def currentTurn(self):
        global turn
        return int(turn/2)+1
    def run(self):
        UI = self.ui
        
            
        for i in range(1,3):#while not otherGrid.allSinked() : 
            #global currentPlayer
##          if (self.myGrid.lastShotInfo):
##              UI.shotUpcome(self.myGrid.lastShotInfo) #if there are no shots (1st turn 1st player does nothing and pass diectly to take shot vs enemy
##              UI.render(self.myGrid,True,True)
            
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
##            if (self.myGrid.allSinked()) :
##                  cv.notify()
##                    cv.release()
##                break
            while not self.checkFlag():
                print(str(self.index) + " waits for its turn\n")
                cv.wait()
            #self.tt+=1
            print("I AM "+str(self.me.name) + " and this is turn " + str(self.currentTurn()) +" \n")
            if i==1:
                UI.startSplash(self.me.name)
            if (self.isPC) and i==1:
                self.shipsAutoPositioning()
                #self.myGrid.shipsPositioning(vett,True)
            #if self.output:
                UI.renderGrid(self.myGrid,True,False)
            elif i==1:
                #vett = self.getShipNamesAndCoord(shipsToGive, 0) #ships to give depend on config
                self.shipsManualPositioning()
                UI.renderGrid(self.myGrid,True,False)
            if i==1 and not self.verifyPositioning():
                raise Exception('Ship positioning failed')
            

##            if (self.isPc):
##                pos = player.computerTarget()
##            else: 
##                pos = UI.getTarget()
##              otherGrid.takeShot(pos)
##              UI.shotUpcome(self.enemyGrid.lastShotInfo)
    ##            UI.render(self.enemyGrid,False,True)
            self.changeFlag()
            cv.notify()
            cv.release()
##        UI.showResults()
##        UI.render(self.myGrid,True,False)
##        UI.render(self.enemyGrid,True,False)
##        UI.finishSplash()


def initGame (side:int, playerNames:list, matchType:MatchType,storageType:StorageType):
    gridArray = [Gr.Grid(side), Gr.Grid(side)]
    if len(games[matchType])==1:
        PlayerTypes = list(games[matchType].pop())
        PlayerTypes *= 2
    else:
        PlayerTypes = list(games[matchType])
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
    distance = 1 # taken from config, too
    gameEnded = False
    stats = None #global stats 
    threads=[None,None]
    #workers (in django assigned to clients..)
    threads[0] =  Action(0, grids, players, uiMode, dataMode,distance)
    threads[1] =  Action(1, grids, players, uiMode, dataMode,distance)
    threads[0].start()
    threads[1].start()
    for x in threads: 
        x.join()
    updateGlobalStats(stats)
