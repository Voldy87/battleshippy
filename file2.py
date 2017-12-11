from texttable import Texttable
from colorama import init # call init() at start

def validatePos (pos):
        pass
class Ship:
    "A battleship"
    def __init__ (self, name, player, length):
        self.name = name
        self.length = length
        self.hitCount = 0
        self.sinked = False
    def getShot ():
        self.hitCount += 1
        self.sinked = (self.hitCount>=self.length)
        return self.sinked

class SeaMap :
    def __init__ (self, dim):
        self.dim = dim
        squaresNum = dim**2 #powers operator
        self.slots = [[0,0]]*(squaresNum) # [0,n] empty slot hit n times before (also 0); [id,n] slot with ship id hit n times before (if n==-1 sinked ship)
        print("Created grid with " + str(squaresNum) + " squares")
class Grid(SeaMap) :
    "The grid of a player, with his/her ships"
    cliSquareMap = { 'Void':'\x1b[44m', 'Ship':'\x1b[42m', 'Shot':['\x1b[0;31m',chr(216)], 'Sinked':'\x1b[45m' }
    def __init__ (self,dim):
        SeaMap.__init__(self,dim)
        self.void = True
        self.ships = None
    def getSquareCode(self,slot): #fg/pre bg/mid let/post
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
        if (what==0):
            mid = self.cliSquareMap['Void']
        else:
            mid = self.cliSquareMap['Ship']
        return (pre+mid+post+'\x1b[0m')
    def renderCLI(self): #var def have to go outisde gthis fun
        dim = self.dim
        letters = list(map(chr, range(65, 91)))
        row_one = [''] + letters[0:dim]
        rows = [row_one]
        for el in range(0,dim): #each row after the header one (that has letters)
            temp = [el+1]
            for x in range(0,dim): #each column
                temp.append(self.getSquareCode(self.slots[(el*x)+x]))
            rows.append(temp)
        t = Texttable()
        t.add_rows(rows) #use a generator or something similar to avoid all this arrays...
        #print(rows)
        print(t.draw())
    def assignToPlayer (self,player):
        self.player = player
    def updateSlot (self,pos,val):
        index = pos.x * pos.y
        self.slots[index]=val
    def addShip (self,vessel,*pos): # variable length argument list for functions
        self.ships.push(vessel)
        shipIndex = self.ships[-2:-1]; # list slicing using negative indexing
        for item in pos:
            updateSlot(item, [shipIndex,0])
        self.void = False
    def takeShot(self,pos):
        index = pos.x * pos.y
        slotState = self.slots[index][0]
        slotNum = self.slots[index][1]
        if (slotState == 0): # no ship in slot
            updateSlot (pos,[slotState,slotHits+1])
            return {"slot":"empty", "already":True}
        else:   # a ship is placed in this slot
            sinked = False
            if (slotNum<0):
                sinked = True
            else: # the ship is still there
                if (self.ships[slotState].getShot()): # just sinked the ship!
                    sinked = True
                    updateSlot (pos,[slotState,-1])
                else:
                    updateSlot (pos,[slotState,slotNum+1]) # ship damaged but not yet sinked
            return {"slot":"full", "ship":hitShip, "sinked":shipstate, "hitNumber":slotNum}
               
    def renderAllCli(self):
        len = dim+1
    def drawGraph():
        pass
    def updateGraph():
        pass
    def renderAll(mode, uiType):
        if (mode=="cli"):
            renderAllCli()
        else:
            drawGraph()
    def renderUpdate(mode, uiType):
        if (mode=="cli"):
            renderAllCli()
        else:
            updateGraph()

init()
g = Grid(4)
g.renderCLI()
