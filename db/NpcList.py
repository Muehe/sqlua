from db.Npc import *
from db.Utilities import *

import os.path
import pickle

class NpcList():
    """Holds a list of Npc() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, version, flavor, cursor, dictCursor, recache=False, extractSpawns=True, debug=False):
        self.version = version
        self.flavor = flavor
        self.debug = debug
        self.nList = {}

        if flavor == 'cmangos':
            from db.flavor.readCmangosNpcList import getNpcTables
        elif flavor == 'mangos':
            from db.flavor.readMangosNpcList import getNpcTables
        elif flavor == 'trinity':
            from db.flavor.readTrinityNpcList import getNpcTables
        elif flavor == 'skyfire':
            from db.flavor.readSkyfireNpcList import getNpcTables

        if (not os.path.isfile(f'data/{version}/{flavor}/npcs.pkl') or recache):
            print('Caching NPCs...')
            self.cacheNpcs(getNpcTables(cursor, dictCursor), extractSpawns)
        else:
            try:
                with open(f'data/{version}/{flavor}/npcs.pkl', 'rb') as f:
                    self.nList = pickle.load(f)
                print('Using cached NPCs.')
            except:
                print('ERROR: Something went wrong while loading cached NPCs. Re-caching.')
                self.cacheNpcs(getNpcTables(cursor, dictCursor), extractSpawns)

    def cacheNpcs(self, dicts, extractSpawns=True):
        count = len(dicts['npc_template'])
        print(f'Caching {count} NPCs...')
        for npc in dicts['npc_template']:
            self.addNpc(npc, dicts, extractSpawns)
            if (count % 1000) == 0:
                print(str(count)+"...")
            count -= 1
        with open(f'data/{self.version}/{self.flavor}/npcs.pkl', 'wb') as f:
            pickle.dump(self.nList, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Done caching NPCs.")

    def addNpc(self, npc, tables, extractSpawns):
        newNpc = Npc(npc, tables, extractSpawns, self.version, self.flavor, debug=self.debug)
        self.nList[newNpc.id] = newNpc

    def findNpc(self, **kwargs):
        return next(self.__iterNpc(**kwargs))

    def allNpcs(self, **kwargs):
        return list(self.__iterNpc(**kwargs))

    def allNpcsWith(self, *args):
        return list(self.__iterNpcWith(*args))

    def __iterNpcWith(self, *args):
        return (self.nList[npc] for npc in self.nList if hasattr(self.nList[npc], *args))

    def __iterNpc(self, **kwargs):
        return (self.nList[npc] for npc in self.nList if self.nList[npc].match(**kwargs))

    def printNpcFile(self, file='output/spawnDB.lua', locale='enGB'):
        print("  Printing NPC file '%s'" % file)
        log = open(f'output/{self.version}/{self.flavor}/print.log', 'w')
        outfile = open(file, "w", encoding='utf-8')
        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

---@type QuestieDB
local QuestieDB = QuestieLoader:ImportModule("QuestieDB");

QuestieDB.npcKeys = {
    ['name'] = 1, -- string
    ['minLevelHealth'] = 2, -- int
    ['maxLevelHealth'] = 3, -- int
    ['minLevel'] = 4, -- int
    ['maxLevel'] = 5, -- int
    ['rank'] = 6, -- int, see https://github.com/cmangos/issues/wiki/creature_template#rank
    ['spawns'] = 7, -- table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    ['waypoints'] = 8, -- table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    ['zoneID'] = 9, -- guess as to where this NPC is most common
    ['questStarts'] = 10, -- table {questID(int),...}
    ['questEnds'] = 11, -- table {questID(int),...}
    ['factionID'] = 12, -- int, see https://github.com/cmangos/issues/wiki/FactionTemplate.dbc
    ['friendlyToFaction'] = 13, -- string, Contains "A" and/or "H" depending on NPC being friendly towards those factions. nil if hostile to both.
    ['subName'] = 14, -- string, The title or function of the NPC, e.g. "Weapon Vendor"
    ['npcFlags'] = 15, -- int, Bitmask containing various flags about the NPCs function (Vendor, Trainer, Flight Master, etc.).
                       -- For flag values see https://github.com/cmangos/mangos-classic/blob/172c005b0a69e342e908f4589b24a6f18246c95e/src/game/Entities/Unit.h#L536
}

QuestieDB.npcData = [[return {
""")
        outString = ""
        excludeTags =  ['[UNUSED]', '[Unused]', '[NOT USED]', '[VO]'] # These tags seem to be needed for some quests: ['[DND]', '[ph]', '[PH]', '[PH[', '[DNT]', '(DND)']
        skippedWaypoints = []
        for npcId in sorted(self.nList):
            npc = self.nList[npcId]
            if not npc.name:
                # 211770 has no name
                continue
            foundTag = False
            for tag in excludeTags:
                if tag in npc.name:
                    foundTag = tag
                    break
            if foundTag != False:
                #print("Excluding %d : %s because of tag '%s'" % (npcId, npc.name, foundTag))
                continue

            #if (not hasattr(npc, "spawns")) and (not hasattr(npc, "waypoints")):
            #    continue
            zoneId = 0
            lenSpawns = 0
            name = npc.name
            if locale != 'enGB' and hasattr(npc, 'locales') and npc.locales['name_loc'+str(localesMap[locale])] != None:
                name = escapeQuotes(npc.locales['name_loc'+str(localesMap[locale])])
            outString += ("["+str(npc.id)+"] = {'"+name+"'," #1
                                                  +str(npc.minlevelhealth)+"," #2
                                                  +str(npc.maxlevelhealth)+"," #3
                                                  +str(npc.minlevel)+"," #4
                                                  +str(npc.maxlevel)+"," #5
                                                  +str(npc.rank)+",") #6
            if hasattr(npc, "spawns") and len(npc.spawns.cList) > 0: #7
                outString += ("{")
                for zone in npc.spawns.cByZone:
                    if not zone in validZoneList:
                        if zoneId == 0:
                            zoneId = zone
                        outString += ("["+str(zone)+"]={{-1,-1}},")
                        continue
                    if len(npc.spawns.cByZone[zone]) > lenSpawns:
                        lenSpawns = len(npc.spawns.cByZone[zone])
                        zoneId = zone
                    outString += ("["+str(zone)+"]={")
                    for coords in npc.spawns.cByZone[zone]:
                        if len(coords) == 3:
                            outString += ("{"+str(coords[0])+","+str(coords[1])+","+str(coords[2])+"},")
                        else:
                            outString += ("{"+str(coords[0])+","+str(coords[1])+"},")
                    outString += ("},")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(npc, "waypoints"): #8
                waypointsByZone = {}
                for route in npc.waypoints:
                    if len(route.cList) == 0:
                        # skip empty lists, these seem to be mostly instance and script spawns, but some other edge cases might be hidded here
                        # print(f'Empty waypoint list for NPC {npc.name} ({npc.id}).')
                        continue
                    if route.cList[0].isInstance:
                        # skip waypoints in instances
                        continue
                    lastZone = route.cList[0].pointList[0][0]
                    path = []
                    for coord in route.cList:
                        if coord.isMulti:
                            print(f'Found waypoint with ambigous zone for NPC {npc.name} ({npc.id}). Skipping path.', file=log)
                            path = []
                            break
                        zone = coord.pointList[0][0]
                        if (zone != lastZone):
                            if (len(path) > 0):
                                if lastZone not in waypointsByZone:
                                    waypointsByZone[lastZone] = []
                                waypointsByZone[lastZone].append(path)
                                path = []
                            lastZone = zone
                        path.append(coord.zoneList[zone])
                    if (len(path) > 0):
                        if lastZone not in waypointsByZone:
                            waypointsByZone[lastZone] = []
                        waypointsByZone[lastZone].append(path)
                if len(npc.spawns.cList) > 3: # Waypoints for NPCs with less than 4 spawns only, otherwise we get EVERYTHIIIIINNNGGGG
                    outString += ("nil,")
                    skippedWaypoints.append(npc.id)
                elif (len(waypointsByZone) > 0):
                    outString += ("{")
                    for zone in waypointsByZone:
                        outString += ('['+str(zone)+']={')
                        for path in waypointsByZone[zone]:
                            outString += ('{')
                            for wp in path:
                                outString += ('{')
                                outString += (f'{wp[0]},{wp[1]}')
                                outString += ('},')
                            outString += ('},')
                        outString += ("},")
                    outString += ("},")
                else:
                    outString += ("nil,")
            else:
                outString += ("nil,")
            outString += (str(zoneId)+",") #9 - zoneID
            if hasattr(npc, "start"): #10 - questStarts
                outString += ("{")
                for quest in npc.start:
                    outString += (str(quest)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(npc, "end"): #11 - questEnds
                outString += ("{")
                for quest in npc.end:
                    outString += (str(quest)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(npc, "faction"): #12 - factionID
                outString += (str(npc.faction)+",")
            else:
                outString += ("nil,")
                print(f"Error: No faction found for NPC {npc.name} ({npc.id})")
            friendlyTo = ""
            if not npc.hostileToA:
                friendlyTo += "A"
            if not npc.hostileToH:
                friendlyTo += "H"
            if friendlyTo == "": #13 - friendlyToFaction
                outString += ("nil,")
            else:
                outString += (f'"{friendlyTo}",')
            if hasattr(npc, "subName") and npc.subName is not None and npc.subName != "": #14 - subName
                sn = npc.subName.replace('"', '\\"')
                outString += (f'"{sn}",')
            else:
                outString += ("nil,")
            if hasattr(npc, "npcFlags"): #15 - npcFlags
                outString += (f'{str(npc.npcFlags)},')
            else:
                outString += ("nil,")
            outString += ("},\n")
        outString += ("}]]\n")

        outfile.write(removeTrailingData(outString))
        outfile.close()
        #print(f"Skipped waypoint IDs ({len(skippedWaypoints)}):", skippedWaypoints)
