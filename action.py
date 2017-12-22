import threading
from cli import CLI
from gui import GUI
#from data import DataDb, DataFile

turn = 1
cv = threading.Condition()

class Action(threading.Thread):
    def __init__(self, index, grids, players, uiMode, dataMode): 
        threading.Thread.__init__(self) 
        self.grids = grids
        self.index = index
        if(uiMode=="cli"):
            self.ui=CLI()
        else:
            self.ui=GUI()
##       if(dataMode=="localDB" || dataMode=="remoteDB"):
##            self.data=DataDb()
##        else:
##            self.data=DataFile()
        self.players = players
        #currentPlayer=0 #always start first in Players array (random choice in main)
        #self.turn = 1 #in one turn each player takes a shot
        #self.cv = cv
    def getShipNamesAndCoord(self, grid, shipsToGive):
        vett=[]
        for elem in shipsToGive: #elem = ship,dim
            while True:
                coords = self.ui.askShip(elem)
                if (grid.posChecker(coords)):
                    break
            vett.append(elem.ship,pos)
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
##        vett = UI.getShipNamesAndCoord(ownGrid, shipsToGive) #ships to give depend on config
##        ownGrid.shipsPositioning(vett)
##        UI.render(ownGrid,True,False)
            
        for i in range(1,20):#while not otherGrid.allSinked() : 
            #global currentPlayer
##          if (ownGrid.lastShotInfo):
##              UI.shotUpcome(ownGrid.lastShotInfo) #if there are not shots (1st turn 1st player does nothing and pass diectly to take shot vs enemy
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
