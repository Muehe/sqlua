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

objectZonesClassic = getObjectZones('data/classic/gameobject_preExtract.csv')
objectZonesTBC = getObjectZones('data/tbc/gameobject_preExtract.csv')

class Obj():
    spawnErrors = [] # Holds IDs of objects without spawns entry, name, type, faction, data1
    def __init__(self, obj, dicts, extractSpawns, version, translation=False, debug=False):
        self.version = version
        if version == 'classic':
            objectZones = objectZonesClassic
        elif version == 'tbc':
            objectZones = objectZonesTBC
        self.id = obj[0]
        self.name = escapeDoubleQuotes(obj[1])
        self.type = obj[2]
        self.faction = obj[3]
        self.data1 = obj[4]
        spawns = []
        if extractSpawns:
            for spawn in dicts['object']:
                if (spawn[0] == self.id):
                    if spawn[4] in objectZones:
                        spawns.append((spawn[1], spawn[2], spawn[3], objectZones[spawn[4]]))
                    else:
                        spawns.append((spawn[1], spawn[2], spawn[3]))
        if (spawns == []):
            Obj.spawnErrors.append(self.id)
            self.noSpawn = True
            self.spawns = CoordList([], version)
        elif extractSpawns:
            self.spawns = CoordList(spawns, version, debug=debug)
        self.start = []
        for pair in dicts['object_start']:
            if pair[0] == self.id:
                self.start.append(pair[1])
        if self.start == []:
            del self.start
        self.end = []
        for pair in dicts['object_end']:
            if pair[0] == self.id:
                self.end.append(pair[1])
        if self.end == []:
            del self.end
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
