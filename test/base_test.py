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
        assert g.coordsConvert(["C",2],True)==[2,1]
        assert g.coordsConvert([1,2],False)==['B',3]
        assert g.coordsConvert(["A",1])==[0,0]
        assert g.coordsConvert(["A",2],True)==[0,1]
        assert g.coordsConvert([2,2],False)==['C',3]

    def test_coordsValidate(idle):
        g = G.Grid(8)
        assert g.coordsValidate(["C",2]) == True
        assert g.coordsValidate(["C",7], False) == True
        assert g.coordsValidate(["H",2]) == True
        assert g.coordsValidate([1,8],True) == True
        assert g.coordsValidate([0,0], True) == True
        assert g.coordsValidate(["R",2]) == False
        assert g.coordsValidate(["C",22]) == False
        assert g.coordsValidate(["C",2], True) == False
        assert g.coordsValidate(["A",1], True) == False
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
    def test_gridRenderAndShoot(palin):
        assert True
    def test_renderGrid(cleese):
        assert True
        

