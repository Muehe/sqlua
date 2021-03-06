from CoordList import *
from Utilities import *
import re
import csv

def getCreatureZones(file="data/creature_preExtract.csv"):
    infile = open(file, "r")
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    zoneDict = {}
    for row in reader:
        zoneDict[int(row[0])] = int(row[1])
    infile.close()
    return zoneDict

zones = getCreatureZones()

def getCreatureWaypoints(file="data/creature_movement_preExtract.csv"):
    infile = open(file, "r")
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    zoneDict = {}
    for row in reader:
        # Split id#point strings
        idAndPoint = re.split("\D", row[0])
        cid = int(idAndPoint[0])
        point = int(idAndPoint[1])
        if cid not in zoneDict:
            zoneDict[cid] = {}
        zoneDict[cid][point] = int(row[1])
    infile.close()
    return zoneDict

movementZones = getCreatureWaypoints()
movementTemplateZones = getCreatureWaypoints("data/creature_movement_template_preExtract.csv")

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
            # spawns and spawn waypoints
            for spawn in dicts['npc']:
                # id, map, position_x, position_y, guid
                if (spawn[0] == self.id):
                    # get spawns
                    if spawn[4] in zones:
                        spawns.append((spawn[1], spawn[2], spawn[3], zones[spawn[4]]))
                    else:
                        spawns.append((spawn[1], spawn[2], spawn[3]))
                    # get waypoints
                    wpSort = {}
                    for waypoint in dicts['npc_movement']:
                        # point, guid, position_x, position_y
                        if (waypoint[1] == spawn[4]):
                            if (spawn[4] in movementZones) and (waypoint[0] in movementZones[spawn[4]]):
                                wpSort[waypoint[0]] = (spawn[1], waypoint[2], waypoint[3], movementZones[spawn[4]][waypoint[0]])
                            else:
                                wpSort[waypoint[0]] = (spawn[1], waypoint[2], waypoint[3])
                    # sort waypoints if there is more than one, discard single-point pathes
                    if (len(wpSort) > 1):
                        temp = []
                        for wp in sorted(list(wpSort)):
                            temp.append(wpSort[wp])
                        waypoints.append(CoordList(temp))
                    elif (len(wpSort) == 1):
                        print(f'Discarded single-point path for GUID {spawn[4]}')

            # template waypoints
            wpError = False
            # get waypoints
            wptSort = {}
            for waypoint in dicts['npc_movement_template']:
                # point, entry, position_x, position_y
                if (waypoint[1] == self.id) and (len(spawns) > 0):
                    if (self.id in movementTemplateZones) and (waypoint[0] in movementTemplateZones[self.id]):
                        wptSort[waypoint[0]] = (spawns[0][0], waypoint[2], waypoint[3], movementTemplateZones[self.id][waypoint[0]])
                    else:
                        wptSort[waypoint[0]] = (spawns[0][0], waypoint[2], waypoint[3])
                else:
                    wpError = True
            # sort waypoints
            if (len(wptSort) > 0):
                temp = []
                for wp in sorted(list(wptSort)):
                    temp.append(wptSort[wp])
                waypoints.append(CoordList(temp))
            # persist spawns and waypoints
            if (spawns == []):
                Npc.spawnErrors.append(self.id)
            else:
                self.spawns = CoordList(spawns)
            if (waypoints != []):
                self.waypoints = waypoints
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
