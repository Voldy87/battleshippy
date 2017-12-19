from math import sqrt
from random import seed,choice

def validSquares(obj,matrix):
    side = int(sqrt(len(matrix)))
    x = obj[0][0]
    y = obj[0][1]
    neighbors=[] #return a list of [x,y] lists (coords)
    if (len(obj)<2): #last shot before this one hit a ship for the first time
        neighbors = lambda x, y : [ [x2, y2] for x2 in range(x-1, x+2)
                                   for y2 in range(y-1, y+2)
                                   if ( ((0 <= x2 < side) and (0 <= y2 < side)) and abs(complex(x2-x,y2-y))<sqrt(2) and matrix[x*side+y][1]==0 and (x2!=x or y2!=y) ) ]
        return neighbors(x,y)
    else: #i'm trying to hit again a ship
        if (x==obj[1][1]): #hit ship is placed horizontally
            yUp = max(idle[1]  for idle in obj)+1
            yDw = min(cleese[1]  for cleese in obj)-1
            if (yUp<side and matrix[x*side+yUp][1]==0):
                neighbors.append([x,yUp])
            if (yDw>=0 and matrix[x*side+yDw][1]==0):
                neighbors.append([x,yDw])
        elif (y==obj[1][1]): #hit ship is placed vertically
            xRt = max(obj,key=lambda palin : palin[0])+1
            xLt = min(obj,key=lambda chapman : chapman[0])-1
            if (xRt<side and matrix[xRt*side+y][1]==0):
                neighbors.append([xRt,y])
            if (xLt>=0 and matrix[xLt*side+y][1]==0):
                neighbors.append([xLt,y]) 
        else: #never executed
            pass
        return neighbors

class Player:
    def __init__(spam,nature,name):
        spam.nature = nature
        spam.name = name
        spam.lastGoodShots = []
    def reactToHit(self,x,y):
        self.lastGoodShots.insert(0,[x,y])
    def reactToSink(self):
        self.lastGoodShots = []
    def computerTarget(self,slots):
        seed()
        side = int(sqrt(len(slots)))
        if (self.lastGoodShots):# current slot is a ship hit(not sunk)
            shootables = (validSquares(self.lastGoodShots, slots ))
            return choice(shootables) 
        else:
            temp = [ [x,y] for x in range(0,side) for y in range(0,side) if slots[x*side+y][1]==0]
            return choice(temp)
    

d = [ [11,0] ,[1,0] ,[0,0] ,[0,1] ,[3,0] ,[4,0] ,[2,0] ,[0,-1] ,[0,10] ,[166,0] ,[0,2] , [111,1] ,[0,0] ,[1,1] ,[0,-2] ,[1,0] ]
c = [ [0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] , [0,0] ,[0,0] ,[0,0] ,[0,0] ,[0,0] ]
for i in range(0,10):
    p = Player("ai","gianni")
    print("void")
    print(p.computerTarget(c))
    p.reactToHit(1,1)
    #print(p.lastGoodShots)
    print("1 ship hit at 1,1")
    print(p.computerTarget(c))
    p.reactToHit(1,2)
    print("ship hit at 1,1 and 1,2")
    print(p.computerTarget(c))
    print("\n")




