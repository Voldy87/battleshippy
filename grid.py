from operator import itemgetter

from ship import Ship

class SeaMap :
    def __init__ (self, dim): #in future a rectangular grid??
        self.dim = dim
        self.slots = [ [[0,0] for x in range(dim)] for y in range(dim) ] # [0,n] empty slot hit n times before (also 0); [id,n] slot with ship id hit n times before (if n==-1 sinked ship)
        print("Created grid with " + str(dim**2) + " squares")
class Grid(SeaMap) :
    def __init__ (self,dim):
        SeaMap.__init__(self,dim)
        self.void = True
        self.lastShotInfo = dict()
        self.ships = []
    def coordsValidate(self,vett,OnlyNum=False):
        dim = self.dim
        if (OnlyNum):
            x,y = vett
            return ( x in range(0,dim+1) and y in range(0,dim+1) )
        else:
            letter, number = vett
            if ( type(letter)!=str or type(number)!=int ):
                return False
            letterAscii = ord(letter.upper())
            if ( (letterAscii not in range(65,65+dim)) or (number not in range(1,dim+1)) ):
                return False
            return [letter,number]
    def coordsConvert(self,vett,ToNum=True):
        if (ToNum):
            return [ ord(vett[0].upper())-65 , vett[1]-1 ] #e.g. ["B",3] => [4,1]
        else:
            return [ chr(vett[0]+65).upper() , vett[1]+1 ] 
        "The grid of a player, with his/her ships"
    def clear():
        pass
    def coordsValidateAndConvert(self,vett):
        coord = self.coordsValidate(vett)
        if (coord):
            return self.coordsConvert(coord)
        else:
            return False
    def posChecker (self, distance, AlphaNumPositions):
        '''Check is a set of positions for a ship is acceptable: first coordinates validity,
then square availability'''
        num = len(AlphaNumPositions)
        if (num==0):
            return True
        NumericPositions = []
        for spam in AlphaNumPositions: #single point is valid and free?
            coords = self.coordsValidateAndConvert(spam)
            if (not coords):
                print("INVALID")
                return False
            if (distance==0):
                if (self.slots[coords[0]][coords[1]][0]!=0):
                    print("BUSY")
                    return False
            else:
                x,y = coords
                lim = self.dim
                for i in range(-distance,distance+1):
                    for j in range(-distance,distance+1):
                        #print(str(self.slots[x+i][y+j][0]))
                        if (x+i<lim) and (y+j<lim) and (self.slots[x+i][y+j][0]!=0):
                            #print(str(x+i))
                            #print(str(y+j))
                            #print(str(self.slots[x+i][y+j][0]))
                            #print("\n")
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
    def addShip (self,vessel,pos): # variable length argument list for functions
        '''Given a single ship and its coordinates put it on the grid, without checking if the space is free'''
        coords = [self.coordsValidateAndConvert(spam) for spam in pos]
        if False in coords: #never fails as the coords validity is checked before invoking this function
            return False
        self.ships.append(vessel)
        shipIndex = len(self.ships)-1
        for [x,y] in coords:
            print(str(x))
            print(str(y))
            self.slots[x][y] = [shipIndex+1,0]
        self.void = False
    def shipsPositioning(self,vett):
        for spam in vett:
            self.addShip(spam) #spam = ship,pos
    def takeShot(self,coord):
        print("Taken shot at "+str(coord[0])+"-"+str(coord[1]))
        x = coord[0]
        y = coord[1]
        shipID = self.slots[x][y][0]
        shotsNum = self.slots[x][y][1]
        self.slots[x][y][1] += 1
        if (shipID == 0): # no ship in slot
            pass
        else:   # a ship is placed in this slot   
            if (shotsNum<0): #there was a ship here, but it was already sinked when it got this shot
                self.slots[x][y][1] -= 1
            elif (shotsNum==0 and self.ships[shipID-1].getShot()): # just sinked the ship!
                for x in range(0,self.dim):
                    for y in range(0,self.dim):
                        if (self.slots[x][y][0]==shipID): 
                            self.slots[x][y][1] = -1
        self.lastShotInfo = {"coords":[x,y], "slot":self.slots[x][y], "allSinked":self.allSinked()}
        return True;
    def shoot(self,coord,radius):
        if (radius<0):
            return False
        pos = self.coordsValidateAndConvert(coord);
        if (not pos):
            return False
        if (radius==0):
            self.takeShot(pos)
        else:
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    target = [ pos[0]+x , pos[1]+y ]
                    if (not self.coordsValidate(target,True)):
                        continue
                    else: 
                        self.takeShot(target)
        return True
    def sinkedShips(self):
        return list(filter(lambda x : x.sinked==True, self.ships))
    def allSinked(self):
        return len(self.sinkedShips())==len(self.ships)
