from Obj import *
from Utilities import *

class ObjList():
    """Holds a list of Obj() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, cursor, dictCursor, extractSpawns=True):
        self.objectList = {}
        dicts = self.__getObjTables(cursor, dictCursor)
        print("Adding Objs...")
        count = len(dicts['object_template'])
        for obj in dicts['object_template']:
            self.addObj(obj, dicts, extractSpawns)
            if ((count % 500) == 0):
                print(str(count)+"...")
            count -= 1
        print("Done.")

    def addObj(self, obj, dicts, extractSpawns):
        newObj = Obj(obj, dicts, extractSpawns)
        self.objectList[newObj.id] = newObj

    def findObj(self, **kwargs):
        return next(self.__iterObj(**kwargs))

    def allObjs(self, **kwargs):
        return list(self.__iterObj(**kwargs))

    def allObjsWith(self, *args):
        return list(self.__iterObjWith(*args))

    def __iterObjWith(self, *args):
        return (self.objectList[obj] for obj in self.objectList if hasattr(self.objectList[obj], *args))

    def __iterObj(self, **kwargs):
        return (self.objectList[obj] for obj in self.objectList if self.objectList[obj].match(**kwargs))

    def __getObjTables(self, cursor, dictCursor):
        print("Selecting object related MySQL tables...")
        cursor.execute("SELECT entry, name, type, faction, data1 FROM gameobject_template")
        obj_tpl = []
        for a in cursor.fetchall():
            obj_tpl.append(a)
        cursor.execute("SELECT id, map, position_x, position_y, guid FROM gameobject")
        obj = []
        for a in cursor.fetchall():
            obj.append(a)
        cursor.execute("SELECT * FROM gameobject_questrelation")
        obj_start = []
        for a in cursor.fetchall():
            obj_start.append(a)
        cursor.execute("SELECT * FROM gameobject_involvedrelation")
        obj_end = []
        for a in cursor.fetchall():
            obj_end.append(a)
        count = dictCursor.execute("SELECT * FROM locales_gameobject")
        loc_obj = {}
        for _ in range(0, count):
            q = dictCursor.fetchone()
            loc_obj[q['entry']] = q
        print("Done.")
        return {'object_template':obj_tpl,
                'object':obj,
                'object_start':obj_start,
                'object_end':obj_end,
                'locales_object':loc_obj}

    def printObjFile(self, file='objData.lua', locale='enGB'):
        outfile = open(file, "w")
        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

-------------------------
--Import modules.
-------------------------
---@type QuestieDB
local QuestieDB = QuestieLoader:ImportModule("QuestieDB");

QuestieDB.objectKeys = {
    ['name'] = 1, -- string
    ['questStarts'] = 2, -- table {questID(int),...}
    ['questEnds'] = 3, -- table {questID(int),...}
    ['spawns'] = 4, -- table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    ['zoneID'] = 5, -- guess as to where this object is most common
}

""")
        outfile.write("QuestieDB.objectData = {\n")
        for objId in sorted(self.objectList):
            obj = self.objectList[objId]
            if obj.type not in [2, 3, 5, 8, 10]:
                continue
            #if not hasattr(obj, 'spawns'):
            #    continue
            zoneId = 0
            lenSpawns = 0
            name = obj.name
            if locale != 'enGB':
                if hasattr(obj, 'locales') and obj.locales['name_loc'+str(localesMap[locale])] != None:
                    name = escapeDoubleQuotes(obj.locales['name_loc'+str(localesMap[locale])])
                else:
                    print('Missing translation for Object:', obj.name, '('+str(obj.id)+')' )
            outfile.write(f'[{obj.id}] = {{"{obj.name}",') #1
            if hasattr(obj, "start"): #2
                outfile.write("{")
                for quest in obj.start:
                    outfile.write(str(quest)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if hasattr(obj, "end"): #3
                outfile.write("{")
                for quest in obj.end:
                    outfile.write(str(quest)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if hasattr(obj, "spawns"): #4
                outfile.write("{")
                for zone in obj.spawns.cByZone:
                    if not zone in validZoneList:
                        if zoneId == 0:
                            zoneId = zone
                        outfile.write("["+str(zone)+"]={{-1, -1}},")
                        continue
                    if len(obj.spawns.cByZone[zone]) > lenSpawns:
                        lenSpawns = len(obj.spawns.cByZone[zone])
                        zoneId = zone
                    outfile.write("["+str(zone)+"]={")
                    for coords in obj.spawns.cByZone[zone]:
                        outfile.write("{"+str(coords[0])+","+str(coords[1])+"},")
                    outfile.write("},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            outfile.write(str(zoneId)+",") #5
            outfile.write("},\n")
        outfile.write("}\n")
