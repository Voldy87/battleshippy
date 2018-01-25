from numpy import sign
from random import seed,randint

def coordsValidate(dim:int,vett:list,OnlyNum:bool=False)->bool:
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
def coordsConvert(vett:list,ToNum:bool=True, LetCol:bool=True)->list: #to extend using class argument to locate alpahbet used for letter (now default A-Z)
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
def randomCoord(dim:int, Num:bool, LetCol:bool)->list:
    '''Return a random coordinate,mainly for testing purpose'''
    seed()
    x = randint(0,dim-1)
    y = randint(0,dim-1)
    if Num :
        return [x,y]
    else:
        return coordsConvert([x,y],False,LetCol)
def allCoords(dim):
    ret = []
    for x in range(0,dim): #for ever cell with a ship check if this slot is within minimum distance
        for y in range(0,dim):
            ret.append([x,y])
    return ret
def squaresDistance(x1,y1,x2,y2):
    return abs(complex(x2-x1,y2-y1))
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
    
    if (len(obj)<2): #last shot before this one hit a ship for the first time
        neighbors = lambda x, y : [
            [x2, y2]
            for x2 in range(x-1, x+2)
            for y2 in range(y-1, y+2)
            if ( ((0<=x2<side)and(0<=y2<side)) and
                     matrix[x2][y2][1]==0 and
                     (x2!=x or y2!=y)
                   )
        ]
        return neighbors(x,y)
    else: #i'm trying to hit again a ship
        neighbors=[]
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