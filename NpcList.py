from Npc import *
from Utilities import *

import os.path
import pickle

class NpcList():
    """Holds a list of Npc() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, cursor, dictCursor, version, extractSpawns=True, recache=False, debug=False):
        self.version = version
        self.debug = debug
        if (not os.path.isfile(f'data/{version}/npcs.pkl') or recache):
            print('Caching NPCs...')
            self.cacheNpcs(cursor, dictCursor, extractSpawns)
        else:
            try:
                with open(f'data/{version}/npcs.pkl', 'rb') as f:
                    self.nList = pickle.load(f)
                print('Using cached NPCs.')
            except:
                print('ERROR: Something went wrong while loading cached NPCs. Re-caching.')
                self.cacheNpcs(cursor, dictCursor, extractSpawns)


    def cacheNpcs(self, cursor, dictCursor, extractSpawns=True):
        self.nList = {}
        dicts = self.getNpcTables(cursor, dictCursor)
        count = len(dicts['npc_template'])
        print(f'Caching {count} NPCs...')
        for npc in dicts['npc_template']:
            self.addNpc(npc, dicts, extractSpawns)
            if ((count % 100) == 0):
                print(str(count)+"...")
            count -= 1
        with open(f'data/{self.version}/npcs.pkl', 'wb') as f:
            pickle.dump(self.nList, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Done caching NPCs.")

    def addNpc(self, npc, tables, extractSpawns):
        newNpc = Npc(npc, tables, extractSpawns, self.version, debug=self.debug)
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

    def getNpcTables(self, cursor, dictCursor):
        print("Selecting NPC related MySQL tables...")
        cursor.execute("SELECT `entry`, `name`, `minlevel`, `maxlevel`, `minlevelhealth`, `maxlevelhealth`, `rank`, `Faction`, `SubName`, `NpcFlags` FROM `creature_template`")
        npc_tpl = []
        for a in cursor.fetchall():
            npc_tpl.append(a)
        cursor.execute("SELECT id, map, position_x, position_y, guid FROM creature")
        npc = []
        for a in cursor.fetchall():
            npc.append(a)
        cursor.execute("SELECT * FROM creature_questrelation")
        npc_start = []
        for a in cursor.fetchall():
            npc_start.append(a)
        cursor.execute("SELECT * FROM creature_involvedrelation")
        npc_end = []
        for a in cursor.fetchall():
            npc_end.append(a)
        cursor.execute("SELECT point, id, position_x, position_y FROM creature_movement")
        npc_mov = []
        for a in cursor.fetchall():
            npc_mov.append(a)
        cursor.execute("SELECT point, entry, position_x, position_y FROM creature_movement_template")
        npc_mov_tpl = []
        for a in cursor.fetchall():
            npc_mov_tpl.append(a)
        count = dictCursor.execute("SELECT * FROM locales_creature")
        loc_npc = {}
        for _ in range(0, count):
            q = dictCursor.fetchone()
            loc_npc[q['entry']] = q
        print("Done.")
        return {'npc_template':npc_tpl,
                'npc':npc,
                'npc_start':npc_start,
                'npc_end':npc_end,
                'npc_movement':npc_mov,
                'npc_movement_template':npc_mov_tpl,
                'locales_npc':loc_npc}

    def printNpcFile(self, file='output/spawnDB.lua', locale='enGB'):
        outfile = open(file, "w")
        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

-------------------------
--Import modules.
-------------------------
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

""")
        outfile.write("QuestieDB.npcData = {\n")
        for npcId in sorted(self.nList):
            npc = self.nList[npcId]
            #if (not hasattr(npc, "spawns")) and (not hasattr(npc, "waypoints")):
            #    continue
            zoneId = 0
            lenSpawns = 0
            name = npc.name
            if locale != 'enGB' and hasattr(npc, 'locales') and npc.locales['name_loc'+str(localesMap[locale])] != None:
                name = escapeQuotes(npc.locales['name_loc'+str(localesMap[locale])])
            outfile.write("["+str(npc.id)+"] = {'"+name+"'," #1
                                                  +str(npc.minlevelhealth)+"," #2
                                                  +str(npc.maxlevelhealth)+"," #3
                                                  +str(npc.minlevel)+"," #4
                                                  +str(npc.maxlevel)+"," #5
                                                  +str(npc.rank)+",") #6
            if hasattr(npc, "spawns"): #7
                outfile.write("{")
                for zone in npc.spawns.cByZone:
                    if not zone in validZoneList:
                        if zoneId == 0:
                            zoneId = zone
                        outfile.write("["+str(zone)+"]={{-1, -1}},")
                        continue
                    if len(npc.spawns.cByZone[zone]) > lenSpawns:
                        lenSpawns = len(npc.spawns.cByZone[zone])
                        zoneId = zone
                    outfile.write("["+str(zone)+"]={")
                    for coords in npc.spawns.cByZone[zone]:
                        outfile.write("{"+str(coords[0])+","+str(coords[1])+"},")
                    outfile.write("},")
                outfile.write("},")
            else:
                outfile.write("nil,")
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
                            print(f'Found waypoint with ambigous zone for NPC {npc.name} ({npc.id}). Skipping path.')
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
                if (len(waypointsByZone) > 0):
                    outfile.write("{")
                    for zone in waypointsByZone:
                        outfile.write('['+str(zone)+']={')
                        for path in waypointsByZone[zone]:
                            outfile.write('{')
                            for wp in path:
                                outfile.write('{')
                                outfile.write(f'{wp[0]},{wp[1]}')
                                outfile.write('},')
                            outfile.write('},')
                        outfile.write("},")
                    outfile.write("},")
                else:
                    outfile.write("nil,")
            else:
                outfile.write("nil,")
            outfile.write(str(zoneId)+",") #9
            if hasattr(npc, "start"): #10
                outfile.write("{")
                for quest in npc.start:
                    outfile.write(str(quest)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if hasattr(npc, "end"): #11
                outfile.write("{")
                for quest in npc.end:
                    outfile.write(str(quest)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if hasattr(npc, "faction"): #12
                outfile.write(str(npc.faction)+",")
            else:
                outfile.write("nil,")
                print(f"Error: No faction found for NPC {npc.name} ({npc.id})")
            friendlyTo = ""
            if not npc.hostileToA:
                friendlyTo += "A"
            if not npc.hostileToH:
                friendlyTo += "H"
            if friendlyTo == "": #13
                outfile.write("nil,")
            else:
                outfile.write(f'"{friendlyTo}",')
            if (hasattr(npc, "subName") and npc.subName != None): #14
                outfile.write(f'"{npc.subName}",')
            else:
                outfile.write("nil,")
            if hasattr(npc, "npcFlags"): #15
                outfile.write(f'{str(npc.npcFlags)},')
            else:
                outfile.write("nil,")
            outfile.write("},\n")
        outfile.write("}\n")
