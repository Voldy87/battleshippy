# python -m common.interface.cli

import os,time #all?

from texttable import Texttable
from colorama import init # call init() at start

from common.game.grid import Grid, coordsConvert as convert
from common.interface.i_o import I_O
from common.utils.enums import ShootType as s
#togliere questi sotto se nn faccio il test qui
# prelevare i messaggi da un file (also good for i18n)
from common.game.ship import Ship

class CLI:
    def __init__(self):
        init()
        self.cliSquareMap = { 'Void':'\x1b[44m', 'Ship':'\x1b[42m', 'Shot':['\x1b[0;37m',chr(216),'\x1b[0;31m'], 'Sinked':'\x1b[45m' }
        self.io = I_O('stdCLI','stdCLI')
    def clear(self):
        self.io.clear()
    def countdown(self,t,msg,shortest=True):
        self.io.write(str(msg)+str(t)+":",None)
        while t:
            mins,secs = divmod(t,60)
            if shortest and mins==0:
                frmt = '{:02d}'
                if secs<=9:
                    frmt = '{:2d}'
                timeformat = frmt.format(secs)
            else:
                timeformat = '{:02d}:{:02d}'.format(mins,secs)
            self.io.write(timeformat,end='\r')
            time.sleep(1)
            t -= 1
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
        self.io.write(t.draw())
    def coordString(self,coord,LetCol):
        vett = convert(coord,False,LetCol)
        return str(vett[0])+str(vett[1])
    def startSplash(self,name):
        self.io.write("Welcome to the Battleship Game, "+name+"!")
##    def askAllShips(self,side,ships):
##        return None
    def gridSplash(self,name):
        self.io.write(name+", these are the ships as you have placed them:")
    def battleSplash(self,name):
        self.io.write("----------------------------------")
        self.io.write("Real battle starts, "+name+"!!")
    def shootSplash(self,name):
        self.io.write("Dear "+me+", it's your turn tho shoot")
        self.io.write("This is the situation of your oppenent's grid")
    def changeSplash(self,me,you,mytime=5,yourtime=5):
        self.io.write("Dear "+me+", your turn is finished")
        self.countdown(mytime,"Please pass the console to the other player ("+you+") after ")
        self.clear()
        self.countdown(yourtime,you+", your turn will start in ")      
    def finishSplash(self,name):
        self.io.write("----------------------------------")
        self.io.write("Game over")
    def askSingleShip(self, side:int, ship:Ship):
        """ Ask all the required positions for a single ship: only check that all positions are given:
        returns the array with the inserted coordinates, in alphanumeric format (e.g. ["C",5]) """
        dim = ship.length
        name = ship.name
        pointCoords = []
        given = ""
        for spam in range(1,dim+1):
            flag = True
            while flag:
                flag = False
                self.io.write("Insert "+name+" ship position ("+str(spam)+" of "+str(dim)+" - "+given+")")
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
                    self.io.clear()
                    given += str(pos) + ";"
                    pointCoords.append(pos)
                else:
                    self.io.write ('Already used position!')
                    flag= True
        return pointCoords   
    def askTarget(self,side): #generalizzare validation coords
        self.io.write ('Give me the coordinates where to shoot')
        flag = True
        pos=[]
        while flag:
            flag = False
            while True:
                self.io.write("VERTICAL/COLUMN(letter):")
                x = self.io.read().upper()
                if (65<=ord(x)<=65+side-1):
                    break
                self.io.write("A letter in the range A-"+chr(65+side-1)+", please") #improve
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
            pos = [x ,y]
        return pos
            
    def shotUpcome(self, name, pos, shotResult, victory, MyShot, LetCol):
        if not shotInfo:
            raise Exception('No shots on this grid')
        shipId, shots = shotInfo['slot']
        who = ["your", "your opponent's"]
        if not MyShot:
            who.reverse()
        string = "So, "+name+", "+who[0]+" shot to the "+ self.coordString([pos['x'],pos['y']],LetCol)+" position "
        if shotResult==s.ALREADY_MISS or shotResult==s.ALREADY_SINKED or shotResult==s.ALREADY_HIT:
            string+="(already used, however) "
        if shotResult==FIRST_MISS or shotResult==s.ALREADY_MISS:
            string += "has hit the sea!"
        else:
            string += "has hit a ship"
            if shotResult==s.JUST_SINKED:
                string += ", sinking it"
            elif shotResult==s.ALREADY_HIT:
                string += ", but in a place already shot"
            elif shotResult==s.ALREADY_SINKED:
                string += "but the whole ship was already sinked"
        if victory:
            string += " and, in addition, this was "+who[1]+" last ship!"
        self.io.write(string)
if ( __name__ == "__main__"):
    dim = 4
    shiplen = 2
    c = CLI()
    c.countdown(228,"next player's turn in ")
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
