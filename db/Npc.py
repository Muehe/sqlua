from db.CoordList import *
from db.Utilities import *
from config import *
from os.path import isfile
import re
import csv

def getCreatureZones(file):
    infile = open(file, "r")
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    zoneDict = {}
    for row in reader:
        zoneDict[int(row[0])] = int(row[1])
    infile.close()
    return zoneDict

def getCreatureWaypoints(file):
    infile = open(file, "r")
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    zoneDict = {}
    for row in reader:
        # Split id#point strings
        idAndPoint = re.split(r"\D", row[0])
        cid = int(idAndPoint[0])
        point = int(idAndPoint[1])
        if cid not in zoneDict:
            zoneDict[cid] = {}
        zoneDict[cid][point] = int(row[1])
    infile.close()
    return zoneDict

def getCreatureTemplateWaypoints(file):
    infile = open(file, "r")
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    zoneDict = {}
    for row in reader:
        # Split id#point strings
        idAndPoint = re.split(r"\D", row[0])
        cid = int(idAndPoint[0])
        point = int(idAndPoint[1])
        pathId = int(idAndPoint[2])
        if cid not in zoneDict:
            zoneDict[cid] = {}
        if pathId not in zoneDict[cid]:
            zoneDict[cid][pathId] = {}
        zoneDict[cid][pathId][point] = int(row[1])
    infile.close()
    return zoneDict

def getFactionTemplate(fac):
    content = ""
    with open(fac, "r") as infile:
        content = infile.read()
    # 1,1,72,3,2,12,0,0,0.000000,0.000000,0,0,0,0,
    # id,name,?,ourMask,friendlyMask,hostileMask,etc...
    factionList = re.findall("(.*?),.*?,.*?,(.*?),(.*?),(.*?),.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,?\n", content)
    factionDict = {}
    for data in factionList:
        if data[0] == 'ID':
            continue
        factionDict[int(data[0])] = (int(data[1]), # ourMask
                                     int(data[2]), # friendlyMask
                                     int(data[3])) # hostileMask
    print(f'Found {len(factionDict)} factions in {fac}')
    return factionDict

zonesDict = {}
movementZonesDict = {}
movementTemplateZonesDict = {}
factionTemplateDict = {}

for version in versions:
    zonesDict[version] = {}
    movementZonesDict[version] = {}
    movementTemplateZonesDict[version] = {}
    factionTemplateDict[version] = getFactionTemplate(f'data/{version}/FactionTemplate.dbc.CSV')
    for flavor in flavors:
        if flavor in dbInfo and version in dbInfo[flavor]:
            if isfile(f'data/{version}/{flavor}/creature_preExtract.csvzone_and_area.csv'):
                zonesDict[version][flavor] = getCreatureZones(f'data/{version}/{flavor}/creature_preExtract.csvzone_and_area.csv')
            else:
                zonesDict[version][flavor] = {}
            if isfile(f'data/{version}/{flavor}/creature_movement_preExtract.csvzone_and_area.csv'):
                movementZonesDict[version][flavor] = getCreatureWaypoints(f'data/{version}/{flavor}/creature_movement_preExtract.csvzone_and_area.csv')
            else:
                movementZonesDict[version][flavor] = {}
            if isfile(f'data/{version}/{flavor}/creature_movement_template_preExtract.csvzone_and_area.csv'):
                movementTemplateZonesDict[version][flavor] = getCreatureTemplateWaypoints(f'data/{version}/{flavor}/creature_movement_template_preExtract.csvzone_and_area.csv')
            else:
                movementTemplateZonesDict[version][flavor] = {}

class Npc():
    spawnErrors = [] # Holds IDs of NPCs without spawns
    waypointErrors = []
    def __init__(self, npc, dicts, extractSpawns, version, flavor, translation=False, debug=False):
        self.version = version
        self.flavor = flavor
        zones = zonesDict[version][flavor]
        movementZones = movementZonesDict[version][flavor]
        movementTemplateZones = movementTemplateZonesDict[version][flavor]
        factionTemplate = factionTemplateDict[version]
        self.id = npc[0]
        self.debug = debug
        self.name = escapeQuotes(npc[1])
        self.minlevel = npc[2]
        self.maxlevel = npc[3]
        self.minlevelhealth = npc[4]
        self.maxlevelhealth = npc[5]
        self.rank = npc[6]
        self.faction = npc[7]
        if self.faction in factionTemplate:
            if (12 & factionTemplate[self.faction][0]) != 0:
                self.hostileToA = True
            else:
                self.hostileToA = False
            if (10 & factionTemplate[self.faction][0]) != 0:
                self.hostileToH = True
            else:
                self.hostileToH = False
        else:
            print("Faction not found in factionTemplate:", self.faction, "NPC ID:", self.id)
            self.hostileToA = True
            self.hostileToH = True
        self.subName = npc[8]
        self.npcFlags = npc[9] & pow(2, 32) - 1
        if extractSpawns:
            spawns = []
            waypoints = []
            # spawns and spawn waypoints
            if self.id in dicts['npc']:
                rawSpawns = dicts['npc'][self.id]
                for spawn in rawSpawns:
                    # id, map, position_x, position_y, guid, PhaseId
                    if (spawn[0] == self.id) or (spawn[0] == 0):
                        # get spawns
                        if spawn[4] in zones:
                            if version == 'cata' or version == 'mop':
                                spawns.append((spawn[1], spawn[2], spawn[3], zones[spawn[4]], spawn[5]))
                            else:
                                spawns.append((spawn[1], spawn[2], spawn[3], zones[spawn[4]], 0))
                        else:
                            if version == 'cata' or version == 'mop':
                                spawns.append((spawn[1], spawn[2], spawn[3], False, spawn[5]))
                            else:
                                spawns.append((spawn[1], spawn[2], spawn[3], False, 0))
                        # get waypoints
                        npcMovement = None
                        if spawn[4] in dicts['npc_movement']:
                            npcMovement = dicts['npc_movement'][spawn[4]] #by GUID
                        if npcMovement is not None:
                            wpSort = {}
                            for waypoint in npcMovement:
                                # point, guid, position_x, position_y
                                if (waypoint[1] == spawn[4]):
                                    if (spawn[4] in movementZones) and (waypoint[0] in movementZones[spawn[4]]):
                                        zone = movementZones[spawn[4]][waypoint[0]]
                                        if zone == 0 and spawn[4] in zones:
                                            zone = zones[spawn[4]]
                                        wpSort[waypoint[0]] = (spawn[1], waypoint[2], waypoint[3], zone)
                                    else:
                                        wpSort[waypoint[0]] = (spawn[1], waypoint[2], waypoint[3])
                            # sort waypoints if there is more than one, discard single-point pathes
                            if (len(wpSort) > 1):
                                temp = []
                                for wp in sorted(list(wpSort)):
                                    temp.append(wpSort[wp])
                                waypoints.append(CoordList(temp, version, debug=self.debug))
                            elif (len(wpSort) == 1):
                                # TODO implement checking for "non-moving" waypoints that are abused for script
                                if self.debug: print(f'DEBUG: Discarded single-point path for GUID {spawn[4]}')
            # template waypoints
            wpError = False
            # get waypoints
            wptSort = {}
            if self.id in dicts['npc_movement_template']:
                for waypoint in dicts['npc_movement_template'][self.id]:
                    # point, entry, position_x, position_y, pathId
                    if (waypoint[1] == self.id) and (len(spawns) > 0):
                        if (self.id in movementTemplateZones) and (waypoint[4] in movementTemplateZones[self.id]) and (waypoint[0] in movementTemplateZones[self.id][waypoint[4]]):
                            wptSort[waypoint[0]] = (spawns[0][0], waypoint[2], waypoint[3], movementTemplateZones[self.id][waypoint[4]][waypoint[0]])
                        else:
                            wptSort[waypoint[0]] = (spawns[0][0], waypoint[2], waypoint[3])
                    else:
                        wpError = True
            # sort waypoints
            if (len(wptSort) > 0):
                temp = []
                for wp in sorted(list(wptSort)):
                    temp.append(wptSort[wp])
                waypoints.append(CoordList(temp, version))
            # persist spawns and waypoints
            if (spawns == []):
                Npc.spawnErrors.append(self.id)
                self.noSpawn = True
                self.spawns = CoordList([], version)
            else:
                self.spawns = CoordList(spawns, version)
                # use npcZoneIdMap to remove invalid spawn entries
                """
                # With updated pre-extract data this code should be obsolete, but if its to be used it needs to be only for Cata
                correct_zone = npcZoneIdMap.get(self.id)
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
                """


            if (waypoints != []):
                self.waypoints = waypoints
            if(wpError):
                Npc.waypointErrors.append(self.id)
        
        #Start
        self.start = []
        if self.id in dicts['npc_start']:
            for pair in dicts['npc_start'][self.id]:
                if pair[0] == self.id:
                    self.start.append(pair[1])
        if self.start == []:
            del self.start

        #End
        self.end = []
        if self.id in dicts['npc_end']:
            for pair in dicts['npc_end'][self.id]:
                if pair[0] == self.id:
                    self.end.append(pair[1])
        if self.end == []:
            del self.end

        #locale
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
