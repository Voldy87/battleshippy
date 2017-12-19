from random import seed,choice

from grid import Grid
from player import Player
from action import Action
from menu import Menu #optional??

def initGame (side,ships,players):
    grids = [Grid(side), Grid(side)]
    players = [Player("andrea","HUMAN"),Player("computer", "PC")]
    seed()
    l = [lambda x: x.reverse(), lambda x: None]
    choice(l)(players) #randomly choose which player will start (has index 0)
    return grids, players
def shipPositioning(index):
    vett = askShipNamesAndCoord()
    for s in vett:
        grids[index].ships.addShip(vett)

if __name__ == "__main__":#this will be also the main thread on the django server
    uiMode = "cli" #args or ask prompt..
        
    #in case of start..

    grids, players = initGame(10,[2,3,3,5])
    gameEnded = False, stats = None#global stats 
    condition = threading.Condition()
    turn = 0 #as in initGame player with 0 index starts
    for index in range(0,2): #workers (in django assigned to clients..)
        threads +=  Action(index, uiMode, grids, players, turn, condition)
        threads[index].start()
    for x in threads: 
        x.join()
    updateGlobalStats(stats)        

