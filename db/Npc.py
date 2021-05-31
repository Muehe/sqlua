from db.CoordList import *
from db.Utilities import *
import re
import csv


import math

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

zonesClassic = getCreatureZones('data/classic/creature_preExtract.csv')
zonesTBC = getCreatureZones('data/tbc/creature_preExtract.csv')

def getCreatureWaypoints(file):
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

movementZonesClassic = getCreatureWaypoints('data/classic/creature_movement_preExtract.csv')
movementTemplateZonesClassic = getCreatureWaypoints('data/classic/creature_movement_template_preExtract.csv')

movementZonesTBC = getCreatureWaypoints('data/tbc/creature_movement_preExtract.csv')
movementTemplateZonesTBC = getCreatureWaypoints('data/tbc/creature_movement_template_preExtract.csv')

def getFactionTemplate(fac):
    content = ""
    with open(fac, "r") as infile:
        content = infile.read()
    # 1,1,72,3,2,12,0,0,0.000000,0.000000,0,0,0,0,
    # id,name,?,ourMask,friendlyMask,hostileMask,etc...
    factionList = re.findall("(.*?),.*?,.*?,(.*?),(.*?),(.*?),.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,?\n", content)
    factionDict = {}
    for data in factionList:
        factionDict[int(data[0])] = (int(data[1]), # ourMask
                                     int(data[2]), # friendlyMask
                                     int(data[3])) # hostileMask
    print(f'Found {len(factionDict)} factions in {fac}')
    return factionDict

factionTemplateClassic = getFactionTemplate('data/classic/FactionTemplate.dbc.CSV')
factionTemplateTBC = getFactionTemplate('data/tbc/FactionTemplate.dbc.CSV')

def euclidDist(x1,y1, x2,y2):
    xd = abs(x1 - x2)
    yd = abs(y1 - y2)
    return math.sqrt(xd * xd + yd * yd)

class Npc():
    spawnErrors = [] # Holds IDs of NPCs without spawns
    waypointErrors = []
    def __init__(self, npc, dicts, extractSpawns, version, translation=False, debug=False):
        self.version = version
        if version == 'classic':
            zones = zonesClassic
            movementZones = movementZonesClassic
            movementTemplateZones = movementTemplateZonesClassic
            factionTemplate = factionTemplateClassic
        elif version == 'tbc':
            zones = zonesTBC
            movementZones = movementZonesTBC
            movementTemplateZones = movementTemplateZonesTBC
            factionTemplate = factionTemplateTBC
        self.id = npc[0]
        self.debug = debug
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
        self.MovementType = npc[12]

        if extractSpawns:
            spawns = []
            waypoints = []
            # spawns and spawn waypoints
            if self.id in dicts['npc']:
                rawSpawns = dicts['npc'][self.id]

                for spawn in rawSpawns:
                    # id, map, position_x, position_y, guid
                    if (spawn[0] == self.id):
                        # get spawns
                        if spawn[4] in zones:
                            spawns.append((spawn[1], spawn[2], spawn[3], zones[spawn[4]]))
                        else:
                            spawns.append((spawn[1], spawn[2], spawn[3]))
                        # get waypoints
                        
                        npcMovement = None
                        #byId = False
                        #if self.id in dicts['npc_movement']:
                        #    npcMovement = dicts['npc_movement'][self.id] #by NPCID
                        #    byId = True
                        if spawn[4] in dicts['npc_movement']:
                            npcMovement = dicts['npc_movement'][spawn[4]] #by GUID
                            #byId = False
                        if npcMovement is not None and spawn[5] == 2 and len(dicts['npc'][self.id]) <= 6:
                            wpSort = {}
                            for waypoint in npcMovement:
                                # point, guid, position_x, position_y
                                if (waypoint[1] == spawn[4]):
                                    if (spawn[4] in movementZones) and (waypoint[0] in movementZones[spawn[4]]):
                                        wpSort[waypoint[0]] = (spawn[1], waypoint[2], waypoint[3], movementZones[spawn[4]][waypoint[0]])
                                    else:
                                        wpSort[waypoint[0]] = (spawn[1], waypoint[2], waypoint[3])
                            # sort waypoints if there is more than one, discard single-point pathes
                            totalDistance = 0
                            if (len(wpSort) > 1):
                                temp = []
                                lastPoint = None
                                sortedListCleaned = sorted(list(wpSort))
                                for wp in sortedListCleaned:
                                    #euclid distance
                                    if(lastPoint == None):
                                        lastPoint = wpSort[wp]
                                    xd = abs(wpSort[wp][1] - lastPoint[1])
                                    yd = abs(wpSort[wp][2] - lastPoint[2])
                                    totalDistance += math.sqrt(xd * xd + yd * yd)
                                    temp.append(wpSort[wp])

                                #print(str(self.id) + " : " + str(totalDistance))
                                if self.hostileToA == True and self.hostileToH == True and totalDistance >= 1000:
                                    waypoints.append(CoordList(temp, version, debug=self.debug))
                                elif totalDistance >= 350 and (self.hostileToA == False or self.hostileToH == False):
                                    waypoints.append(CoordList(temp, version, debug=self.debug))
                                #elif totalDistance >= 2500 and byId:
                                #    waypoints.append(CoordList(temp, version, debug=self.debug))
                            elif (len(wpSort) == 1):
                                # TODO implement checking for "non-moving" waypoints that are abused for script
                                if self.debug: print(f'DEBUG: Discarded single-point path for GUID {spawn[4]}')

            # template waypoints
            wpError = False
            # get waypoints
            wptSort = {}
            if self.id in dicts['npc_movement_template']:
                for waypoint in dicts['npc_movement_template'][self.id]:
                    # point, entry, position_x, position_y
                    if (waypoint[1] == self.id) and (len(spawns) > 0):
                        if (self.id in movementTemplateZones) and (waypoint[0] in movementTemplateZones[self.id]):
                            wptSort[waypoint[0]] = (spawns[0][0], waypoint[2], waypoint[3], movementTemplateZones[self.id][waypoint[0]])
                        else:
                            wptSort[waypoint[0]] = (spawns[0][0], waypoint[2], waypoint[3])
                    else:
                        wpError = True
            # sort waypoints
            if (len(wptSort) > 1): #and self.MovementType == 2
                temp = []
                lastPoint = None
                totalDistance = 0
                for wp in sorted(list(wptSort)):
                    #euclid distance
                    if(lastPoint == None):
                        lastPoint = wptSort[wp]
                    xd = abs(wptSort[wp][1] - lastPoint[1])
                    yd = abs(wptSort[wp][2] - lastPoint[2])
                    totalDistance += math.sqrt(xd * xd + yd * yd)
                    temp.append(wptSort[wp])
                if self.hostileToA == True and self.hostileToH == True and totalDistance >= 1000:
                    waypoints.append(CoordList(temp, version))
                elif totalDistance >= 350 and (self.hostileToA == False or self.hostileToH == False):
                    waypoints.append(CoordList(temp, version))
                #print(str(self.id) + " : " + str(totalDistance))
            # persist spawns and waypoints
            if (spawns == []):
                Npc.spawnErrors.append(self.id)
                self.noSpawn = True
                self.spawns = CoordList([], version)
            else:
                self.spawns = CoordList(spawns, version)
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
