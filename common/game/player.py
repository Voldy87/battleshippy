from math import sqrt
from numpy import sign
from random import seed,choice,randint
#togliere sotto se test ok
from common.game.grid import Grid
from common.game.ship import Ship

def squaresBetween(start,end):
    '''Generate all coordinates between two cells, using the double 0-indexed notation both for input and output'''
    coordinates = []
    index = 1 if (start[0]==end[0]) else 0 # squares are placed in vertical or horizontal?
    step = sign(end[index]-start[index])
    for num in range(start[index],end[index]+1*step, step):
        temp=[None,None]
        temp[index],temp[1-index]=num,start[1-index]
        coordinates.append(temp)
    return coordinates 
def validSquares(obj,matrix):
    '''Compute the neighboring cells around a series of shots on a ship (at least 1)
     using double 0-indexed lists'''
    side = len(matrix)
    x = obj[0][0]
    y = obj[0][1]
    neighbors=[] #return a list of [x,y] lists (coords)
    if (len(obj)<2): #last shot before this one hit a ship for the first time
        neighbors = lambda x, y : [
            [x2, y2]
            for x2 in range(x-1, x+2)
            for y2 in range(y-1, y+2)
            if ( ((0<=x2<side)and(0<=y2<side)) and
                     #abs(complex(x2-x,y2-y))<sqrt(2),
                     matrix[x2][y2][1]==0 and
                     (x2!=x or y2!=y)
                   )
        ]
        return neighbors(x,y)
    else: #i'm trying to hit again a ship
        if (x==obj[1][0]): #hit ship is placed vertically (common abscissa)
            yUp = +1+max(idle[1]  for idle in obj)
            yDw = -1+min(cleese[1]  for cleese in obj)
            if (yUp<side and matrix[x][yUp][1]==0):
                neighbors.append([x,yUp])
            if (yDw>=0 and matrix[x][yDw][1]==0):
                neighbors.append([x,yDw])
        elif (y==obj[1][1]): #hit ship is placed horizontally (common ordinate)
            xRt = +1+max(obj,key=lambda palin : palin[0])[0]
            xLt = -1+min(obj,key=lambda chapman : chapman[0])[0]
            if (xRt<side and matrix[xRt][y][1]==0):
                neighbors.append([xRt,y])
            if (xLt>=0 and matrix[xLt][y][1]==0):
                neighbors.append([xLt,y]) 
        else: #never executed
            pass
        return neighbors

class Player:
    '''Constructor'''
    def __init__(spam,nature,name):
        spam.nature = nature
        spam.name = name
        spam.lastGoodShots = []
    def reactToHit(self,x,y):
        self.lastGoodShots.insert(0,[x,y])
    def reactToSink(self):
        self.lastGoodShots = []
    def reactToShot(self,shotInfo):
        x, y = shotInfo["coords"]["x"], shotInfo["coords"]["y"]
        shipId, shotNum =  shotInfo["slot"]
        if shipId==0:
            return "MISS"
        elif shotNum==1:
            self.reactToHit(x,y)
            return "FIRST_HIT"
        elif shotNum>1:
            self.reactToHit(x,y)
            return "ALREADY_HIT"
        elif shotNum==-1:
            self.reactToSink()
            return "JUST_SINKED"
        elif shotNum<-1:
            return "ALREADY_SINKED"
    def humanTarget():
        pass
    def computerTarget(self,slots,strategy):
        '''Return random target coordinates, according to strategy and last shot upcome'''
        switch = { "basic" : self.basicAIshot }
        switch[strategy](slots)
    def basicAIshot(self,slots):
        seed()
        side = len(slots)
        if (self.lastGoodShots):# current slot is a ship hit(not sunk)
            shootables = validSquares(self.lastGoodShots, slots )
            return choice(shootables)
        else:
            temp = [ [x,y] for x in range(0,side) for y in range(0,side) if slots[x][y][1]==0]
            return choice(temp) #random extract one coordinate from not yet hit ones
    def computerShip(self,shipLen,strategy,distance,slots):
        '''Insert ship in free map spaces respecting the distance, choosing an algorithm'''
        switch = {"basic":self.basicAIship}
        endpoint = switch[strategy](shipLen,distance,slots)
        return squaresBetween(endpoint[0],endpoint[1])    
    def basicAIship(self,shipLen,shipMinDistance,slots):
        '''Randomly find space for a ship, returning endpoints coordinates'''
        seed() #in program main?
        dim = len(slots)
        flag = True
        xS = xE = yS = yE = -1
        while flag:
            xS = randint(0,dim-1)
            yS = randint(0,dim-1)
            #print(str(xS)+" "+str(yS))
            #print(slots[xS][yS])
            if slots[xS][yS][0]!=0: #starting slot is free?
                continue
            mul = choice(tuple(([-1,0],[+1,0],[0,-1],[0,+1]))) #choose direction ('NSWE')
            xE = xS + mul[0]*(shipLen-1)
            yE = yS + mul[1]*(shipLen-1)
            if( xE in range(0,dim) and yE in range(0,dim) and slots[xE][yE][0]==0 ) : #in this direction the endof the ship exists free 
                flag = False
                step=1
                if mul[0]!=0:
                    step=mul[0]
                for i in range( xS+mul[0], xE+mul[0]*(shipMinDistance+1), step ):
                    if (slots[i][yE][0]!=0):
                        flag = True
                        break
                if mul[1]==0:
                    step=1
                else:
                    step=mul[1]
                for i in range( yS+mul[1], yE+mul[1]*(shipMinDistance+1), step ):
                    if (slots[xE][i][0]!=0):
                        flag = True
                        break
                if (not flag):
                    return [xS,yS],[xE,yE]
        return False
                            
if ( __name__ == "__main__"):
##    d = [ [[11,0] ,[1,0] ,[0,0] ,[0,1]] ,[[3,0] ,[4,0] ,[2,0] ,[0,-1]] ,[[0,10] ,[166,0] ,[0,2] , [111,1]] ,[[0,0] ,[1,1] ,[0,-2] ,[1,0]] ]
##    c = [ [[10,0] ,[10,0] ,[10,0] ,[10,0]] ,[[10,0] ,[10,0] ,[10,0] ,[10,0]] ,[[10,0] ,[10,0] ,[10,0] , [0,0]] ,[[10,0] ,[10,0] ,[10,0] ,[0,0]] ]
    p = Player("ai","gianni")
    g = Grid(4)
##    for i in range(0,0):
##        print("void")
##        print(p.computerTarget(c,"basic"))
##        p.reactToHit(1,1)
##        #print(p.lastGoodShots)
##        print("1 ship hit at 1,1")
##        print(p.computerTarget(c,"basic"))
##        p.reactToHit(1,2)
##        print("ship hit at 1,1 and 1,2")
##        print(p.computerTarget(c,"basic"))
##        print("\n")
    g.addShip(Ship("test",2),[["A",1],["a",2]])
    for i in range(0,35):
        print(p.computerShip(3,"basic",0,g.slots))
