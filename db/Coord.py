from db.CoordData import *

class Coord():
    """This class takes a (x,y) point from the continent maps and creates a dictionary of all possible zone (x,y) coordinates.
       If the map/zone belongs to an instance a dummy is added."""
    def __init__(self, mapId, x, y, version, zoneId=False, phase_id=0, debug=False):
        self.pointList = []
        self.zoneList = {}
        self.isInstance = False
        self.isMulti = False
        self.noZone = False
        if version == 'classic':
            mapBorders = mapBordersClassic
        elif version == 'tbc':
            mapBorders = mapBordersTBC
        elif version == 'wotlk':
            mapBorders = mapBordersWotLK
        elif version == 'cata':
            mapBorders = mapBordersCata
        elif version == 'mop':
            mapBorders = mapBordersMoP
        for mapSet in mapBorders:
            zone = int(mapSet[0])
            if (not (zoneId == False)) and (zone != zoneId):
                continue
            mId = int(mapSet[2])
            x_min = float(mapSet[5])
            x_max = float(mapSet[6])
            y_min = float(mapSet[3])
            y_max = float(mapSet[4])
            is_in_map_boundary = (x_min < x < x_max) and (y_min < y < y_max)
            if mapId == mId and not is_in_map_boundary: # No clue why this is "not"
                if x_max == x_min or y_max == y_min:
                    print("WARNING: Map " + str(mapId) + " has no valid coordinates! " + str(mapSet))
                    continue
                xCoord = round(abs(((x - x_min) / (x_max - x_min)) * 100), 2)
                yCoord = round(abs(((y - y_min) / (y_max - y_min)) * 100), 2)
                if 1 < phase_id < 4294967295:
                    self.zoneList[zone] = (yCoord, xCoord, phase_id)
                    self.pointList.append((zone, yCoord, xCoord, phase_id))
                else:
                    self.zoneList[zone] = (yCoord, xCoord)
                    self.pointList.append((zone, yCoord, xCoord))

        for instance in instanceIds:
            zoneID = int(instance[0])
            mapID = int(instance[2])
            if mapId == mapID or zoneID == zoneId:
                self.isInstance = True
                self.instanceId = zoneID

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


def worldToZone(mapId, x, y, version, zone=False):
    a = Coord(mapId, x, y, zone, version)
    for point in a.pointList:
        print(point)
