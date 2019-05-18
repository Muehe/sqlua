from Npc import *
from Utilities import *

class NpcList():
    """Holds a list of Npc() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, cursor, dictCursor, extractSpawns = True):
        self.nList = {}
        dicts = self.__getNpcTables(cursor, dictCursor)
        print("Adding Npcs...")
        count = len(dicts['npc_template'])
        for npc in dicts['npc_template']:
            self.addNpc(npc, dicts, extractSpawns)
            if ((count % 100) == 0):
                print(str(count)+"...")
            count -= 1
        print("Done.")

    def addNpc(self, npc, tables, extractSpawns):
        newNpc = Npc(npc, tables, extractSpawns)
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

    def __getNpcTables(self, cursor, dictCursor):
        print("Selecting NPC related MySQL tables...")
        cursor.execute("SELECT entry, name, minlevel, maxlevel, minlevelhealth, maxlevelhealth, rank, Faction FROM creature_template")
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

    def printNpcFile(self, file='npcData.lua', locale='enGB'):
        outfile = open(file, "w")
        outfile.write("npcData = {\n")
        for npcId in sorted(self.nList):
            npc = self.nList[npcId]
            #if (not hasattr(npc, "spawns")) and (not hasattr(npc, "waypoints")):
            #    continue
            zoneId = 0
            lenSpawns = 0
            name = npc.name
            if locale != 'enGB' and hasattr(npc, 'locales') and npc.locales['name_loc'+str(localesMap[locale])] != None:
                name = escapeQuotes(npc.locales['name_loc'+str(localesMap[locale])])
            outfile.write("["+str(npc.id)+"] = {'"+name+"',"+str(npc.minlevelhealth)+","+str(npc.maxlevelhealth)+","+str(npc.minlevel)+","+str(npc.maxlevel)+","+str(npc.rank)+",")
            if hasattr(npc, "spawns"):
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
            if hasattr(npc, "waypoints"):
                outfile.write("{")
                for zone in npc.waypoints.cByZone:
                    if not zone in validZoneList:
                        if zoneId == 0:
                            zoneId = zone
                        outfile.write("["+str(zone)+"]={{-1, -1}},")
                        continue
                    outfile.write("["+str(zone)+"]={")
                    for coords in npc.waypoints.cByZone[zone]:
                        outfile.write("{"+str(coords[0])+","+str(coords[1])+"},")
                    outfile.write("},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            outfile.write(str(zoneId)+",")
            if hasattr(npc, "start"):
                outfile.write("{")
                for quest in npc.start:
                    outfile.write(str(quest)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if hasattr(npc, "end"):
                outfile.write("{")
                for quest in npc.end:
                    outfile.write(str(quest)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            outfile.write("},\n")
        outfile.write("}\n")
