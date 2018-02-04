from math import inf
from random import seed,choice,randint
from enum import Enum,auto
#rename in funzioni di sole AI, visto che il player human nn c'è? oppure è ok perchè alcune cose il giocatore umano può chiederle automatiche (come lo ship positioning??)
from common.utils.grid import validSquares, allCoords, squaresDistance, squaresBetween
from common.utils.enums import ShootType as S
#togliere sotto se test ok
from common.game.grid import Grid
from common.game.ship import Ship
from common.interface.cli import CLI

def shipsMinDistance(foo,bar):
    minim = inf
    for i in foo:
        for j in bar:
            dist = squaresDistance(i[0],i[1],j[0],j[1])
            if dist<minim :
                minim = dist
    return minim-1

class PlayerType(Enum):
    PC = auto()
    HUMAN = auto()

class Player:
    '''This class'''
    def __init__(spam,nature:PlayerType,name:str ):
        '''Constructor'''
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
        if shipId == 0:
            if shotNum==1:
                return S.FIRST_MISS
            elif shotNum>1:
                return S.ALREADY_MISS
        elif shipId != 0:
            if shotNum==1:
                self.reactToHit(x,y)
                return S.FIRST_HIT
            elif shotNum>1:
                return S.ALREADY_HIT
            elif shotNum==-1:
                self.reactToSink()
                return S.JUST_SINKED
            elif shotNum<-1:
                return S.ALREADY_SINKED
    def humanTarget():
        pass
    def computerTarget(self,slots,strategy="basic"):
        '''Return random target coordinates (double 0-indexed), according to strategy and last shot upcome'''
        switch = {
            "basic" : self.basicAIshot #ENUM for Basic??
        }
        return switch[strategy](slots)
    def basicAIshot(self,slots):
        '''Return random target coordinates (double 0-indexed): if the last shot has hit a ship
        tries one of the squares around the latter, otherwise shoots completely randomly'''
        seed()
        side = len(slots)
        if (self.lastGoodShots):# current slot is a ship hit(not sunk)
            shootables = validSquares( self.lastGoodShots, slots )
            return choice(shootables)
        else:
            temp = [ [x,y] for [x,y] in allCoords(side) if slots[x][y][1]==0]
            return choice(temp) #random extract one coordinate from not yet hit ones
    def computerShip(self,shipLen,strategy,distance,slots,ships=[]):
        '''Insert ship in free map spaces respecting the distance, choosing an algorithm'''
        switch = {
            "basic":self.basicAIship #ENUM for Basic??
        }
        endpoint = switch[strategy](shipLen,distance,slots,ships)
        return squaresBetween(endpoint[0],endpoint[1])    
    def basicAIship(self,shipLen,minDistance,slots,ships=[]):
        '''Randomly find space for a ship (2 minimum length), returning endpoints coordinates;
            assumes that on the grid there is enough space for the ship (considering minimum distance,too), if its length is right.'''
        seed() #in program main?
        dim = len(slots)
        if shipLen not in range(2,dim+1) or minDistance >= dim:
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
            candidate = squaresBetween([xS,yS],[xE,yE])
            for [x,y] in candidate: #every slot of the ship (endpoints included)
                if slots[x][y][0]!=0: #already busy cell
                    flag = True
                    break
            if minDistance > 0 :
                for ship in ships:
                    positioned = squaresBetween(ship["ends"][0],ship["ends"][1])
                    if shipsMinDistance(candidate,positioned) < minDistance :
                        flag = True
                        break
        return [[xS,yS],[xE,yE]]
                            
if ( __name__ == "__main__"):
##    d = [ [[11,0] ,[1,0] ,[0,0] ,[0,1]] ,[[3,0] ,[4,0] ,[2,0] ,[0,-1]] ,[[0,10] ,[166,0] ,[0,2] , [111,1]] ,[[0,0] ,[1,1] ,[0,-2] ,[1,0]] ]
##    c = [ [[10,0] ,[10,0] ,[10,0] ,[10,0]] ,[[10,0] ,[10,0] ,[10,0] ,[10,0]] ,[[10,0] ,[10,0] ,[10,0] , [0,0]] ,[[10,0] ,[10,0] ,[10,0] ,[0,0]] ]
    p = Player("ai","gianni")
    g = Grid(4)
    print(g.addShip(Ship("test",4),[["A",1],["a",2],["A",3],["a",4]]))
    c = CLI()
    c.renderGrid(g,True,True);
    print(p.basicAIship(4,2,g.slots,g.ships))
    g.shoot(["A",1])
