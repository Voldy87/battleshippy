from operator import itemgetter

#from ship import Ship
def coordsValidate(dim,vett,OnlyNum=False):
    '''Validate, for the given grid, a couple of coordinates (2nd argument) in one of the two
    possibile formats, letter+number or two numbers, decided by the 3rd argument); this function,
does not care of how coordinates refers to row and columns (unless the grid is square)'''
    if (len(vett)==0):
        return False
    if (OnlyNum):
        x,y = vett
        return ( x in range(0,dim) and y in range(0,dim) )
    else:
        letter, number = vett
        if ( type(letter)!=str or type(number)!=int ):
            return False
        letterAscii = ord(letter.upper())
        if ( (letterAscii not in range(65,65+dim)) or (number not in range(1,dim+1)) ):
            return False
        return True
def coordsConvert(vett,ToNum=True, LetCol=True): #to extend using class argument to locate alpahbet used for letter (now default A-Z)
    '''Convert coordinates for the given grid between two formats
    - AlphaNumeric  (letter + integer >0 intepreted as Col/Rig or viceversa, decided by 4th arg e.g. C3)
    - Numeric (double 0-indexed matrix, e.g. [2][0])
    The direction of the conversion is given by the third argument, which
    by default is false, thus making conversion as [A,12]=>[0,11] (default)'''
    l = [lambda x: x[::-1], lambda x: x]
    index = int(LetCol)
    if (ToNum):
        return l[index]([ vett[1]-1, ord(vett[0].upper())-65  ]) #e.g. ["B",3] => [1,1]
    else:
        l[index](vett)
        return [ chr(vett[0]+65).upper() , vett[1]+1  ] #e.g. [1,0] => ["A",2]
    
class SeaMap :
    def __init__ (self, dim): #in future a rectangular grid??
        ''' Constructor for this class. Only square side needed.'''
        self.dim = dim
        self.slots = [ [[0,0] for x in range(dim)] for y in range(dim) ] # [0,n] empty slot hit n times before (also 0); [id,n] slot with ship id hit n times before (if n==-1 sinked ship)
        #print("Created grid with " + str(dim**2) + " squares")

class Grid(SeaMap) :
    "The grid of a player, with his/her ships"
    def __init__ (self,dim, LetCol=True):
        ''' Constructor for this class: side, empty flag, ships list, map information about last shot taken on.'''
        SeaMap.__init__(self,dim)
        self.letCol = LetCol
        self.void = True
        self.lastShotInfo = dict()
        self.ships = []
    def clear():
        pass
    def coordsValidateAndConvert(self,vett):
        if coordsValidate(self.dim,vett):
            return coordsConvert(vett,self.letCol)
        else:
            return False
    def posChecker (self, distance, AlphaNumPositions):
        '''Check is a set of positions for a ship is acceptable, giving a distance from other ships'''
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
    def addShip (self,vessel,pos): # variable length argument list for functions
        '''Given a single ship and its coordinates put it on the grid, checking
        if coordinates are of the correct number and valid, but without checking
        if the space that they occupy is consecutive or free'''
        if vessel.length != len(pos) or vessel.length not in range (1,self.dim+1): #ship too long, not enough or too many coordinates for this ship
            return False
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
        self.ships.append(vessel)
        shipIndex = len(self.ships)-1
        for [x,y] in coords:
            self.slots[x][y] = [shipIndex+1,0]
        self.void = False
        return True
    def shipsPositioning(self,vett):
        for spam in vett:
            self.addShip(spam) #spam = ship,pos
    def takeShot(self,coord):
        '''Modify the grid slot matrix using the 0-index couple of coordinates'''
        x = coord[0]
        y = coord[1]
        shipID = self.slots[x][y][0]
        shotsNum = self.slots[x][y][1]
        self.slots[x][y][1] += 1
        if (shipID == 0): # no ship in slot
            pass
        else:   # a ship is placed in this slot   
            if (shotsNum<0): #there was a ship here, but it was already sinked when it got this shot
                self.slots[x][y][1] = -1
            elif (shotsNum==0 and self.ships[shipID-1].getShot()): # just sinked the ship!
                for xx in range(0,self.dim):
                    for yy in range(0,self.dim):
                        if (self.slots[xx][yy][0]==shipID): 
                            self.slots[xx][yy][1] = -1
        self.lastShotInfo = {"coords":{"x":x,"y":y}, "slot":self.slots[x][y], "allSinked":self.allSinked()}
        return True;
    def shoot(self,coord,radius):
        '''Launch a shoot (area effect if 3rd arg >0) centered to the given coordinate'''
        if (radius<0):
            return False
        pos = self.coordsValidateAndConvert(coord)
        if (not pos):
            return False
        if (radius==0):
            self.takeShot(pos)
        else:
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    target = [ pos[0]+x , pos[1]+y ]
                    if (coordsValidate(self.dim,target,True)):
                        self.takeShot(target)
        return True
    def sinkedShips(self):
        return list(filter(lambda x : x.sinked==True, self.ships))
    def allSinked(self):
        return len(self.sinkedShips())==len(self.ships)
