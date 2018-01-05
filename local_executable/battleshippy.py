# python -m local_executable.battleshippy

import common.game.grid as Gr
import common.game.player as Pl
import common.interface.cli as CL, common.interface.gui as GU
##import common.interface.menu as ME
##import common.data.db as DB, common.data.file as FI 

import threading
from random import seed,choice


turn = 1
cv = threading.Condition()

class Action(threading.Thread):
    def __init__(self, index, grids, players, uiMode, dataMode): 
        threading.Thread.__init__(self) 
        self.grids = grids
        self.index = index
        if(uiMode=="cli"):
            self.ui=CL.CLI()
        else:
            self.ui=CL.GUI()
##       if(dataMode=="localDB" || dataMode=="remoteDB"):
##            self.data=DataDb()
##        else:
##            self.data=DataFile()
        self.players = players
        #currentPlayer=0 #always start first in Players array (random choice in main)
        #self.turn = 1 #in one turn each player takes a shot
        #self.cv = cv
    def computeShipNamesAndCoord(self, index, shipsToGive, distance):
        for elem in shipsToGive: #elem = ship,dim
            coords = self.players[self.index].computerShip(elem.dim,distance,grids[self.index])
            vett.append(elem.ship,pos)
        return vett
    def getShipNamesAndCoord(self, shipsToGive, distance):
        vett = self.ui.askAllShips(self.grids.dim, ships)
        if (vett==None):
            vett=[]
        else:
            return vett #e.g. django gui wait for positioning
        for elem in shipsToGive: #elem = Ship
            while True:
                coords = self.ui.askSingleShip(self.grids.dim,elem)
                if (grids[self.index].posChecker(distance,coords)):
                    break 
            vett.append([elem.ship,coords])
        return vett #every elem has ship(maybe only name and len?) and position
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
##        ownGrid, othersGrid = self.grids[self.index], self.grids[1-self.index]
##      UI = self.ui
     ##   UI.startSplash()
        ## if (player.nature == "PC"):
##                vett = self.computeShipNamesAndCoord( shipsToGive, 0)
       ##         ownGrid.shipsPositioning(vett) 
##            else: 
##                 vett = self.getShipNamesAndCoord(shipsToGive, 0) #ships to give depend on config
##                  ownGrid.shipsPositioning(vett)
##                  UI.render(ownGrid,True,False)
            
        for i in range(1,20):#while not otherGrid.allSinked() : 
            #global currentPlayer
##          if (ownGrid.lastShotInfo):
##              UI.shotUpcome(ownGrid.lastShotInfo) #if there are no shots (1st turn 1st player does nothing and pass diectly to take shot vs enemy
##              UI.render(ownGrid,True,True)
            print("I AM "+str(self.index) + " and this is turn " + str(self.currentTurn()) +" \n")
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
##            if (ownGrid.allSinked()) :
##                  cv.notify()
##                    cv.release()
##                break
            while not self.checkFlag():
                print(str(self.index) + " waits for its turn\n")
                cv.wait()
            #self.tt+=1
            print(str(self.index) + " IS DOIG THINGS\n")
##            if (player.nature == "PC"):
##                pos = player.computerTarget()
##            else: 
##                pos = UI.getTarget()
##              otherGrid.takeShot(pos)
##              UI.shotUpcome(otherGrid.lastShotInfo)
    ##            UI.render(othersGrid,False,True)
            self.changeFlag()
            cv.notify()
            cv.release()
##        UI.showResults()
##        UI.render(ownGrid,True,False)
##        UI.render(othersGrid,True,False)
##        UI.finishSplash()


def initGame (side,players,uiMode):
    grids = [Gr.Grid(side), Gr.Grid(side)]
    players = [Pl.Player("andrea","HUMAN"),Pl.Player("computer", "PC")]
    seed()
    l = [lambda x: x.reverse(), lambda x: None]
    choice(l)(players) #randomly choose which player will start (has index 0)
    return grids, players
def updateGlobalStats(stats):
    pass

if __name__ == "__main__":#this will be also the main thread on the django server
    uiMode = "cli" #args or ask prompt..
    dataMode = "localFile" # localDB, remoteFile, remoteDB    
    #in case of start..
    grids, players = initGame(10,[2,3,3,5],uiMode)
    gameEnded = False
    stats = None #global stats 
    threads=[None,None]
    #workers (in django assigned to clients..)
    threads[0] =  Action(0, grids, players, uiMode, dataMode)
    threads[1] =  Action(1, grids, players, uiMode, dataMode)
    threads[0].start()
    threads[1].start()
    for x in threads: 
        x.join()
    updateGlobalStats(stats)
