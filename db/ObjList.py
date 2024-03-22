from db.Obj import *
from db.Utilities import *

import os.path
import pickle


class ObjList():
    """Holds a list of Obj() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, version):
        self.version = version
        self.objectList = {}

    def run(self, cursor, extractSpawns=True, recache=False):
        if (not os.path.isfile(f'data/{self.version}/objects.pkl') or recache):
            print('Caching objects...')
            dicts = self.getObjTables(cursor)
            self.cacheObjects(dicts, extractSpawns)
        else:
            try:
                with open(f'data/{self.version}/objects.pkl', 'rb') as f:
                    self.objectList = pickle.load(f)
                print('Using cached objects.')
            except:
                print('ERROR: Something went wrong while loading cached objects. Re-caching.')
                dicts = self.getObjTables(cursor)
                self.cacheObjects(dicts, extractSpawns)

    def cacheObjects(self, dicts, extractSpawns=True):
        count = len(dicts['object_template'])
        print(f'Caching {count} objects...')
        for obj in dicts['object_template']:
            self.addObj(obj, dicts, extractSpawns)
            if ((count % 500) == 0):
                print(str(count)+"...")
            count -= 1
        with open(f'data/{self.version}/objects.pkl', 'wb') as f:
            pickle.dump(self.objectList, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Done caching objects.")

    def addObj(self, obj, dicts, extractSpawns):
        newObj = Obj(obj, dicts, extractSpawns, self.version)
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

    def getObjTables(self, cursor):
        print("Selecting object related MySQL tables...")
        print("  SELECT gameobject_template")
        cursor.execute("SELECT entry, name, type, faction, data1 FROM gameobject_template")
        obj_tpl = []
        for a in cursor.fetchall():
            obj_tpl.append(a)

        if self.version == 'cata':
            print(" SELECT gameobject")
            cursor.execute("SELECT id, map, position_x, position_y, guid FROM gameobject")
            obj = {}
            for a in cursor.fetchall():
                if a[0] not in obj:
                    obj[a[0]] = []
                obj[a[0]].append(a)
        else:
            print('  SELECT gameobject_spawn_entry')
            cursor.execute('SELECT * FROM gameobject_spawn_entry')
            obj_spawn_entry = {}
            for guid, entry in cursor.fetchall():
                if guid not in obj_spawn_entry:
                    obj_spawn_entry[guid] = []
                obj_spawn_entry[guid].append(entry)

            print("  SELECT gameobject")
            cursor.execute("SELECT id, map, position_x, position_y, guid FROM gameobject")
            obj = {}
            for a in cursor.fetchall():
                if (a[0] == 0):
                    if a[4] in obj_spawn_entry:
                        for entry in obj_spawn_entry[a[4]]:
                            if entry not in obj:
                                obj[entry] = []
                            obj[entry].append(a)
                    #else:
                        #print(f'Missing entry for GUID {a[4]}')
                    continue
                elif(a[0] not in obj):
                    obj[a[0]] = []
                obj[a[0]].append(a)

        if self.version == "cata":
            print("  SELECT quest_relation")
            obj_start = {}
            obj_end = {}
            # actor 0=creature, 1=gameobject
            # entry=creature_template.entry or gameobject_template.entry
            # quest=quest_template.entry
            # role 0=start, 1=end
            cursor.execute("SELECT entry, quest, role FROM quest_relations WHERE actor=1")
            for a in cursor.fetchall():
                entry = a[0]
                quest = a[1]
                if a[2] == 0:
                    if quest not in obj_start:
                        obj_start[quest] = []
                    obj_start[quest].append((entry, quest))
                elif a[2] == 1:
                    if quest not in obj_end:
                        obj_end[quest] = []
                    obj_end[quest].append((entry, quest))
        else:
            print("  SELECT gameobject_questrelation")
            cursor.execute("SELECT * FROM gameobject_questrelation")
            obj_start = {}
            for a in cursor.fetchall():
                if(a[0] in obj_start):
                    obj_start[a[0]].append(a)
                else:
                    obj_start[a[0]] = []
                    obj_start[a[0]].append(a)

            print("  SELECT gameobject_involvedrelation")
            cursor.execute("SELECT * FROM gameobject_involvedrelation")
            obj_end = {}
            for a in cursor.fetchall():
                if(a[0] in obj_end):
                    obj_end[a[0]].append(a)
                else:
                    obj_end[a[0]] = []
                    obj_end[a[0]].append(a)

        print("  SELECT locales_gameobject")
        cursor.execute("SELECT * FROM locales_gameobject")
        loc_obj = {}
        for a in cursor.fetchall():
            if(a[0] in loc_obj):
                loc_obj[a[0]].append(a)
            else:
                loc_obj[a[0]] = []
                loc_obj[a[0]].append(a)

        print("Done.")
        return {'object_template':obj_tpl,
                'object':obj,
                'object_start':obj_start,
                'object_end':obj_end,
                'locales_object':loc_obj}

    def printObjFile(self, file='output/objectDB.lua', locale='enGB'):
        print("  Printing Object file '%s'" % file)
        outfile = open(file, "w", encoding='utf-8')
        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

---@type QuestieDB
local QuestieDB = QuestieLoader:ImportModule("QuestieDB");

QuestieDB.objectKeys = {
    ['name'] = 1, -- string
    ['questStarts'] = 2, -- table {questID(int),...}
    ['questEnds'] = 3, -- table {questID(int),...}
    ['spawns'] = 4, -- table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    ['zoneID'] = 5, -- guess as to where this object is most common
    ['factionID'] = 6, -- faction restriction mask (same as spawndb factionid)
}

QuestieDB.objectData = [[return {
""")
        mailBoxes = []
        meetingStones = []
        outString = ""
        for objId in sorted(self.objectList):
            obj = self.objectList[objId]
            if obj.type == 19: #Mailbox
                mailBoxes.append(objId)
            elif obj.type == 23: #Meeting Stone
                meetingStones.append(objId)

            if obj.type not in [2, 3, 5, 8, 10, 19, 23, 25, 32, 34]:
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
            outString += (f'[{obj.id}] = {{"{obj.name}",') #1
            if hasattr(obj, "start"): #2
                outString += ("{")
                for quest in obj.start:
                    outString += (str(quest)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(obj, "end"): #3
                outString += ("{")
                for quest in obj.end:
                    outString += (str(quest)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(obj, "spawns") and len(obj.spawns.cList) > 0: #4
                outString += ("{")
                for zone in obj.spawns.cByZone:
                    if not zone in validZoneList:
                        if zoneId == 0:
                            zoneId = zone
                        outString += ("["+str(zone)+"]={{-1,-1}},") # ,"+str(len(obj.spawns.cByZone[zone]))+"
                        continue
                    if len(obj.spawns.cByZone[zone]) > lenSpawns:
                        lenSpawns = len(obj.spawns.cByZone[zone])
                        zoneId = zone
                    outString += ("["+str(zone)+"]={")
                    for coords in obj.spawns.cByZone[zone]:
                        outString += ("{"+str(coords[0])+","+str(coords[1])+"},")
                    outString += ("},")
                outString += ("},")
            else:
                outString += ("nil,")
            outString += (str(zoneId)+",") #5
            if obj.type == 19: # mailboxes
                outString += (str(obj.faction)+",") #5
            outString += ("},\n")
        outString += ("}]]\n")

        outfile.write(removeTrailingData(outString))
        outfile.close()

        
        outfile = open(file+".meta.lua", "w", encoding='utf-8')
        outfile.write("local mailboxes = ")
        outfile.write("{" + ",".join(map(str, sorted(mailBoxes))) + "}\n")
        outfile.write("local meetingStones = ")
        outfile.write("{" + ",".join(map(str, sorted(meetingStones))) + "}\n")
        outfile.close()
