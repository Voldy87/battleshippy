from texttable import Texttable
from colorama import init # call init() at start

from common.game.grid import Grid
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
                print("HL")
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
            - view all ships or only hitten parts
            - highlight last shot or not
        '''
        dim = len(grid.slots)
        letters = list(map(chr, range(65, 91)))
        row_one = [''] + letters[0:dim]
        rows = [row_one]
        for x in range(0,dim): #each row after the header one (that has letters)
            temp = [x+1]
            for y in range(0,dim): #each column
                highlightShot = (lastshotView) and ("coords" in grid.lastShotInfo) and (grid.lastShotInfo["coords"]==[x,y])
                temp.append(self.getSquareCode(grid.slots[x][y],fullView, highlightShot))
            rows.append(temp)
        t = Texttable(0) #(github.com/foutaise/texttable) "__init__(self, max_width=80) max_width is an integer, specifying the maximum width of the table if set to 0, size is unlimited, therefore cells won't be wrapped"
        t.add_rows(rows) #use a generator or something similar to avoid all this arrays...
        print(t.draw())
    def askAllShips(self,side,ships):
        return None
    def askSingleShip(self, side, ship): #ship is a ship class object
        "Ask DIM positions for a single ship: only check that DIM positions are given"
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
                    self.io.write("A letter in the range A-"+chr(65+dim-1)+", please")
                while True:
                    self.io.write("HORIZONTAL/ROW(number):")
                    y = self.io.read()
                    try:
                       y = int(y)
                    except ValueError:
                       self.io.write ('A number, between 0 and '+ str(side) + " please")
                       continue
                    if ( 0 <= y < side):
                        break
                    else:
                        self.io.write ('A number between 0 and '+ str(side-1) + " please")
                pos = [x.upper(),y]
                if pos not in pointCoords: 
                    pointCoords.append(pos)
                else:
                    self.io.write ('Already used position!')
                    flag= True
        return pointCoords   
    def shotUpcome(self, shotInfo):
        pos, shipId, shots = shotInfo.coords, shotInfo.self.slots[x][y][0], shotInfo.self.slots[x][y][1]
        if (not pos):
            return
        self.io.write("Your shot to the "+str(pos.x)+"-"+str(pos.y)+" position ")  
        if (shipId==0):
            self.io.write("has hit the sea!")
        else:
            self.io.write("has hit a ship, ")
            if (shots==-1):
                self.io.write("sinking it!!")
            elif (shots>0):
                self.io.write(" but you had already hit it in this position!")
        if (shotInfo.allSinked):
            self.io.write("In addition, this was the last ship of your enemy!")

if ( __name__ == "__main__"):
    dim = 4
    g = Grid(dim)
    c = CLI()
    c.renderGrid(g,False,False)#c.print(g.slots,False) 
    s = Ship("cargo",4)
    res = g.addShip(s, [["B",2],["B",3],["B",1],["B",4]])
    print(res)
    c.renderGrid(g,False,True)#c.print(g.slots,False)
    g.shoot(["B",2],0)
    c.renderGrid(g,True,False)#c.print(g.slots,False)
    g.shoot(["D",2],0)
    c.renderGrid(g,False,False)#c.print(g.slots,False)
    g.shoot(["B",3],0)
    g.shoot(["B",1],0)
    g.shoot(["B",1],0)
    c.renderGrid(g,False,True)#c.print(g.slots,False)
    g.shoot(["B",4],0)
    c.renderGrid(g,False,False)#c.print(g.slots,False)
    g.shoot(["C",4],0)
    g.shoot(["C",4],0)
    g.shoot(["A",4],0)
    c.renderGrid(g,False,False)
    g.shoot(["A",2],0)
    g.shoot(["C",2],0)
    c.renderGrid(g,False,False)
    c.renderGrid(g,True,True)
    #c.print(g.slots,False)
    gg = Grid(dim+2)
    lim = 1
    row1 = [["B",2],["B",1],["B",3]]
    #print(gg.posChecker(lim,row1))
    ss = Ship("submarine",3)
    tt = Ship("submarine",3)
    gg.addShip(ss,row1)
##    print(gg.posChecker(lim,[["B",1],["B",3],["B",2]]))
    row2 = [["B",5],["C",5], ["A",5]]
    gg.addShip(tt,row2)
    print(gg.posChecker(lim,row2))
    
    #gg.addShip(ss,row2)
##    print(gg.posChecker(lim,[["C",2],["D",2],["B",2]]))
##    print(gg.posChecker(lim,[["A",2],["D",2]]))
##    print(gg.posChecker(lim,[["A",2],["A",4],["A",3],["A",1]]))
##    print(gg.posChecker(lim,[[12,2],["2",2],[0,2]]))
##    print(gg.posChecker(lim,[["C",1],["B",3],["A",2]]))
    c.renderGrid(gg,True,False)#c.print(gg.slots,False)
    gg.shoot(["D",4],1)
    c.renderGrid(gg,True,True)
    zz = Ship("submarine",3)
    print(c.askSingleShip(dim+2,zz))
