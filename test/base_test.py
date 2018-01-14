#   RUN python -m pytest -vs  IN THE TEST DIR

from common.game import grid as G, ship as S
import common.interface.cli as C

import pytest

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
        
# SHIP
class TestShipClass(object):
    def test_constructor(idle):
        assert True
# GRID  
class TestGridClass(object):
    def test_coordsConvert(gilliam):
        g = G.Grid(4)
        assert g.coordsConvert(["C",2])==[2,1]
        assert g.coordsConvert(["c",2])==[2,1]
        assert g.coordsConvert(["C",2],True)==[2,1]
        assert g.coordsConvert([1,2],False)==['B',3]
        assert g.coordsConvert(["A",1])==[0,0]
        assert g.coordsConvert(["d",4])==[3,3]
        assert g.coordsConvert(["A",2],True)==[0,1]
        assert g.coordsConvert([2,2],False)==['C',3]
        assert g.coordsConvert([3,0],False)==['D',1]
    def test_coordsValidate(idle):
        g = G.Grid(8)
        assert g.coordsValidate(["C",2]) == True
        assert g.coordsValidate(["C",7], False) == True
        assert g.coordsValidate(["H",2]) == True
        assert g.coordsValidate([4,5],True) == True
        assert g.coordsValidate([0,0], True) == True
        assert g.coordsValidate([7,7], True) == True
        assert g.coordsValidate([0,0], True) == True
        assert g.coordsValidate(["R",2]) == False
        assert g.coordsValidate(["C",9]) == False
        assert g.coordsValidate(["C",22]) == False
        assert g.coordsValidate(["C",2], True) == False
        assert g.coordsValidate(["A",1], True) == False
        assert g.coordsValidate([0,8],True) == False
        assert g.coordsValidate([0,28]) == False
        assert g.coordsValidate([8,2]) == False
        assert g.coordsValidate([-33,8]) == False
        assert g.coordsValidate(["A",13], False) == False
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
        assert True
        

