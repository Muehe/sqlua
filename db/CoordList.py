from db.Coord import *

class CoordList():
    """Holds a list of Coord() objects."""
    def __init__(self, coordTable, version, debug=False):
        self.cList = []
        self.cByZone = {}
        self.debug = debug
        for coord in coordTable:
            if len(coord) > 4:
                self.addCoord(coord[0], coord[1], coord[2], version, coord[3], coord[4])
            else:
                self.addCoord(coord[0], coord[1], coord[2], version, False, 0)

    def addCoord(self, map, x, y, version, zone, phase_id):
        newCoord = Coord(map, x, y, version, zone, phase_id, debug=self.debug)
        if not newCoord.noZone:
            self.cList.append(newCoord)
            for zone in newCoord.zoneList:
                # TODO: Add this for coords in instances and at the entry
                # if newCoord.isInstance:
                #     if zone in self.cByZone:
                #         self.cByZone[zone].append((-1, -1))
                #     else:
                #         self.cByZone[zone] = [(-1, -1)]

                if zone in self.cByZone:
                    self.cByZone[zone].append(newCoord.zoneList[zone])
                else:
                    self.cByZone[zone] = [newCoord.zoneList[zone]]

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
