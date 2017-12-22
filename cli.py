from texttable import Texttable
from colorama import init # call init() at start

from i_o import I_O
#togliere questi sotto se nn faccio il test qui
from grid import Grid
from ship import Ship

class CLI:
    def __init__(self):
        init()
        self.cliSquareMap = { 'Void':'\x1b[44m', 'Ship':'\x1b[42m', 'Shot':['\x1b[0;37m',chr(216),'\x1b[0;31m'], 'Sinked':'\x1b[45m' }
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
        t = Texttable()
        t.add_rows(rows) #use a generator or something similar to avoid all this arrays...
        print(t.draw())
    def askShip(self, dim):
        "Ask DIM positions for a single ship: only check that DIM positions are given"
        for spam in range(0,dim):
            pass

if ( __name__ == "__main__"):
    dim = 4
    g = Grid(dim)
    c = CLI() 
    c.renderGrid(g,False,False)#c.print(g.slots,False) 
    s = Ship("cargo",4)
    res = g.addShip(s, ["B",2],["B",3],["B",1],["B",4])
    print(res)
    c.renderGrid(g,False,True)#c.print(g.slots,False)
    g.takeShot(["B",2])
    c.renderGrid(g,True,False)#c.print(g.slots,False)
    g.takeShot(["D",2])
    c.renderGrid(g,False,False)#c.print(g.slots,False)
    g.takeShot(["B",3])
    g.takeShot(["B",1])
    g.takeShot(["B",1])
    c.renderGrid(g,False,True)#c.print(g.slots,False)
    g.takeShot(["B",4])
    c.renderGrid(g,False,False)#c.print(g.slots,False)
    g.takeShot(["C",4])
    g.takeShot(["C",4])
    g.takeShot(["A",4])
    c.renderGrid(g,False,False)
    g.takeShot(["A",2])
    g.takeShot(["C",2])
    c.renderGrid(g,False,False)
    c.renderGrid(g,True,True)
    #c.print(g.slots,False)
    gg = Grid(dim)
    print(gg.posChecker(["B",4],["B",1],["B",3],["B",2]))
    print(gg.posChecker(["B",1],["B",3],["B",2]))
    print(gg.posChecker(["D",2],["D",3]))
    print(gg.posChecker(["C",2],["D",2],["B",2]))
    print(gg.posChecker(["A",2],["D",2]))
    print(gg.posChecker(["A",2],["A",4],["A",3],["A",1]))
    print(gg.posChecker([12,2],["2",2],[0,2]))
    print(gg.posChecker(["C",1],["B",3],["A",2]))
    c.renderGrid(g,False,False)#c.print(gg.slots,False)
