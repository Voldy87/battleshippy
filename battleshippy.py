from random import seed,choice

from grid import Grid
from player import Player
from action import Action
from menu import Menu #optional??

def initGame (side,players,uiMode):
    grids = [Grid(side,uiMode), Grid(side,uiMode)]
    players = [Player("andrea","HUMAN"),Player("computer", "PC")]
    seed()
    l = [lambda x: x.reverse(), lambda x: None]
    choice(l)(players) #randomly choose which player will start (has index 0)
    return grids, players


if __name__ == "__main__":#this will be also the main thread on the django server
    uiMode = "cli" #args or ask prompt..
        
    #in case of start..

    grids, players = initGame(10,[2,3,3,5],uiMode)
    gameEnded = False, stats = None#global stats 
    condition = threading.Condition()
    turn = 0 #as in initGame player with 0 index starts
    for index in range(0,2): #workers (in django assigned to clients..)
        threads +=  Action(index, uiMode, grids, players, turn, condition)
        threads[index].start()
    for x in threads: 
        x.join()
    updateGlobalStats(stats)        

