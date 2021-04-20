from CoordData import *

class Coord():
    """This class takes a (x,y) point from the continent maps and creates a dictionary of all possible zone (x,y) coordinates.
       If the map/zone belongs to an instance a dummy is added."""
    def __init__(self, mapId, x, y, zoneId=False, debug=False):
        self.pointList = []
        self.zoneList = {}
        self.isInstance = False
        self.isMulti = False
        self.noZone = False
        for mapSet in mapBorders:
            zone = int(mapSet[0])
            if (not (zoneId == False)) and (zone != zoneId):
                continue
            mId = int(mapSet[2])
            x1 = float(mapSet[5])
            x2 = float(mapSet[6])
            y1 = float(mapSet[3])
            y2 = float(mapSet[4])
            if (mapId == mId) and (x < x1) and (x > x2) and (y < y1) and (y > y2):
                xCoord = round(abs((x-x1)/(x2-x1)*100), 2)
                yCoord = round(abs((y-y1)/(y2-y1)*100), 2)
                self.zoneList[zone] = (yCoord, xCoord)
                self.pointList.append((zone, yCoord, xCoord))

        for instance in instanceIds:
            zoneID = int(instance[0])
            mapID = int(instance[2])
            if (mapId == mapID):
                self.zoneList[zoneID] = (-1, -1)
                self.pointList.append((zoneID, -1, -1))
                self.isInstance = True

        if len(self.pointList) > 1:
            self.isMulti = True
        elif len(self.pointList) == 0:
            self.noZone = True
            if debug:
                print("No zone! " + str(mapId) + " " + str(zoneId))

    def __repr__(self):
        points = ""
        for c in self.zoneList:
            points += "("+str(c)+": "+str(self.zoneList[c])+")"
        return points


def worldToZone(mapId, x, y, zone=False):
    a = Coord(mapId, x, y, zone)
    for point in a.pointList:
        print(point)
