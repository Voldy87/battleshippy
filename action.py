import threading

class Action(threading.Thread):
    def __init__(self, index, uiMode, grids, players, turn, cv): 
        threading.Thread.__init__(self) 
        self.grids = grids
        self.index = index
        self.uiMode = uiMode
        self.players = players
        self.turn = turn
        self.cv = cv
    def run(self):
        ownGrid, othersGrid = grids[index], grid[1-index]
        if (self.uiMode = "cli"):
            cliStart()
        else:
            enableMenu()
        disableMenu() #partial...
        startSplash(uiMode)
        Positioning(ownGrid)
        ownGrid.renderFirst(uiMode) 
        othersGrid.renderFirst(uiMode)
        while True : 
            cv.acquire() #consider not blocking interaction for all block if not ciritcal, especially in GUI
            if ownGrid.allSinked or othersGrid.allSinked:
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
                ownGrid.renderUpdate(uiMode)
                pos = askTarget()
            shotResult = othersGrid.takeShot(pos)
            if (not isAI):
                showLastOwnShotUpcome(shotResult)
                othersGrid.renderUpdate(uiMode)
            turn = 1-index
            cv.notify()
            cv.release()
        showResults(uiMode)
        finishSplash(uiMode)
