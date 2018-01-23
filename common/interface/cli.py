# python -m common.interface.cli

from texttable import Texttable
from colorama import init # call init() at start

from common.game.grid import Grid, coordsConvert as convert
from common.interface.i_o import I_O
#togliere questi sotto se nn faccio il test qui

from common.game.ship import Ship

class CLI:
    def __init__(self):
        init()
        self.cliSquareMap = { 'Void':'\x1b[44m', 'Ship':'\x1b[42m', 'Shot':['\x1b[0;37m',chr(216),'\x1b[0;31m'], 'Sinked':'\x1b[45m' }
        self.io = I_O('stdCLI','stdCLI')
    def getSquareCode(self,slot,show_ships, highlightShot): #fg/pre bg/mid let/post
        what = slot[0]
        shots = slot[1]
        pre=''
        post=' '
        mid =''
        if (shots<0):
            pre = self.cliSquareMap['Sinked']
            return (pre+mid+post+'\x1b[0m')
        elif (shots>0):
            post = self.cliSquareMap['Shot'][1]
            if (highlightShot): #the slot i'm printing needs to be highlighted?
                pre = self.cliSquareMap['Shot'][2]
            else:
                pre = self.cliSquareMap['Shot'][0]
        if (what==0)or(not show_ships and shots==0):
            mid = self.cliSquareMap['Void']
        else:
            mid = self.cliSquareMap['Ship']
        return (pre+mid+post+'\x1b[0m')
    def renderGrid(self, grid, fullView, lastshotView): #var def have to go outisde gthis fun
        '''Show the grid on the console, with shoots and ships if present and desired:
            - grid to show
            - view all ships or only hit parts
            - highlight last shot or not
        '''
        dim = len(grid.slots)
        letters = list(map(chr, range(65, 91)))
        row_one = [''] + letters[0:dim]
        rows = [row_one]
        for x in range(0,dim): #each row after the header one (that has letters)
            temp = [x+1]
            for y in range(0,dim): #each column
                highlightShot = (lastshotView) and ("coords" in grid.lastShotInfo) and (grid.lastShotInfo["coords"]=={'x':x,'y':y})
                temp.append(self.getSquareCode(grid.slots[x][y],fullView, highlightShot))
            rows.append(temp)
        t = Texttable(0) #(github.com/foutaise/texttable) "__init__(self, max_width=80) max_width is an integer, specifying the maximum width of the table if set to 0, size is unlimited, therefore cells won't be wrapped"
        t.add_rows(rows) #use a generator or something similar to avoid all this arrays...
        print(t.draw())
    def coordString(self,coord,LetCol):
        vett = convert(coord,False,LetCol)
        return str(vett[0])+str(vett[1])
    def askAllShips(self,side,ships):
        return None
    def askSingleShip(self, side, ship): #ship is a ship class object
        """ Ask all the required positions for a single ship: only check that all positions are given:
        returns the array with the inserted coordinates """
        dim = ship.length
        name = ship.name
        pointCoords = []
        for spam in range(1,dim+1):
            flag = True
            while flag:
                flag = False
                self.io.write("Insert "+name+" ship position ("+str(spam)+" of "+str(dim)+")")
                while True:
                    self.io.write("VERTICAL/COLUMN(letter):")
                    x = self.io.read()
                    if (65<=ord(x.upper())<=65+side-1):
                        break
                    self.io.write("A letter in the range A-"+chr(65+side-1)+", please")
                while True:
                    self.io.write("HORIZONTAL/ROW(number):")
                    y = self.io.read()
                    try:
                       y = int(y)
                    except ValueError:
                       self.io.write ('A number, between 1 and '+ str(side) + " please")
                       continue
                    if ( 0 < y <= side):
                        break
                    else:
                        self.io.write ('A number between 1 and '+ str(side) + " please")
                pos = [x.upper(),y]
                if pos not in pointCoords: 
                    pointCoords.append(pos)
                else:
                    self.io.write ('Already used position!')
                    flag= True
        return pointCoords   
    def shotUpcome(self, shotInfo, LetCol):
        pos = shotInfo['coords']
        shipId, shots = shotInfo['slot']
        if not pos:
            return
        string = "Your shot to the "+ self.coordString([pos['x'],pos['y']],LetCol)+" position "
        if shipId==0:
            string += "has hit the sea!"
        else:
            string += "has hit a ship"
            if shots==-1:
                string += ", sinking it"
            elif shots>1:
                string += ", but you had already hit it in this position"
            elif shots<-1:
                string += "but it was already sinked"
        if (shotInfo['allSinked']):
            string += " and, in addition, this was the last ship of your enemy!"
        self.io.write(string)
if ( __name__ == "__main__"):
    dim = 4
    shiplen = 2
    c = CLI()
    gg = Grid(dim)
    c.renderGrid(gg,True,True)
    z = Ship("submarine",shiplen)
    pos = c.askSingleShip(dim,z)
    if gg.posChecker(10,pos):
        gg.addShip(z,pos)
    c.renderGrid(gg,True,True)
    zz = Ship("submarine",shiplen)
    pos2 = c.askSingleShip(dim,zz)
    if gg.posChecker(0,pos2):
        gg.addShip(zz,pos2)
    c.renderGrid(gg,True,True)
    for i in pos:
        gg.shoot(i,0)
        c.renderGrid(gg,True,True)
        c.shotUpcome(gg.lastShotInfo, gg.letCol)
    for i in pos2:
        gg.shoot(i,0)
        c.shotUpcome(gg.lastShotInfo, gg.letCol)
    c.renderGrid(gg,True,True)
