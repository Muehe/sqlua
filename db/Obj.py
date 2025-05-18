from db.CoordList import *
from db.Utilities import *
import csv

def getObjectZones(file):
    infile = open(file, "r")
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    zoneDict = {}
    for row in reader:
        zoneDict[int(row[0])] = int(row[1])
    infile.close()
    return zoneDict

def get_zones_from_spawn(spawn: tuple[any, str, int, float, float], version: str) -> dict[int, int]:
    zoneDict = {}
    guid = spawn[4]
    mapId = spawn[1]
    pos_x = spawn[2]
    pos_y = spawn[3]

    coord = Coord(mapId, pos_x, pos_y, version)

    if coord.pointList:
        # Use the first found zoneID
        zoneID = coord.pointList[0][0]
        zoneDict[guid] = zoneID
    else:
        zoneDict[guid] = None
    return zoneDict

objectZonesClassic = getObjectZones('data/classic/gameobject_preExtract.csvzone_and_area.csv')
objectZonesTBC = getObjectZones('data/tbc/gameobject_preExtract.csvzone_and_area.csv')
objectZonesWotLK = getObjectZones('data/wotlk/gameobject_preExtract.csvzone_and_area.csv')
objectZonesCata = getObjectZones('data/cata/gameobject_preExtract.csvzone_and_area.csv')

class Obj():
    spawnErrors = [] # Holds IDs of objects without spawns entry, name, type, faction, data1
    def __init__(self, obj, dicts, extractSpawns, version, translation=False, debug=False):
        self.version = version
        if version == 'classic':
            objectZones = objectZonesClassic
        elif version == 'tbc':
            objectZones = objectZonesTBC
        elif version == 'wotlk':
            objectZones = objectZonesWotLK
        elif version == 'cata':
            objectZones = objectZonesCata
        self.id = obj[0]
        self.name = escapeDoubleQuotes(obj[1])
        self.type = obj[2]
        self.faction = obj[3]
        self.data1 = obj[4]
        spawns = []
        if extractSpawns:
            if self.id in dicts['object']:
                rawSpawn = dicts['object'][self.id]
                for spawn in rawSpawn:
                    # id, map, position_x, position_y, guid, PhaseId
                    if (spawn[0] == self.id) or (spawn[0] == 0):
                        if version == 'mop':
                            objectZones = get_zones_from_spawn(spawn, version)

                        if spawn[4] in objectZones:
                            if version == 'cata':
                                spawns.append((spawn[1], spawn[2], spawn[3], objectZones[spawn[4]], spawn[5]))
                            else:
                                spawns.append((spawn[1], spawn[2], spawn[3], objectZones[spawn[4]], 0))
                        else:
                            if version == 'cata':
                                spawns.append((spawn[1], spawn[2], spawn[3], False, spawn[5]))
                            else:
                                spawns.append((spawn[1], spawn[2], spawn[3], False, 0))
        if (spawns == []):
            Obj.spawnErrors.append(self.id)
            self.noSpawn = True
            self.spawns = CoordList([], version)
        elif extractSpawns:
            self.spawns = CoordList(spawns, version, debug=debug)
            correct_zone = objectZoneIdMap.get(self.id)
            if correct_zone and correct_zone in self.spawns.cByZone:
                cleaned_cList = []
                for coord in self.spawns.cList:
                    for point in coord.pointList:
                        if point[0] == correct_zone:
                            cleaned_cList.append(coord)
                            break
                self.spawns.cList = cleaned_cList
                self.spawns.cByZone = {correct_zone: self.spawns.cByZone[correct_zone]}
            elif len(self.spawns.cByZone) > 1:
                first_zone = sorted(list(self.spawns.cByZone.keys()))[0]
                cleaned_cList = []
                for coord in self.spawns.cList:
                    for point in coord.pointList:
                        if point[0] == first_zone:
                            cleaned_cList.append(coord)
                            break
                self.spawns.cList = cleaned_cList
                self.spawns.cByZone = {first_zone: self.spawns.cByZone[first_zone]}
        
        #Start
        self.start = []
        if self.id in dicts['object_start']:
            for pair in dicts['object_start'][self.id]:
                if pair[0] == self.id:
                    self.start.append(pair[1])
        if self.start == []:
            del self.start

        #End
        self.end = []
        if self.id in dicts['object_end']:
            for pair in dicts['object_end'][self.id]:
                if pair[0] == self.id:
                    self.end.append(pair[1])
        if self.end == []:
            del self.end
        
        #locales
        if self.id in dicts['locales_object']:
            self.locales = dicts['locales_object'][self.id]
        else:
            if translation:
                print('Missing translation for Object:', self.name, '('+str(self.id)+')' )

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        for (key, val) in kwargs.items():
            if not (hasattr(self, key)):
                return False
        return all(getattr(self,key) == val for (key, val) in kwargs.items())
