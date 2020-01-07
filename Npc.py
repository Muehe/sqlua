from CoordList import *
from Utilities import *
import re

def getCreatureZones(file="data/creatureZones.txt"):
    infile = open(file, "r")
    content = infile.read()
    infile.close()
    zoneList = re.findall("(\d+),(\d+)", content)
    zoneDict = {}
    for pair in zoneList:
        zoneDict[int(pair[1])] = int(pair[0])
    return zoneDict

zones = getCreatureZones()

def getFactionTemplate(file="data/FactionTemplate.dbc.CSV"):
    content = ""
    with open(file, "r") as infile:
        content = infile.read()
    # 1,1,72,3,2,12,0,0,0.000000,0.000000,0,0,0,0,
    # id,name,?,ourMask,friendlyMask,hostileMask,etc...
    factionList = re.findall("(.*?),.*?,.*?,(.*?),(.*?),(.*?),.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,", content)
    factionDict = {}
    for data in factionList:
        factionDict[int(data[0])] = (int(data[1]), # ourMask
                                     int(data[2]), # friendlyMask
                                     int(data[3])) # hostileMask
    return factionDict

factionTemplate = getFactionTemplate()

class Npc():
    spawnErrors = [] # Holds IDs of NPCs without spawns
    waypointErrors = []
    def __init__(self, npc, dicts, extractSpawns, translation=False):
        self.id = npc[0]
        self.name = escapeQuotes(npc[1])
        self.minlevel = npc[2]
        self.maxlevel = npc[3]
        self.minlevelhealth = npc[4]
        self.maxlevelhealth = npc[5]
        self.rank = npc[6]
        self.faction = npc[7]
        if (12 & factionTemplate[self.faction][0]) != 0:
            self.hostileToA = True
        else:
            self.hostileToA = False
        if (10 & factionTemplate[self.faction][0]) != 0:
            self.hostileToH = True
        else:
            self.hostileToH = False
        self.subName = npc[8]
        self.npcFlags = npc[9]
        if extractSpawns:
            spawns = []
            waypoints = []
            for spawn in dicts['npc']:
                if (spawn[0] == self.id):
                    if spawn[4] in zones:
                        spawns.append((spawn[1], spawn[2], spawn[3], zones[spawn[4]]))
                    else:
                        spawns.append((spawn[1], spawn[2], spawn[3]))
                    for waypoint in dicts['npc_movement']:
                        if (waypoint[1] == spawn[4]):
                            waypoints.append((spawn[1], waypoint[2], waypoint[3]))
            wpError = False
            for waypoint in dicts['npc_movement_template']:
                if (waypoint[1] == self.id):
                    if (spawns == []):
                        if (not wpError):
                            wpError = True
                    else:
                        waypoints.append((spawns[0][0], waypoint[2], waypoint[3]))
            if (spawns == []):
                Npc.spawnErrors.append(self.id)
            else:
                self.spawns = CoordList(spawns)
            if (waypoints != []):
                self.waypoints = CoordList(waypoints)
            if(wpError):
                Npc.waypointErrors.append(self.id)
        self.start = []
        for pair in dicts['npc_start']:
            if pair[0] == self.id:
                self.start.append(pair[1])
        if self.start == []:
            del self.start
        self.end = []
        for pair in dicts['npc_end']:
            if pair[0] == self.id:
                self.end.append(pair[1])
        if self.end == []:
            del self.end
        if self.id in dicts['locales_npc']:
            self.locales = dicts['locales_npc'][self.id]
        else:
            if translation:
                print('Missing translation for NPC:', self.name, '('+str(self.id)+')' )

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        for (key, val) in kwargs.items():
            if not (hasattr(self, key)):
                return False
        return all(getattr(self,key) == val for (key, val) in kwargs.items())
