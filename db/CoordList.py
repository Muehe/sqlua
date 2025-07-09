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
            elif len(coord) > 3:
                self.addCoord(coord[0], coord[1], coord[2], version, coord[3], 0)
            else:
                self.addCoord(coord[0], coord[1], coord[2], version, False, 0)

    def addCoord(self, map, x, y, version, zone, phase_id):
        newCoord = Coord(map, x, y, version, zone, phase_id, debug=self.debug)
        if not newCoord.noZone:
            self.cList.append(newCoord)
            for zone in newCoord.zoneList:
                if zone in self.cByZone:
                    self.cByZone[zone].append(newCoord.zoneList[zone])
                else:
                    self.cByZone[zone] = [newCoord.zoneList[zone]]
            if newCoord.isInstance:
                if newCoord.instanceId in self.cByZone:
                    if (-1, -1) not in self.cByZone[newCoord.instanceId]:
                        self.cByZone[newCoord.instanceId].append((-1, -1))
                else:
                    self.cByZone[newCoord.instanceId] = [(-1, -1)]

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

    def __repr__(self):
        points = "{"
        for z in self.cByZone:
            points += f'{z}:['
            for c in self.cByZone[z]:
                points += str(c) + ','
            points += '],'
        points += "},"
        return points
