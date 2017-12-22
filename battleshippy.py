from random import seed,choice
import threading

from grid import Grid
from players import Player
from action import Action
#from menu import Menu #optional??


def initGame (side,players,uiMode):
    grids = [Grid(side,uiMode), Grid(side,uiMode)]
    players = [Player("andrea","HUMAN"),Player("computer", "PC")]
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
