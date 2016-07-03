from sqlua.Coord import *

class CoordList():
    """Holds a list of Coord() objects."""
    def __init__(self, coordTable):
        self.cList = []
        self.cByZone = {}
        for coord in coordTable:
            if len(coord) > 3:
                self.addCoord(coord[0], coord[1], coord[2], coord[3])
            else:
                self.addCoord(coord[0], coord[1], coord[2])

    def addCoord(self, map, x, y, zone=False):
        newCoord = Coord(map, x, y, zone)
        if newCoord.pointList != {}:
            self.cList.append(newCoord)
            for c in newCoord.pointList:
                if c in self.cByZone:
                    self.cByZone[c].append(newCoord.pointList[c])
                else:
                    self.cByZone[c] = [newCoord.pointList[c]]

    def findCoord(self, **kwargs):
        return next(self.__iterCoord(**kwargs))

    def allCoords(self, **kwargs):
        return list(self.__iterCoord(**kwargs))

    def allCoordsWith(self, *args):
        return list(self.__iterCoordWith(*args))

    def __iterCoordWith(self, *args):
        return (coord for coord in self.cList if hasattr(coord, *args))

    def __iterCoord(self, **kwargs):
        return (coord for coord in self.cList if coord.match(**kwargs))
