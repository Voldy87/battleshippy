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
turn = ui = None #togliere omonomia
cv = threading.Condition()
interrupted = None #index of the player who retired or anyway exited abruptly (thus losing),in this case is updated and put in stats
newgame = True


class Action(threading.Thread):
    def __init__(self, index:int, grids:list, players:list, stats:object, config:dict): 
        threading.Thread.__init__(self) 
        self.index = index
        self.myGrid, self.enemyGrid = grids[index], grids[1-index] #deve puntare all'array di 2 griglie
        self.me, self.enemy = players[index], players[1-index]
        self.isPC =  players[index].nature is p.PC
        self.output = config["outputPC"] or not self.isPC #may be different, e.g. in a 2 pc battle one wants to see what happens (consider introducing a delay)
        self.minShipDistance = config["distance"] #all these are equal for all thread maybe we can keep them global and don't pass
        self.shotRadius = config["radius"]["area"]
        self.numRadius = config["radius"]["num"]
        self.letCol = config["LetCol"]
        self.clear = config["clear"]
        self.stats=stats#ridonda la roba sopra (ttt in config??)
        self.AIstrategy = {"ship":config["shipAI"],"shoot":config["shootAI"]}
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
                ui.insertedSplash(self.myGrid)
                coords = ui.askSingleShip(side,vessel)
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
    def endgame(self): #classic game end(allsunk), more explici namethus?
        return self.myGrid.allSinked() or self.enemyGrid.allSinked()
    def updateShotStats(self,coord,radius):
        self.stats['moves'].append([coord,radius]) #store shoot coordinate
    def updateGridStats(self):
        self.stats['startingGrids'][self.index]=self.myGrid.ships #ships are enough to stat, giving all the subsequent shots
    def updateRetiredStats(self):
        self.stats['interrupted']=interrupted
    def run(self):
        global ui
        UI = ui
        global interrupted
        interrupted = -1
        while not self.enemyGrid.allSinked() and interrupted==-1:
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
            while not self.checkFlag() and interrupted==-1:
                cv.wait()
            if self.currentTurn()==0: #"turn 0": ship positioning
                if self.output:
                    UI.startSplash(self.me.name,self.index==0)
                if self.isPC :
                    self.shipsAutoPositioning(self.AIstrategy['ship'])
                else:
                    self.shipsManualPositioning()
                self.updateGridStats()
                if self.output:
                    UI.gridSplash(self.me.name)
                    UI.renderGrid(self.myGrid,True,False)
                if not self.verifyPositioning():
                    raise Exception('Ship positioning failed')
                if self.output:
                    UI.battleSplash(self.me.name)
            else: #"normal turn"
                if self.output:
                    UI.turnSplash(self.me.name,self.currentTurn())
                if turn>=3 and interrupted==-1: #enemy shot result
                    shooting_result = self.me.reactToShot(self.myGrid.lastShotInfo,False)
                    coords, victory = self.myGrid.lastShotInfo['coords'], self.myGrid.allSinked()
                    if self.output:
                        UI.shotUpcome(self.me.name,coords,shooting_result,victory, False,self.letCol) #enemy's last shot info
                        UI.renderGrid(self.myGrid,True,True)
                    if not self.isPC and not self.endgame():
                        if UI.askRetire():
                            interrupted=self.index
                    if interrupted!=(-1):
                        self.updateRetiredStats()
                if self.myGrid.allSinked() or interrupted!=(-1):
                    cv.notify()
                    cv.release()
                    break
                pos = None
                if self.isPC :
                    pos = self.me.computerTarget(self.enemyGrid.slots,self.AIstrategy['shoot'])
                    OnlyNum = True
                else: 
                    UI.shootSplash(self.me.name) 
                    UI.renderGrid(self.enemyGrid,False,False)
                    pos = UI.askTarget(self.enemyGrid.dim) #gestione radius, da fare
                    OnlyNum = False
                shotCoord = self.enemyGrid.shoot(pos,self.shotRadius,OnlyNum) #radius, if enabled by this variable, can be used (always, liimited, etc..) so this arg changes
                self.updateShotStats(shotCoord,self.shotRadius)
                shooting_result = self.me.reactToShot(self.enemyGrid.lastShotInfo)
                if self.output:#my shot result
                    coords, victory = self.enemyGrid.lastShotInfo['coords'], self.enemyGrid.allSinked()
                    UI.shotUpcome(self.me.name,coords,shooting_result,victory,True,self.letCol)
                    UI.renderGrid(self.enemyGrid,False,True)
            if self.output and self.clear and not self.endgame(): #in case players share terminal (hum vs hum) one cannot see the others grids!
                UI.changeSplash(self.me.name,self.enemy.name,5*int(self.clear),3*int(self.clear))#the last two values depend on game type
            self.changeFlag()
            cv.notify()
            cv.release()
        if self.output:
            UI.resultSplash(self.me.name,self.enemyGrid.allSinked(),self.myGrid.allSinked(),interrupted==self.index)

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

if __name__ == "__main__":#this will be also the shape of the main thread on the django server, the server etc...
    # all above args of init are taken from config files or others (e.g. ask before starting), not hardcoded 
    config = {
        "side": 2,
        "type":m.VERSUS_HUMAN,
        "names":["andrea","computer"], #always human before, otherwise alphabetical order
        "uiMode" : i.CLI, #args or ask prompt..
        "dataMode" : s.FILE_LOCAL ,
        "distance" : 1, # taken from config
        "radius" : {
            "area":0,
            "num":0
        }, # taken from config, too
        "LetCol" : True, # idem as above
        "outputPC" : False,
        "clear": True,#dipende dal tipo di partita!?(confgi..),
        "shipAI":"basic",
        "shootAI":"basic"
    }
    ##       if(dataMode=="localDB" || dataMode=="remoteDB"): #these stuff can not be decided by player at RT
    ##            self.data=DataDb()
    ##        else:
    ##            self.data=DataFile()
    #in case of start..
    tempCLI=CL.CLI() #ask gui first time at console (other way to add invoking this and config via cli launching executable..bisogna pensarci)
    config["uiMode"]=tempCLI.askUI()
    if config["uiMode"] is i.CLI:
        ui=tempCLI
    elif config["uiMode"] is i.GUI:
        ui=CL.GUI()
        del tempCLI
    else:
        exit(1)#better an exception 
    ui.enterSplash()
    while (newgame):    
        #UI.askConfig(config)#don't ask storage, interface(CL), etc..
        grids, players, clear = initGame(config["side"],config["names"],config["type"],config["dataMode"])
        gameEnded = False
        stats = {
            "gameConfig":{#only configs utili per le stats
                "distance":config["distance"],
                "radius":config["radius"]
            },
            "players":players,
            "startingGrids":[None,None],
            "moves":[],
            "interrupted":None
        } #global stats 
        threads=[None,None]
        #workers (in django assigned to clients..)
        threads[0] =  Action(0, grids, players, stats, config) #mettere un po' di roba in un dcit o altro x ridurre args?
        threads[1] =  Action(1, grids, players, stats, config) #notnecessarily args are equal, in case always sintetizza..
        threads[0].start()
        threads[1].start()
        for x in threads: 
            x.join()
        ui.finalSplash()
        for ind in (0,1):
            ui.endgridsSplash(players[ind].name)
            ui.renderGrid(grids[ind],True,False)
        ui.finishSplash()
        updateGlobalStats(stats) #write stats somewhere
        newgame = not ui.askExit()
    ui.exitSplash()
