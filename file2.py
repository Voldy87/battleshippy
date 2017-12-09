from texttable import Texttable

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
        self.slots = [0,0]*(squaresNum) # [0,n] empty slot hit n times before (also 0); [id,n] slot with ship id hit n times before (if n==-1 sinked ship)
    
class Grid(SeaMap) :
    "The grid of a player, with his/her ships"
    def __init__ (self,dim):
        SeaMap(dim)
        self.void = True
        self.ships = None
    def renderCLI(): #var def have to go outisde gthis fun
        letters = list(map(chr, range(65, 91)))
        numbers = list(range(1,100,1))
        t = Texttable()
        t.add_rows([ ['', letters[0:4]], [letters[0], ''], [letters[0], ''],[letters[0], ''],[letters[0], ''] ]) #use a generator or something similar to avoid all this arrays...
        print(t.draw())
    def assignToPlayer (player):
        self.player = player
    def updateSlot (pos,val):
        index = pos.x * pos.y
        self.slots[index]=val
    def addShip (vessel,*pos): # variable length argument list for functions
        self.ships.push(vessel)
        shipIndex = self.ships[-2:-1]; # list slicing using negative indexing
        for item in pos:
            updateSlot(item, [shipIndex,0])
        self.void = False
    def takeShot(pos):
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
              
        
        
    def renderAllCli():
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
