from operator import itemgetter
from common.utils.grid import coordsConvert,coordsValidate, coordsEndpoints, squaresAlignment

from common.game.ship import Ship

class SeaMap :
    def __init__ (self, dim): #in future a rectangular grid??
        ''' Constructor for this class. Only square side needed.
            - dim (positive integer): side of the square grid (has dim^2 slots)
            - slots matrix (list of list):
                - [0,n>0] empty slot hit n times before (also 0);
                - [id>0,n] slot with ship id hit n times before (if n<0 sinked ship hit |n| times in this slot)'''
        if dim<=0 :
            raise Exception('Non-positive length')
        self.dim = dim
        self.slots = [ [[0,0] for x in range(dim)] for y in range(dim) ] 
        #print("Created grid with " + str(dim**2) + " squares")

class Grid(SeaMap) :
    "The grid of a player, with his/her ships"
    def __init__ (self,dim, LetCol=True):
        ''' Constructor for this class: side, empty flag, ships list, map information about last shot taken on.'''
        SeaMap.__init__(self,dim)
        self.letCol = LetCol
        self.void = True
        self.lastShotInfo = dict()
        self.lastAreaShotInfo = []
        self.ships = []
    def clear(self):
        SeaMap.__init__(self,self.dim)
        self.void = True
        self.lastShotInfo = dict()
        self.lastAreaShotInfo = []
        self.ships = []
    def coordsValidateAndConvert(self,vett,ToNum=True):
        if coordsValidate(self.dim,vett):
            return coordsConvert(vett,ToNum,self.letCol)
        else:
            return False
    def posChecker (self, distance, AlphaNumPositions):
        '''Check is a set of positions for a ship is acceptable, giving a distance from other ships,
        using alphanumerical input coordinates'''
        num = len(AlphaNumPositions)
        if (num==0):
            return True
        if (any(AlphaNumPositions.count(x) > 1 for x in AlphaNumPositions)): #all coords given are unique
            return False
        NumericPositions = []
        for spam in AlphaNumPositions: #single point is valid and free?
            coords = self.coordsValidateAndConvert(spam)
            if (not coords): #invalid coordinate
                return False
            if (distance==0):
                if (self.slots[coords[0]][coords[1]][0]!=0):
                    return False #slot already bearing a part of a ship
            else:
                x,y = coords
                lim = self.dim
                for i in range(-distance,distance+1):
                    for j in range(-distance,distance+1):
                        if (x+i in range(0,lim)) and (y+j in range(0,lim)) and (self.slots[x+i][y+j][0]!=0):
                            return False #slot already bearing a part of a ship
            NumericPositions.append(coords)  
        if (num==1):
            return (self.slots[0][0][0]==0)
        if (NumericPositions[0][0]==NumericPositions[1][0]): #check if ship is placed horizional or vertical
            index = 1
        elif (NumericPositions[0][1]==NumericPositions[1][1]):
            index = 0
        else:
            return False #not consecutive coordinates
        sortedPos = sorted(NumericPositions, key=itemgetter(index))
        if( sortedPos[num-1][1-index] != sortedPos[0][1-index] ):
            return False #not consecutive coordinates
        if( sortedPos[num-1][index] - sortedPos[0][index] != (num-1) ):
            return False #not consecutive coordinates
        return True              
    def addShip (self,vessel,pos,NumericCoord=False): # variable length argument list for functions
        '''Given a single ship and its coordinates put it on the grid, checking
        if coordinates are of the correct number and valid'''
        if vessel.length != len(pos) or vessel.length not in range (1,self.dim+1): #ship too long, not enough or too many coordinates for this ship
            return False
        if not NumericCoord: #format of the coordinates given for the ship
            coords = []
            for spam in pos :
                temp = self.coordsValidateAndConvert(spam)
                if temp :
                    coords.append(temp)
                else :
                    coords = [False]
                    break
            if False in coords: #never fails as the coords validity is checked before invoking this function
                return False
        else:
            coords = pos
        if squaresAlignment(coords)=="D":
            return False
        self.ships.append({"vessel":vessel,"ends":coordsEndpoints(coords)})
        shipIndex = len(self.ships)
        for [x,y] in coords:
            self.slots[x][y] = [shipIndex,0]
        self.void = False
        return True
##    def shipsPositioning(self,vett,NumericCoord):
##        for spam in vett:
##            pos = spam["coords"]
##            if not self.addShip(Ship(spam["name"],len(pos)), pos,NumericCoord):
##                return False
    def takeShot(self,coord,OnlyNum=True):
        '''Modify the grid slot matrix, updating the lastShotInfo member,
           which stores the coordinates in numeric (double 0-indexed matrix) format'''
        if OnlyNum:
            x = coord[0]
            y = coord[1]
        else:
            x,y=self.coordsValidateAndConvert(coord)
        shipID = self.slots[x][y][0]
        shotsNum = self.slots[x][y][1]
        self.slots[x][y][1] += 1
        if (shipID == 0): # no ship in slot
            pass
        else:   # a ship is placed in this slot   
            if (shotsNum<0): #there was a ship here, but it was already sinked when it took this shot
                self.slots[x][y][1] = shotsNum-1
            elif (shotsNum==0 and self.ships[shipID-1]["vessel"].getShot()): # just sinked the ship!
                for xx in range(0,self.dim):
                    for yy in range(0,self.dim):
                        if (self.slots[xx][yy][0]==shipID): 
                            self.slots[xx][yy][1] = -1
        self.lastShotInfo = {"coords":{"x":x,"y":y}, "slot":self.slots[x][y], "allSinked":self.allSinked()}
        return True;
    def shoot(self,coord,radius=0,OnlyNum=False):
        '''Launch a shoot (area effect if 3rd arg >0) centered to the given coordinate (alphanumeric notation)'''
        if (radius<0):
            return False
        self.lastAreaShotInfo = [] #both in case of single (remains void) or area (new array of lastshotinfo) this var needs to be voided
        if not OnlyNum:
            pos = self.coordsValidateAndConvert(coord,not OnlyNum) #two possible directions for the conversion
        else:
            pos = coord
        if (not pos):
            return False
        if (radius==0):
            self.takeShot(pos)
        else: #area shot
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    target = [ pos[0]+x , pos[1]+y ]
                    if (coordsValidate(self.dim,target,True)):
                        self.takeShot(target)
                        self.lastAreaShotInfo.append(self.lastShotInfo)
        return pos #numeric coordinate of shot (or central if radius is active)
    def sinkedShips(self):
        return list(filter(lambda x : x["vessel"].sinked==True, self.ships))
    def allSinked(self):
        if self.void: #check at turn 0, when no ships have been positioned
            return False
        return len(self.sinkedShips())==len(self.ships)
