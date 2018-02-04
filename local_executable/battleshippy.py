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
from common.utils.enums import MatchType as m, PlayerType as p, StorageType as s, InterfaceType as i

def shipSlots(ships):
    count = 0
    for spam in ships:
        for i in range(0,spam[1]):
            count+=spam[2]
    return count
games = {
        m.VERSUS_PC: [p.HUMAN, p.PC],
        m.VERSUS_HUMAN:[p.HUMAN,p.HUMAN],
        m.AI_BATTLE: [p.PC,p.PC]
    }
ships = {
    2:[
        ["destroyer",1,2]
    ],
    10:[
        ["destroyer",1,2], #name,num,len
        ["cruiser",1,3],
        ["submarine",1,3],
        ["battleship",1,4],
        ["carrier",1,5]
    ]
} #loaded from config, normally includes or loads names (yaml parse)
turn = None #togliere omonomia
cv = threading.Condition()

class Action(threading.Thread):
    def __init__(self, index:int, grids:list, players:list, config:dict): 
        threading.Thread.__init__(self) 
        self.index = index
        self.myGrid, self.enemyGrid = grids[index], grids[1-index] #deve puntare all'array di 2 griglie
        if(config["uiMode"] is i.CLI):
            self.ui=CL.CLI()
        elif(config["uiMode"] is i.GUI):
            self.ui=CL.GUI()
        else:
            exit(1)#better an exception 
##       if(dataMode=="localDB" || dataMode=="remoteDB"):
##            self.data=DataDb()
##        else:
##            self.data=DataFile()
        self.me, self.enemy = players[index], players[1-index]
        self.isPC =  players[index].nature is p.PC
        self.output = config["outputPC"] or not self.isPC #may be different, e.g. in a 2 pc battle one wants to see what happens (consider introducing a delay)
        self.minShipDistance = config["distance"] #all these are equal for all thread maybe we can keep them global and don't pass
        self.shotRadius = config["radius"]
        self.letCol = config["LetCol"]
        self.clear = config["clear"]
    def shipsAutoPositioning(self,strategy):
        shipsToGive = ships[self.myGrid.dim]
        vett = []
        for elem in shipsToGive: #elem = ship,dim
            for spam in range(0,elem[1]): #there can be more ships with the same name/type
                pos = self.me.computerShip(elem[2],strategy,self.minShipDistance,self.myGrid.slots,self.myGrid.ships)
                self.myGrid.addShip(Sh.Ship(elem[0],len(pos)), pos, True)
    def shipsManualPositioning(self):
        side = self.myGrid.dim
        shipsToGive = ships[side]#improve
        for elem in shipsToGive:
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
    def currentTurn(self):#in this "turn" every player takes a shot
        global turn
        return int(turn/2)
    def endgame(self):
        return self.myGrid.allSinked() or self.enemyGrid.allSinked()
    def run(self):
        UI = self.ui
        if self.index==0:
            print(self.me.name+" starts!!")
            #no direct printing in prod
        #for i in range(1,4):#
        while not self.enemyGrid.allSinked():
 
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
            while not self.checkFlag():
                print(str(self.me.name) + " waits for its turn\n")
                cv.wait()
            print("I AM "+str(self.me.name) + " and this is turn " + str(self.currentTurn()) +" \n")
            if self.currentTurn()==0: #"turn 0": ship positioning
                if self.output:
                    UI.startSplash(self.me.name)
                if self.isPC :
                    self.shipsAutoPositioning("basic")
                else:
                    self.shipsManualPositioning()
                if self.output:
                    UI.gridSplash(self.me.name)
                    UI.renderGrid(self.myGrid,True,False)
                if not self.verifyPositioning():
                    raise Exception('Ship positioning failed')
                if self.output:
                    UI.battleSplash(self.me.name)
            else: #"normal turn"
                if turn>=3:
                    UI.shotUpcome(self.me.name,self.myGrid.lastShotInfo,False,self.letCol) #enemy's last shot info
                    UI.renderGrid(self.myGrid,True,True)
                if self.myGrid.allSinked():
                    cv.release()
                    break
                pos = None
                if self.isPC :
                    pos = self.me.computerTarget(self.enemyGrid.slots,"basic")
                    OnlyNum = True
                else: 
                    UI.shootSplash(self.me.name) 
                    UI.renderGrid(self.enemyGrid,False,True)
                    pos = UI.askTarget(self.enemyGrid.dim) #gestione radius, da fare
                    OnlyNum = False
                self.enemyGrid.shoot(pos,self.shotRadius,OnlyNum)
                shooting_result = self.me.reactToShot(self.enemyGrid.lastShotInfo)
                if self.output:#enemy shot result (includes both player types)
                    coords, victory = self.enemyGrid.lastShotInfo['coords'], self.enemyGrid.allSinked()
                    UI.shotUpcome(self.me.name,coords,shooting_result,victory,True,self.letCol)
                    UI.renderGrid(self.enemyGrid,False,True)
            if self.clear and not self.endgame(): #in case players share terminal (hum vs hum) one cannot see the others grids!
                UI.changeSplash(self.me.name,self.enemy.name,3,3)
            self.changeFlag()
            cv.notify()
            cv.release()
            
##        UI.showResults()
##        UI.render(self.myGrid,True,False)
##        UI.render(self.enemyGrid,True,False)
##        UI.finishSplash()


def initGame (side, playerNames, matchType,storageType):
    global turn
    turn = 0
    gridArray = [Gr.Grid(side), Gr.Grid(side)]
    PlayerTypes = games[matchType]
    clear = PlayerTypes[0]==PlayerTypes[0]==Pl.PlayerType.HUMAN
    playerArray=[]
    for ind in (0,1):
        playerArray.append(Pl.Player(PlayerTypes[ind],playerNames[ind]))
    seed() #randomly choose which player will start (has index 0), but can be decided before (look config) givin prio
    l = [lambda x: x[::-1], lambda x: x] 
    return gridArray, choice(l)(playerArray),clear #two arrays of 2 elements each
def updateGlobalStats(stats):
    pass

if __name__ == "__main__":#this will be also the shape of the main thread on the django server
    
       
    #in case of start..
    grids, players, clear = initGame(2,["andrea","computer"],m.VERSUS_PC,s.FILE_LOCAL)
    # all above args of init are taken from config files or others, not hardcoded
    config = {
        "uiMode" : i.CLI, #args or ask prompt..
        "dataMode" : s.FILE_LOCAL ,
        "distance" : 1, # taken from config
        "radius" : 0, # taken from config, too
        "LetCol" : True, # idem as above
        "outputPC" : True,
        "clear": True#clear
    }
    gameEnded = False
    stats = None #global stats 
    threads=[None,None]
    #workers (in django assigned to clients..)
    threads[0] =  Action(0, grids, players, config) #mettere un po' di roba in un dcit o altro x ridurre args?
    threads[1] =  Action(1, grids, players, config) #notnecessarily args are equal, in case always sintetizza..
    threads[0].start()
    threads[1].start()
    for x in threads: 
        x.join()
    updateGlobalStats(stats)
