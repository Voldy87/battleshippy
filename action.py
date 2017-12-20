import threading

class Action(threading.Thread):
    def __init__(self, index, grids, players, turn, cv): 
        threading.Thread.__init__(self) 
        self.grids = grids
        self.index = index
        self.ui = ui
        self.players = players
        self.turn = turn #in one turn each player takes a shot
        self.cv = cv
    def run(self):
        ownGrid, othersGrid = grids[index], grid[1-index]
        ui.startSplash()
        vett = askShipNamesAndCoord()
        ownGrid.shipsPositioning(vett)
        ownGrid.render(False)
        while True : 
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
            if (ownGrid.allSinked or othersGrid.allSinked) :
                cv.notify()
                cv.release()
                break
            while not turn==index:
                cv.wait()
            isAI = (player.nature == "PC")
            if (isAI):
                pos = player.computerTarget()
            else: 
                showLastEnemyShotUpcome()
                ownGrid.render(False)
                pos = askTarget()
            shotResult = othersGrid.takeShot(pos)
            if (not isAI):
                showLastOwnShotUpcome(shotResult)
                othersGrid.render(False)
            turn = 1-index
            cv.notify()
            cv.release()
        showResults(uiMode)
        ownGrid.render(True)
        othersGrid.render(True)
        finishSplash()
