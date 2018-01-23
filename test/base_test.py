#   RUN python -m pytest -vs  IN THE TEST DIR

from common.game import grid as G, ship as S, player as P
import common.interface.cli as C

import pytest
from operator import itemgetter
from random import seed,randint


#test that pytest works !
def func(x):
    return x + 1
def test_tester(): # :-)
    assert func(4) == 5
def f():
    raise SystemExit(1)
def test_exceptions():
    with pytest.raises(SystemExit):
        f()
# PLAYER
class TestPlayerClassAndUtils(object):
    def test_squaresBetween(idle):
        assert P.squaresBetween([0,3],[0,8])== [[0,3],[0,4],[0,5],[0,6],[0,7],[0,8]]
        assert P.squaresBetween([0,8],[0,2])== [[0,8], [0,7], [0,6],[0,5],[0,4],[0,3],[0,2]]
        assert P.squaresBetween([2,13],[2,9])== [[2,13],[2,12],[2,11],[2,10],[2,9],]
        assert P.squaresBetween([1,3],[2,3])== [[1,3],[2,3]]
        assert P.squaresBetween([40,23],[45,23])== [[40,23],[41,23],[42,23],[43,23],[44,23],[45,23]]
        assert P.squaresBetween([2,9],[9,9])== [[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9]]
        assert P.squaresBetween([22,99],[18,9])== [[22,99],[21,99],[20,99],[19,99],[18,99]]
    def test_validSquares(jones):
        g = G.Grid(6)
        pos = ["C",3]
        assert g.shoot(pos) == True
        pos = G.coordsConvert(pos) #[2,2]
        assert sorted(P.validSquares([pos],g.slots),key=itemgetter(0)) == sorted([[1,1],[1,2],[1,3], [2,1],[2,3],[3,1],[3,2],[3,3]],key=itemgetter(0))
        g = G.Grid(6)
        pos = ["A",2]
        assert g.shoot(pos) == True
        pos = G.coordsConvert(pos) #[1,0]
        assert sorted(P.validSquares([pos],g.slots),key=itemgetter(0)) == sorted([[0,0],[0,1],[1,1], [2,0],[2,1]],key=itemgetter(0))
        pos2 = ["A",1]
        assert g.shoot(pos2) == True
        pos2 = G.coordsConvert(pos2) #[0,0]
        assert sorted(P.validSquares([pos,pos2],g.slots),key=itemgetter(0)) == [[2,0]]
        pos3 = ["F",4]
        assert g.shoot(pos3) == True
        pos3 = G.coordsConvert(pos3) #[3,5]
        assert sorted(P.validSquares([pos3],g.slots),key=itemgetter(0)) == sorted([[2,4],[2,5], [3,4],[4,4],[4,5]],key=itemgetter(0))
        pos4, pos5 = ["d",3],["D",4] #[2,3], [3,3]
        assert g.shoot(pos4) == True
        assert g.shoot(pos5) == True
        pos4, pos5 = G.coordsConvert(pos4),G.coordsConvert(pos5)
        assert sorted(P.validSquares([pos4,pos5],g.slots),key=itemgetter(0)) == [[1,3],[4,3]]
        pos4, pos5 = ["e",2],["d",2] #[1,4], [1,3]
        assert g.shoot(pos4) == True
        assert g.shoot(pos5) == True
        pos4, pos5 = G.coordsConvert(pos4),G.coordsConvert(pos5)
        assert sorted(P.validSquares([pos4,pos5],g.slots),key=itemgetter(1)) == [[1,2],[1,5]]
    def test_reactToShot(cleese):
        seed()
        dim = randint(4,25)
        pp = P.Player("ai","test")
        for letter in list(map(chr, range(65, 65+dim))):
            g = G.Grid(dim)
            for i in range(1,7):
                g.shoot([letter,i])
                assert pp.reactToShot(g.lastShotInfo) == "MISS"
            for i in range(1,100):
                g.shoot(G.randomCoord(dim,False,True))
                assert pp.reactToShot(g.lastShotInfo) == "MISS"
            g.addShip( S.Ship("cargo",4), [[letter,1],[letter,2],[letter,3],[letter,4]] )
            for i in range(1,4):
                g.shoot([letter,i])
                assert pp.reactToShot(g.lastShotInfo) == "FIRST_HIT"
            for i in range(1,4):
                g.shoot([letter,i])
                assert pp.reactToShot(g.lastShotInfo) == "ALREADY_HIT"
            g.shoot([letter,4])
            assert pp.reactToShot(g.lastShotInfo) == "JUST_SINKED"
            for i in range(1,5):
                g.shoot([letter,i])
                assert pp.reactToShot(g.lastShotInfo) == "ALREADY_SINKED"
    def test_basicAIshot(gilliam):
        g = G.Grid(2)
        pp = P.Player("ai","gianni")
        assert pp.basicAIshot(g.slots) in [[0,0],[0,1],[1,0],[1,1]]
        g.shoot(["A",1])
        assert pp.basicAIshot(g.slots)!=[0,0]
        g.shoot(["b",2])
        assert pp.basicAIshot(g.slots)!=[1,1]
        assert pp.basicAIshot(g.slots)!=[0,0]
        g = G.Grid(2)
        g.shoot(["A",1])
        assert pp.reactToShot(g.lastShotInfo) == "MISS"
        g.shoot(["A",2])
        assert pp.reactToShot(g.lastShotInfo) == "MISS"
        g.shoot(["B",1])
        assert pp.reactToShot(g.lastShotInfo) == "MISS"
        assert pp.basicAIshot(g.slots)==[1,1]
        g = G.Grid(4)
        assert g.addShip( S.Ship("cargo",4), [["B",2],["B",3],["B",1],["B",4]] ) == True
        g.shoot(["B",2])
        assert pp.reactToShot(g.lastShotInfo) == "FIRST_HIT"
        g.shoot(["B",3])
        assert pp.reactToShot(g.lastShotInfo) == "FIRST_HIT"
        temp = pp.basicAIshot(g.slots)
        assert temp==[3,1] or temp==[0,1]
        g.shoot(["B",1])
        assert pp.reactToShot(g.lastShotInfo) == "FIRST_HIT"
        assert pp.basicAIshot(g.slots)==[3,1]
        g.shoot(["B",4])
        assert pp.reactToShot(g.lastShotInfo) == "JUST_SINKED"
# SHIP
class TestShipClass(object):
    def test_constructor(idle):
        assert str(S.Ship("cargo",3)) == "cargo: 3 long, hit 0 times"
        assert str(S.Ship("submarine",7)) == "submarine: 7 long, hit 0 times"
        assert str(S.Ship("test",4)) == "test: 4 long, hit 0 times"

# GRID  
class TestGridClassAndUtils(object):
    def test_coordsConvert(gilliam):
        assert G.coordsConvert(["C",2],LetCol=False)==[2,1]
        assert G.coordsConvert(["c",2],LetCol=False)==[2,1]
        assert G.coordsConvert(["C",2])==[1,2]
        assert G.coordsConvert(["C",2],True,True)==[1,2]
        assert G.coordsConvert(["C",2],True)==[1,2]
        assert G.coordsConvert(["C",2],True,False)==[2,1]
        assert G.coordsConvert([1,2],False,False)==['B',3]
        assert G.coordsConvert(["A",1])==[0,0]
        assert G.coordsConvert(["d",4])==[3,3]
        assert G.coordsConvert(["A",1],True,False)==[0,0]
        assert G.coordsConvert(["d",4],True,False)==[3,3]
        assert G.coordsConvert(["A",2],True,False)==[0,1]
        assert G.coordsConvert([2,2],False,False)==['C',3]
        assert G.coordsConvert([3,0],False,False)==['D',1]
        assert G.coordsConvert([0,3],False,True)==['A',4]
        assert G.coordsConvert([3,1],False,True)==['D',2]
    def test_coordsValidate(idle):
        dim = 8
        assert G.coordsValidate(dim,["C",2]) == True
        assert G.coordsValidate(dim,["C",7], False) == True
        assert G.coordsValidate(dim,["H",2]) == True
        assert G.coordsValidate(dim,[4,5],True) == True
        assert G.coordsValidate(dim,[0,0], True) == True
        assert G.coordsValidate(dim,[7,7], True) == True
        assert G.coordsValidate(dim,[0,0], True) == True
        assert G.coordsValidate(dim,["R",2]) == False
        assert G.coordsValidate(dim,["C",9]) == False
        assert G.coordsValidate(dim,["C",22]) == False
        assert G.coordsValidate(dim,["C",2], True) == False
        assert G.coordsValidate(dim,["A",1], True) == False
        assert G.coordsValidate(dim,[0,8],True) == False
        assert G.coordsValidate(dim,[0,28]) == False
        assert G.coordsValidate(dim,[8,2]) == False
        assert G.coordsValidate(dim,[-33,8]) == False
        assert G.coordsValidate(dim,["A",13], False) == False
#CLI
class TestCliClass(object):
    def test_gridRenderOnly(chapman):
        for i in range(1,1):
            g = G.Grid(i)
            c = C.CLI()
            c.renderGrid(g,False,False)
            c.renderGrid(g,False,True)
            c.renderGrid(g,True,False)
            c.renderGrid(g,True,True)
        assert True
    def test_gridRenderAndShip(jones):
        g = G.Grid(10)
        c = C.CLI()
        assert g.addShip( S.Ship("cargo",5), [["B",2],["B",3],["B",1],["B",4]] ) == False
        assert g.addShip( S.Ship("cargo",4), [["W",2],["B",3],["B",1],["B",4]] ) == False
        assert g.addShip( S.Ship("cargo",4), [["A",2],["B",3],["B",1],["B",4]] ) == True #addShip does not check space continguity or freedom
        assert g.slots[0][1] == [1,0]
        assert g.slots[2][1] == [1,0]
        assert g.slots[3][1] == [1,0]
        c.renderGrid(g,True,False)
        g = G.Grid(10)
        assert g.addShip( S.Ship("cargo",4), [["B",2],["B",3],["B",1],["B",4]] ) == True
        assert g.addShip( S.Ship("cargo",8), [["C",1],["C",2],["C",3],["C",5],["C",4],["C",6],["C",7],["C",8]] ) == True
        c.renderGrid(g,False,False)
        c.renderGrid(g,True,False)
    def test_gridPosCheckerForOneShip(cleese):
        g = G.Grid(4)
        assert g.posChecker(0,[["A",3]]) == True
        assert g.posChecker(0,[["B",2],["B",3],["B",1],["B",4]] ) == True
        assert g.posChecker(0,[["A",1],["B",1],["C",1]] ) == True
        assert g.posChecker(0,[["C",3],["B",3]] ) == True
        assert g.posChecker(0,[["A",2],["C",2],["B",2]]) == True
        assert g.posChecker(0,[["C",4],["B",4],["D",4]]) == True
        assert g.posChecker(0,[["A",3],["H",3]] ) == False
        assert g.posChecker(0,[["A",32],["D",3]] ) == False
        assert g.posChecker(0,[["A",3],["D",3]] ) == False
        assert g.posChecker(0,[["A",1],["B",1],["C",1],["B",4]] ) == False
        assert g.posChecker(0,[["B",2],["B",3],["B",1],["B",4],["B",5],["B",6]] ) == False
        assert g.posChecker(0,[["A",2],["C",2],["D",2]]) == False
        assert g.posChecker(0,[["A",2],["C",2],["A",2]]) == False
    def test_gridPosCheckerForManyShipsWithoutDistance(gilliam):
        g = G.Grid(7)
        p1 = [["E",5],["E",4]]
        assert g.posChecker(0,[["E",6]]) == True
        assert g.posChecker(0,p1) == True
        assert g.addShip( S.Ship("test",2), p1 ) == True
        p2 = [["B",3],["D",3],["C",3],["E",3]]
        assert g.posChecker(0,p2) == True
        assert g.addShip( S.Ship("test",4), p2 ) == True
        assert g.posChecker(0,[["B",2]]) == True
        assert g.posChecker(0,p1) == False
        assert g.posChecker(0,[["B",1],["B",3],["B",2]]) == False
        assert g.posChecker(0,[["E",5]]) == False
        assert g.posChecker(0,[["B",77]]) == False
        assert g.posChecker(0,[["F",1],["B",3],["B",2]]) == False
        
    def test_gridPosCheckerForManyShipsWithDistance(jones):
        g = G.Grid(6)
        p1 = [["C",3],["D",3]]
        for i in range(1,7):
            assert g.posChecker(i,p1) == True
        assert g.posChecker(0,p1) == True
        assert g.addShip( S.Ship("test",2), p1 ) == True
        p2 = [["B",1],["B",3],["B",2]]
        assert g.posChecker(1,[["C",1],["D",1]]) == True
        assert g.posChecker(0,p1) == False
        assert g.posChecker(3,p1) == False
        assert g.posChecker(1,p2) == False
        assert g.posChecker(9,p2) == False
        assert g.posChecker(2,[["C",1],["D",1]]) == False
        assert g.addShip( S.Ship("test",2), p2 ) == False
        assert g.addShip( S.Ship("test",4), p2 ) == False
        assert g.posChecker(0,p2) == True
        assert g.addShip( S.Ship("test",3), p2 ) == True
        assert g.posChecker(0,p2) == False
        assert g.posChecker(0,[["A",1],["A",3],["a",2]]) == True
        assert g.posChecker(0,[["A",1],["d",3],["a",2]]) == False
        assert g.posChecker(0,[["C",3],["d",1]]) == False
    def test_gridShoot(palin):
        g = G.Grid(5)
        assert g.shoot(["B",21],0) == False
        assert g.shoot(["B",1],-10) == False
        assert g.shoot(["H",1],0) == False
        assert g.shoot(["B",44],10) == False
        assert g.shoot(["z",2],1) == False
        assert g.shoot(["A",2],1) == True
        assert g.shoot(["B",1],0) == True
        assert g.shoot(["E",1],10) == True
        assert g.shoot(["D",2],0) == True
        assert g.shoot(["C",3],0) == True
        assert g.shoot(["E",3],2) == True 
    def test_gridRenderAndShoot(palin):
        g = G.Grid(10)
        c = C.CLI()
        c.renderGrid(g,False,False)#c.print(g.slots,False) 
        assert g.addShip(S.Ship("test",4), [["B",2],["B",3],["B",1],["B",4]]) == True
        c.renderGrid(g,False,True)#c.print(g.slots,False)
        assert g.shoot(["B",2],0) == True
        c.renderGrid(g,True,False)#c.print(g.slots,False)
        assert  g.shoot(["D",2],0) == True
        c.renderGrid(g,False,False)#c.print(g.slots,False)
        assert g.shoot(["B",3],0) == True
        assert g.shoot(["B",1],0) == True
        assert g.shoot(["B",1],0) == True
        c.renderGrid(g,False,True)#c.print(g.slots,False)
        assert g.shoot(["B",4],0) == True
        c.renderGrid(g,False,False)#c.print(g.slots,False)
        assert g.shoot(["C",4],0) == True
        assert g.shoot(["C",4],0) == True
        assert g.shoot(["A",4],0) == True
        c.renderGrid(g,False,False)
        assert g.shoot(["A",2],0) == True
        assert g.shoot(["C",2],0) == True
        assert g.addShip(S.Ship("test2",7), [["c",8],["f",8],["D",8],["B",8],["e",8],["g",8],["H",8]]) == True
        c.renderGrid(g,False,False)
        c.renderGrid(g,True,True)
        assert g.shoot(["p",2],0) == False
        assert g.shoot(["A",2],0) == True
        assert g.shoot(["C",8],0) == True
        assert g.shoot(["e",23],0) == False
        assert g.shoot(["A",8],0) == True
        assert g.shoot(["d",8],0) == True
        assert g.shoot(["d",10],0) == True
        c.renderGrid(g,False,True)
        c.renderGrid(g,True,False)
        for i in range(1,11):
            assert g.shoot(["A",i],0) == True
        c.renderGrid(g,False,False)
        c.renderGrid(g,True,True)
