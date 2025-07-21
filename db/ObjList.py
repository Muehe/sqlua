from db.Obj import *
from db.Utilities import *

import os.path
import pickle


class ObjList():
    """Holds a list of Obj() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, version, flavor, cursor, extractSpawns=True, recache=False):
        self.version = version
        self.flavor = flavor
        self.objectList = {}

        if flavor == 'cmangos':
            from db.flavor.readCmangosObjList import getObjTables
        elif flavor == 'mangos':
            from db.flavor.readMangosObjList import getObjTables
        elif flavor == 'trinity':
            from db.flavor.readTrinityObjList import getObjTables
        elif flavor == 'skyfire':
            from db.flavor.readSkyfireObjList import getObjTables

        if (not os.path.isfile(f'data/{version}/{flavor}/objects.pkl') or recache):
            print('Caching objects...')
            self.cacheObjects(getObjTables(cursor), extractSpawns)
        else:
            try:
                with open(f'data/{version}/{flavor}/objects.pkl', 'rb') as f:
                    self.objectList = pickle.load(f)
                print('Using cached objects.')
            except:
                print('ERROR: Something went wrong while loading cached objects. Re-caching.')
                self.cacheObjects(getObjTables(cursor), extractSpawns)

    def cacheObjects(self, dicts, extractSpawns=True):
        count = len(dicts['object_template'])
        print(f'Caching {count} objects...')
        for obj in dicts['object_template']:
            self.addObj(obj, dicts, extractSpawns)
            if ((count % 500) == 0):
                print(str(count)+"...")
            count -= 1
        with open(f'data/{self.version}/{self.flavor}/objects.pkl', 'wb') as f:
            pickle.dump(self.objectList, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Done caching objects.")

    def addObj(self, obj, dicts, extractSpawns):
        newObj = Obj(obj, dicts, extractSpawns, self.version, self.flavor)
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

            if obj.type not in [2, 3, 5, 8, 10, 19, 22, 23, 25, 32, 34]:
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
                    if isInstance(zone):
                        if zoneId == 0:
                            zoneId = zone
                        outString += ("["+str(zone)+"]={{-1,-1}},") # ,"+str(len(obj.spawns.cByZone[zone]))+"
                        continue
                    if len(obj.spawns.cByZone[zone]) > lenSpawns:
                        lenSpawns = len(obj.spawns.cByZone[zone])
                        zoneId = zone
                    outString += ("["+str(zone)+"]={")
                    for coords in obj.spawns.cByZone[zone]:
                        if len(coords) == 3:
                            outString += ("{"+str(coords[0])+","+str(coords[1])+","+str(coords[2])+"},")
                        else:
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

    def getDict(self):
        d = {}
        fields = [
            "id",
            "name",
            "type",
            "faction",
            "data1",
            "spawns",
            "start",
            "end",
        ]
        for o in self.objectList:
            obj = self.objectList[o]
            d[o] = {}
            for field in fields:
                if hasattr(obj, field):
                    d[o][field] = getattr(obj, field)
        return d

    def writeDict(self, filepath=None):
        if filepath == None:
            filepath = f'output/{self.version}/{self.flavor}/objectDump.py'
        writeDict(self.getDict(), filepath)
