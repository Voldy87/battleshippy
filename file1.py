#!/usr/bin/python

##import Tkinter #use pip to install python modules
##root = Tkinter.Tk()
##root.mainloop()

from time import clock
import sys, getopt
from astropy.io import ascii
from astropy.table import Table

rows = [(1,2,3),(4,5,6),(7,8,9)]
t = Table(rows)
ascii.write(t)

if (False):
    sys.exit()

def handleCliArg(argv):
    try: opts, args = getopt.getopt(argv,"cgi:o:", ["ifile=","ofile="])
    except getopt.GetOptError:
        print ('erroreeeeeeeeeeeeeeeeeeeeee')
    for opt, arg in opts:
        pass
handleCliArg(sys.argv[1:])

print("Welcome to the BattleShip!") #welcome message
gamedesc = '''A game by 
Andrea Orlandi''' # with triple quotes you can span a string on multiple lines
gameDesc = 'You can dowload this game at this address:' # string are immutable objects
print(gamedesc) #semicolon are notrequired
print(gameDesc) #case sensitive
vers = 0.1#float
pointsRecord = 485893986 # int
contactList = ["ing.orlandi.andrea@gmail,com", "github....", ]
for item in contactList: #whitespace is significant
    print (item)
aList = [] #list are mutable ordred objects
aList.append("xxxx"); aList.remove("xxxx") #semicolons allows multiple statements per line
aList.extend(['xxx', 15121515, True])
len(aList)

def pointToComplex (x,y,limit):
    if x>limit or y>limit: #boolean or operator
        return 0
    else: return complex(x,y) #complex numbers
def abbrGrade (fullName):
    return fullName[1:3] #string slice
def abbrShip (shipName) :
    return shipName[0] #string indexing
def complexToCoord(complexCoord):
    return xCoord, yCoord
defaultPlayerData1 = {"name":"John", 'surname':'Doe', "grade":"Captain", "wins":22} # dict initialize to non-empty value
defaultPlayerData2 = dict([("name","John"), ('surname',"Doe"), ("grade",'Captain'), ('wins',3)])
latin_Alphabet = frozenset(["a","b","c","d","e", "f","g" #statements in bracket don't need the line continuation character
                            "h","i","j","k"]) #frozen sets are immutable and unordrered
greek_Alphabet = () #tuple are immutable and ordered

gridDim = 10;

for i in range(0,squaresNum,1):
    pass

class Player: #class names start in uppercase
    "The model for a single Player" #docstring, followed by class suite
    count = 0 # class variable data member
    def __init__(self, name, surname): # constructor
        self.name = name # instance variable
        self.surname = surname
    def __del__():
        pass
    def getFullName(self): #class method data member
        return self.name + " " + self.surname
    
defaultPlayer1 = Player(defaultPlayerData1['name'], defaultPlayerData1["surname"])
print(defaultPlayer1.getFullName())                    
