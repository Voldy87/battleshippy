from texttable import Texttable
from colorama import init # call init() at start


from ship import Ship


class SeaMap :
    def __init__ (self, dim):
        self.dim = dim
        squaresNum = dim**2 #powers operator
        self.slots = [[0,0] for _ in range(squaresNum)] # [0,n] empty slot hit n times before (also 0); [id,n] slot with ship id hit n times before (if n==-1 sinked ship)
        print("Created grid with " + str(squaresNum) + " squares")
class Grid(SeaMap) :
    "The grid of a player, with his/her ships"
    cliSquareMap = { 'Void':'\x1b[44m', 'Ship':'\x1b[42m', 'Shot':['\x1b[0;31m',chr(216)], 'Sinked':'\x1b[45m' }
    def __init__ (self,dim):
        SeaMap.__init__(self,dim)
        self.void = True
        self.player = None
        self.ships = [] 
    def coordsValidateAndConvert(self,letter,number):
        if (len(locals())!=3):
            return False
        if (type(letter)!=str or type(number)!=int):
            return False
        letterAscii = ord(letter.upper())
        if ( (letterAscii not in range(65,65+self.dim)) or (number not in range(1,self.dim)) ):
            return False
        return [letterAscii-65,number-1]
    def getSquareCode(self,slot,show_ships): #fg/pre bg/mid let/post
        what = slot[0]
        shots = slot[1]
        pre=''
        post=' '
        mid =''
        if (shots<0):
            pre = self.cliSquareMap['Sinked']
            return (pre+mid+post+'\x1b[0m')
        elif (shots>0):
            post = self.cliSquareMap['Shot'][1]
            pre = self.cliSquareMap['Shot'][0]
        if (what==0)or(not show_ships and shots==0):
            mid = self.cliSquareMap['Void']
        else:
            mid = self.cliSquareMap['Ship']
        return (pre+mid+post+'\x1b[0m')
    def printCli(self, enemyview): #var def have to go outisde gthis fun
        dim = self.dim
        letters = list(map(chr, range(65, 91)))
        row_one = [''] + letters[0:dim]
        rows = [row_one]
        for x in range(0,dim): #each row after the header one (that has letters)
            temp = [x+1]
            for y in range(0,dim): #each column
                temp.append(self.getSquareCode(self.slots[(x*dim)+y],not enemyview))
            rows.append(temp)
        t = Texttable()
        t.add_rows(rows) #use a generator or something similar to avoid all this arrays...
        print(t.draw())
    def addShip (self,vessel,*pos): # variable length argument list for functions
        self.ships.append(vessel)
        shipIndex = len(self.ships)-1
        for item in pos:
            self.slots[item[0] * self.dim + item[1]] = [shipIndex+1,0]
        self.void = False
    def takeShot(self,pos):
        index = pos[0] * self.dim + pos[1]
        shipID = self.slots[index][0]
        shotsNum = self.slots[index][1]
        self.slots[index][1] += 1
        slotStatus = "empty"
        isSinked = False
        if (shipID == 0): # no ship in slot
            pass
        else:   # a ship is placed in this slot
            slotStatus = "full"    
            if (shotsNum<0): #there was a ship here, but it was already sinked when it got this shot
                isSinked = True
                self.slots[index][1] -= 1
            elif (shotsNum==0 and self.ships[shipID-1].getShot()): # just sinked the ship!
                isSinked = True
                for i in range(0,self.dim**2):
                    if (self.slots[i][0]==shipID): 
                        self.slots[i][1] = -1
        return {"slot":slotStatus, "sinked":isSinked, "hitNumber":shotsNum+1}          
    def sinkedShips(self):
        return list(filter(lambda x : x.sinked==True, self.ships))
    def allSinked(self):
        return len(sinkedShips())==len(self.ships)
    def drawGraph():
        pass
    def updateGraph():
        pass
    def renderFirst(self, uiType, enemyView):
        if (uiType=="cli"):
            printCli(enemyView)
        else:
            drawGraph(enemyView)
    def renderUpdate(self, uiType, enemyView):
        if (uiType=="cli"):
            printCli(enemyView)
        else:
            updateGraph(enemyView)

init()
g = Grid(4)
g.printCli(False)
s = Ship("cargo",4)
g.addShip(s, [1,1],[1,2],[1,0],[1,3])
g.printCli(False)
g.takeShot([1,1])
g.printCli(False)
g.takeShot([3,1])
g.printCli(False)
g.takeShot([1,2])
g.takeShot([1,0])
g.takeShot([1,0])
g.printCli(False)
g.takeShot([1,3])
g.printCli(False)
g.takeShot([3,3])
g.takeShot([3,3])
g.takeShot([0,3])
g.printCli(False)
print(g.coordsValidateAndConvert("A",2))
print(g.coordsValidateAndConvert("a",1))
print(g.coordsValidateAndConvert("A",23))
print(g.coordsValidateAndConvert("G",2))
print(g.coordsValidateAndConvert("t",1))
print(g.coordsValidateAndConvert("A",0))
print(g.coordsValidateAndConvert("C",3))
print(g.coordsValidateAndConvert(-1,-3))
