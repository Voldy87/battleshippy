from texttable import Texttable
from colorama import init # call init() at start

class CLI:
    def __init__(self,dim):
        init()
        self.dim=dim
        self.cliSquareMap = { 'Void':'\x1b[44m', 'Ship':'\x1b[42m', 'Shot':['\x1b[0;31m',chr(216)], 'Sinked':'\x1b[45m' }
    def getSquareCode(self,slot,show_ships): #fg/pre bg/mid let/post
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
            pre = self.cliSquareMap['Shot'][0]
        if (what==0)or(not show_ships and shots==0):
            mid = self.cliSquareMap['Void']
        else:
            mid = self.cliSquareMap['Ship']
        return (pre+mid+post+'\x1b[0m')
    def print(self, slots,enemyview): #var def have to go outisde gthis fun
        dim = self.dim
        letters = list(map(chr, range(65, 91)))
        row_one = [''] + letters[0:dim]
        rows = [row_one]
        for x in range(0,dim): #each row after the header one (that has letters)
            temp = [x+1]
            for y in range(0,dim): #each column
                temp.append(self.getSquareCode(slots[x][y],not enemyview))
            rows.append(temp)
        t = Texttable()
        t.add_rows(rows) #use a generator or something similar to avoid all this arrays...
        print(t.draw())
    def askShip(self, dim):
        "Ask DIM positions for a ship: only check that DIM positions are given"
        for spam in range(0,dim):
            pass
        
