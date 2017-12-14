from math import sqrt

def validSquares(x,y,side):
    neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if ((0 <= x2 < side) and (0 <= y2 < side)) and (abs(complex(x2-x,y2-y)))<sqrt(2) ]
    return neighbors(x,y)

def emptySlots(matrix):
    dim = int(sqrt(len(matrix)))
    ret = { (x,y) for x in range(0,dim) for y in range(0,dim) if (matrix[x*dim+y][1]==0)}
    return ret

class Player:
    def __init__(self,nature,name):
        self.nature = nature
        self.name = name
        self.lastGoodShot = {}
    def computerShot(self,slots):
        side = int(sqrt(len(slots)))
        if (self.lastGoodShot)# current slot is a ship hit(not sunk)
            shootables = emptySlots(slots).intersection(validSquares(lastGoodShot.x, lastGoodShot.y, side))
        pass

c = [ [11,0] ,[1,0] ,[0,0] ,[0,1] ,[3,0] ,[4,0] ,[2,0] ,[0,-1] ,[0,10] ,[166,0] ,[0,2] , [111,1] ,[0,0] ,[1,1] ,[0,-2] ,[1,0] ]

print(emptySlots(c))
