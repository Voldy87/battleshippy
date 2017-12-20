from operator import itemgetter

from cli import CLI
from gui import GUI
from ship import Ship


class SeaMap :
    def __init__ (self, dim): #in future a rectangular grid??
        self.dim = dim
        self.slots = [ [[0,0] for x in range(dim)] for y in range(dim) ] # [0,n] empty slot hit n times before (also 0); [id,n] slot with ship id hit n times before (if n==-1 sinked ship)
        print("Created grid with " + str(dim**2) + " squares")
class Grid(SeaMap) : 
    "The grid of a player, with his/her ships"
    def __init__ (self,dim,uiType):
        SeaMap.__init__(self,dim)
        self.void = True
        self.player = None
        self.ships = []
        if(uiType=="cli"):
            self.ui=CLI(dim)
        else:
            self.ui=GUI(dim)
    def coordsValidateAndConvert(self,letter,number):
        if (len(locals())!=3):
            return False
        if (type(letter)!=str or type(number)!=int):
            return False
        letterAscii = ord(letter.upper())
        if ( (letterAscii not in range(65,65+self.dim)) or (number not in range(1,self.dim+1)) ):
            return False
        return [letterAscii-65,number-1]
    def posChecker (self,*AlphaNumPositions):
        '''Check is a set of positions for a ship is acceptable: first coordinates validity,
then square availability'''
        num = len(AlphaNumPositions)
        if (num==0):
            return True
        NumericPositions = []
        for [letter,number] in AlphaNumPositions: #single point is valid and free?
            coords = self.coordsValidateAndConvert(letter,number)
            if (not coords):
                print("INVALID")
                return False
            if (self.slots[coords[0]][coords[1]][0]!=0):
                print("BUSY")
                return False
            NumericPositions.append(coords)  
        if (num==1):
            return (self.slots[0][0][0]==0)
        if (NumericPositions[0][0]==NumericPositions[1][0]): #check if ship is placed horizional or vertical
            index = 1
        elif (NumericPositions[0][1]==NumericPositions[1][1]):
            index = 0
        else:
            print("DIAG")
            return False
        sortedPos = sorted(NumericPositions, key=itemgetter(index))
        if( sortedPos[num-1][index] - sortedPos[0][index] != (num-1) ):
            print("LEN")
            return False #points are consecutive?
        return True              
    def addShip (self,vessel,*pos): # variable length argument list for functions
        #convert coords from let/num to [0-n][0-n]
        self.ships.append(vessel)
        shipIndex = len(self.ships)-1
        for [x,y] in pos:
            self.slots[x][y] = [shipIndex+1,0]
        self.void = False
    def shipsPositioning(self,vett):
        for spam in vett:
            self.ships.addShip(spam) #elem = ship,pos
    def askShipNamesAndCoord(self, shipsToGive):
        vett=[]
        for elem in shipsToGive: #elem = ship,dim
            while (not self.posChecker(self.ui.askShip(elem.dim))):
                pass
            vett.append(elem.ship,pos)
        return vett #every elem has ship(maybe only name and len?) and position
    def takeShot(self,pos):
        x = pos[0]
        y = pos[1]
        shipID = self.slots[x][y][0]
        shotsNum = self.slots[x][y][1]
        self.slots[x][y][1] += 1
        slotStatus = "empty"
        isSinked = False
        if (shipID == 0): # no ship in slot
            pass
        else:   # a ship is placed in this slot
            slotStatus = "full"    
            if (shotsNum<0): #there was a ship here, but it was already sinked when it got this shot
                isSinked = True
                self.slots[x][y][1] -= 1
            elif (shotsNum==0 and self.ships[shipID-1].getShot()): # just sinked the ship!
                isSinked = True
                for x in range(0,self.dim):
                    for y in range(0,self.dim):
                        if (self.slots[x][y][0]==shipID): 
                            self.slots[x][y][1] = -1
        return {"slot":slotStatus, "sinked":isSinked, "hitNumber":shotsNum+1}          
    def sinkedShips(self):
        return list(filter(lambda x : x.sinked==True, self.ships))
    def allSinked(self):
        return len(sinkedShips())==len(self.ships)
    def render(self, enemyView):
        ui.print(enemyView) #gui first time draw, others update
            
dim = 4
g = Grid(dim,"cli")
c = CLI(dim)
c.print(g.slots,False)
s = Ship("cargo",4)
g.addShip(s, [1,1],[1,2],[1,0],[1,3])
c.print(g.slots,False)
g.takeShot([1,1])
c.print(g.slots,False)
g.takeShot([3,1])
c.print(g.slots,False)
g.takeShot([1,2])
g.takeShot([1,0])
g.takeShot([1,0])
c.print(g.slots,False)
g.takeShot([1,3])
c.print(g.slots,False)
g.takeShot([3,3])
g.takeShot([3,3])
g.takeShot([0,3])
c.print(g.slots,False)
print(g.coordsValidateAndConvert("A",4))
print(g.coordsValidateAndConvert("a",1))
print(g.coordsValidateAndConvert("A",23))
print(g.coordsValidateAndConvert("G",2))
print(g.coordsValidateAndConvert("t",1))
print(g.coordsValidateAndConvert("A",0))
print(g.coordsValidateAndConvert("C",3))
print(g.coordsValidateAndConvert(-1,-3))
gg = Grid(dim,"cli")
print(gg.posChecker(["B",4],["B",1],["B",3],["B",2]))
print(gg.posChecker(["B",1],["B",3],["B",2]))
print(gg.posChecker(["D",2],["D",3]))
print(gg.posChecker(["C",2],["D",2],["B",2]))
print(gg.posChecker(["A",2],["D",2]))
print(gg.posChecker(["A",2],["A",4],["A",3],["A",1]))
print(gg.posChecker([12,2],["2",2],[0,2]))
print(gg.posChecker(["C",1],["B",3],["A",2]))

c.print(gg.slots,False)
