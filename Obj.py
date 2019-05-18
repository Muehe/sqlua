from CoordList import *
from Utilities import *
import re

def getObjectZones(file="data/objectZones.txt"):
    infile = open(file, "r")
    content = infile.read()
    infile.close()
    zoneList = re.findall("(\d+),(\d+)", content)
    zoneDict = {}
    for pair in zoneList:
        zoneDict[int(pair[1])] = int(pair[0])
    return zoneDict

objectZones = getObjectZones()

class Obj():
    spawnErrors = [] # Holds IDs of objects without spawns entry, name, type, faction, data1
    def __init__(self, obj, dicts, extractSpawns, translation=False):
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
        elif extractSpawns:
            self.spawns = CoordList(spawns)
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
