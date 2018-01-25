from math import sqrt
from random import seed,choice,randint

from common.utils.grid import validSquares, allCoords, squaresDistance, squaresBetween
#togliere sotto se test ok
from common.game.grid import Grid
from common.game.ship import Ship



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
    def computerTarget(self,slots,strategy="basic"):
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
            temp = [ [x,y] for [x,y] in allCoords(side) if slots[x][y][1]==0]
            return choice(temp) #random extract one coordinate from not yet hit ones
    def computerShip(self,shipLen,strategy,distance,slots):
        '''Insert ship in free map spaces respecting the distance, choosing an algorithm'''
        switch = {"basic":self.basicAIship}
        endpoint = switch[strategy](shipLen,distance,slots)
        return squaresBetween(endpoint[0],endpoint[1])    
    def basicAIship(self,shipLen,shipMinDistance,slots):
        '''Randomly find space for a ship (2 minimum length), returning endpoints coordinates;
            assumes that on the grid there is enough space for the ship (considering minimum distance,too), if its length is right.'''
        seed() #in program main?
        dim = len(slots)
        if shipLen not in range(2,dim+1) or shipMinDistance >= dim:
            return False
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
            if not( xE in range(0,dim) and yE in range(0,dim) and slots[xE][yE][0]==0 ) : #in this direction the endof the ship exists free     
                continue #second endpoit invalid
            flag = False
            for [x,y] in squaresBetween([xS,yS],[xE,yE]): #every slot of the ship (endpoints included)
                if slots[x][y][0]!=0: #already busy cell
                    flag = True
                    break
                if shipMinDistance >0:
                    for [xx,yy] in allCoords(dim): #for ever cell with a ship check if this slot is within minimum distance
                        if slots[xx][yy][0]>0 and 1+squaresDistance(x,y,xx,yy)< shipMinDistance :
                            flag = True
                            break
                if flag:
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
