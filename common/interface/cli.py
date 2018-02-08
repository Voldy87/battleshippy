# python -m common.interface.cli

import os,time #all?

from texttable import Texttable
from colorama import init # call init() at start

from common.game.grid import Grid, coordsConvert as convert
from common.interface.i_o import I_O
from common.utils.enums import ShootType as s, InterfaceType
#togliere questi sotto se nn faccio il test qui
# prelevare i messaggi da un file (also good for i18n)
from common.game.ship import Ship

def consoleCode(obj):
    return obj["fg"]+obj["bg"]+obj["chr"]+obj["rst"];
class CLI:
    def __init__(self):
        init()
        self.cliSquareMap = { #must be built from config
            'Void':'\x1b[44m',
            'Ship':'\x1b[42m',
            'Shot':['\x1b[0;37m',chr(216),'\x1b[0;31m'], #duplica in shot e last shot (vedi config)
            'Sinked':'\x1b[45m'
        }
##        self.gridColors:{
##            "Reset":,
##            "Void": {"bg":},
##            "Ship": {"bg":},
##            "Sinked": {"bg":},
##            "Shot": {"fg":, "chr":},
##            "LastShot": {"fg":, "chr":}
##        }
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
        pre='' #out = {"bg":'', "fg":'',"chr":' ', "rst":'\x1b[0m'}
        post=' '
        mid =''
        if (shots<0):
            pre = self.cliSquareMap['Sinked'] #out["bg"]=gridColors["Sinked"]["bg"]
            return (pre+mid+post+'\x1b[0m') #return consoleCode(out)
        elif (shots>0):
            post = self.cliSquareMap['Shot'][1] #out["chr"]=gridColors["Shot"]["chr"]
            if (highlightShot): #the slot i'm printing needs to be highlighted?
                pre = self.cliSquareMap['Shot'][2] #out["fg"]=gridColors["LastShot"]["fg"]
            else:
                pre = self.cliSquareMap['Shot'][0] #out["fg"]=gridColors["Shot"]["fg"]
        if (what==0)or(not show_ships and shots==0):
            mid = self.cliSquareMap['Void'] #out["bg"]=gridColors["Void"]["bg"]
        else:
            mid = self.cliSquareMap['Ship'] #out["bg"]=gridColors["Ship"]["bg"]
        return (pre+mid+post+'\x1b[0m') #return consoleCode(out)
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
    def enterSplash(self):
        self.io.write("####################")
        self.io.write("##  BATTLESHIPPY  ##")
        self.io.write("####################")
    def startSplash(self,name,starting):
        self.io.write("Welcome to the Battleship Game, "+name+"!")
        self.io.write(["You", "Your opponent"][int(not starting)]+" will start")
    def insertedSplash(self,grid):
        self.io.write("Your grid status:")
        self.renderGrid(grid,True,False)
    def gridSplash(self,name):
        self.io.write(name+", these are the ships as you have placed them:")
    def battleSplash(self,name):
        self.io.write("----------------------------------")
        self.io.write("Real battle starts, "+name+"!!")
        self.io.write("----------------------------------")
    def turnSplash(self,name,turn):
        self.io.write("Turn "+str(turn)+", "+name)
    def shootSplash(self,name):
        self.io.write("Dear "+name+", it's your turn to shoot")
        self.io.write("This is the situation of your oppenent's grid")
    def changeSplash(self,me,you,mytime=5,yourtime=5):
        self.io.write("Dear "+me+", your turn is finished")
        if yourtime!=0:
            self.countdown(mytime,"Please pass the console to the other player ("+you+") after ")
            self.clear()
            self.countdown(yourtime,you+", your turn will start in ")      
    def resultSplash(self,name,myVictory,itsVictory,myRetire):
        (result,who,whom) = ("won","you","your enemy") if (myVictory or (not itsVictory and not myRetire)) else ("lost","your opponent","you")
        how = whom+" retired" if (myRetire or (not myRetire and not myVictory and not itsVictory)) else who+" sank all the ships belonging to "+whom
        self.io.write("----------------------------------")
        string = "Dear "+name+", "+how+", so "+who+" won."
        self.io.write(string)
    def finalSplash(self):
        self.io.write("These are the grids as match finished:")
    def endgridsSplash(self,name):
        self.io.write(name+"'s one")
    def finishSplash(self):
        self.io.write("----------------------------------")
        self.io.write("Game over")
        self.io.write("----------------------------------")
    def exitSplash(self):
        self.io.write("####################")
        self.io.write("##    GOODBYE!    ##")
        self.io.write("####################")
    def askUI(self): #TODO:checking input
        self.io.write("Do you want to activate the Graphical Mode?(Y/N)")
        res = self.io.read().upper()
        #check 
        return InterfaceType.GUI if res=="Y" else InterfaceType.CLI
    def askConfig(self,configMap):
       # for spam in configMap:
          #  if dataMode uiMode outputPC clear shipAI shootAI
        pass
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
                    x = self.io.read().upper()
                    if (len(x)>0 and 65<=ord(x)<=65+side-1):
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
                if (len(x)>0 and 65<=ord(x)<=65+side-1):
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
    def askRetire(self):
        self.io.write ('Do you want to retire?(Y, otherwise continue)')
        res = self.io.read().upper()
        return len(res)>0 and res[0]=="Y"
    def shotUpcome(self, name, pos, shotResult, victory, MyShot, LetCol):
        if not shotResult:
            raise Exception('No shots on this grid')
        who = ["your", "your opponent's"]
        if not MyShot:
            who.reverse()
        string = "So, "+name+", "+who[0]+" shot to the "+ self.coordString([pos['x'],pos['y']],LetCol)+" position "
        if shotResult==s.ALREADY_MISS or shotResult==s.ALREADY_SINKED or shotResult==s.ALREADY_HIT:
            string+="(already used, however) "
        if shotResult==s.FIRST_MISS or shotResult==s.ALREADY_MISS:
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
    def askExit(self):
        self.io.write("Do you want to play a new game?")
        self.io.write("Y to accept, otherwise exit)")
        res = self.io.read().upper()
        return not(len(res)>0 and res[0]=="Y")
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
