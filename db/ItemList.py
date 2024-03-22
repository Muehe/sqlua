from db.Item import *
from db.Utilities import *

import os.path
import pickle

class ItemList():
    def __init__(self, version):
        self.version = version

    def run(self, dictCursor, locale = "enGB", recache=False):
        if (not os.path.isfile(f'data/{self.version}/items.pkl') or recache):
            tables = self.__getItemTables(dictCursor)
            print('Caching items...')
            self.cacheItems(tables, locale)
        else:
            try:
                with open(f'data/{self.version}/items.pkl', 'rb') as f:
                    self.itemList = pickle.load(f)
                print('Using cached items.')
            except:
                print('ERROR: Something went wrong while loading cached items. Re-caching.')
                tables = self.__getItemTables(dictCursor)
                self.cacheItems(tables, locale)

    def cacheItems(self, tables, locale = 'enGB'):
        self.itemList = {}
        count = len(tables["item_template"])
        print(f'Caching {count} items...')
        for item in tables["item_template"]:
            self.__addItem(item, tables, locale)
            if ((count % 250) == 0):
                print(str(count)+"...")
            count -= 1
        with open(f'data/{self.version}/items.pkl', 'wb') as f:
            pickle.dump(self.itemList, f, protocol=pickle.HIGHEST_PROTOCOL)
        print('Done caching items.')

    def __addItem(self, item, tables, locale = "enGB"):
        """only used by constructor"""
        newItem = Item(item, tables, locale)
        self.itemList[newItem.id] = newItem

    def findItem(self, **kwargs):
        """find one item by keyword = value, ..."""
        return next(self.__iterItem(**kwargs))

    def allItems(self, **kwargs):
        """find all items by keyword = value, ..."""
        return list(self.__iterItem(**kwargs))

    def allItemsWith(self, *args):
        """find all items by keyword, ..."""
        return list(self.__iterItemWith(*args))

    def __iterItemWith(self, *args):
        return (self.itemList[item] for item in self.itemList if hasattr(self.itemList[item], *args))

    def __iterItem(self, **kwargs):
        return (self.itemList[item] for item in self.itemList if self.itemList[item].match(**kwargs))

    def __sortDictById(self, before):
        after = {}
        for key in before:
            after[before[key]["id"]] = before[key]
        return after

    def __getItemTables(self, dictCursor):
        print("Getting item related MySQL tables...")

        ret = {}

        print("  SELECT item_template")
        dictCursor.execute("SELECT entry AS id, name, Flags, startquest, FoodType, ItemLevel, RequiredLevel, ammo_type, class, subclass FROM item_template")
        ret['item_template'] = dictCursor.fetchall()

        print("  SELECT creature_loot_template")
        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM creature_loot_template")
        ret['creature_loot_template'] = {}#dictCursor.fetchall()
        creature_loot_template_lootid = {}#dictCursor.fetchall()
        for a in dictCursor.fetchall():
            if(a['item'] in ret['creature_loot_template']):
                ret['creature_loot_template'][a['item']].append(a)
            else:
                ret['creature_loot_template'][a['item']] = []
                ret['creature_loot_template'][a['item']].append(a)
            
            if(a['id'] in creature_loot_template_lootid):
                creature_loot_template_lootid[a['id']].append(a)
            else:
                creature_loot_template_lootid[a['id']] = []
                creature_loot_template_lootid[a['id']].append(a)

        print("  SELECT gameobject_loot_template")
        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM gameobject_loot_template")
        ret['gameobject_loot_template'] = {}#dictCursor.fetchall()
        gameobject_loot_template_lootid = {}#dictCursor.fetchall()
        for a in dictCursor.fetchall():
            if(a['item'] in ret['gameobject_loot_template']):
                ret['gameobject_loot_template'][a['item']].append(a)
            else:
                ret['gameobject_loot_template'][a['item']] = []
                ret['gameobject_loot_template'][a['item']].append(a)

            if(a['id'] in gameobject_loot_template_lootid):
                gameobject_loot_template_lootid[a['id']].append(a)
            else:
                gameobject_loot_template_lootid[a['id']] = []
                gameobject_loot_template_lootid[a['id']].append(a)

        print("  SELECT item_loot_template")
        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM item_loot_template")
        ret['item_loot_template'] = {}#dictCursor.fetchall()
        #item_loot_template_lootid = {}
        for a in dictCursor.fetchall():
            if(a['item'] in ret['item_loot_template']):
                ret['item_loot_template'][a['item']].append(a)
            else:
                ret['item_loot_template'][a['item']] = []
                ret['item_loot_template'][a['item']].append(a)

            #TODO: Gotta use this to check reference_loot_template
            #if(a['id'] in item_loot_template_lootid):
            #    item_loot_template_lootid[a['id']].append(a)
            #else:
            #    item_loot_template_lootid[a['id']] = []
            #    item_loot_template_lootid[a['id']].append(a)

        print("  SELECT reference_loot_template")
        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM reference_loot_template")

        ret['reference_loot_template'] = {}#dictCursor.fetchall()
        for a in dictCursor.fetchall():
            if(a['id'] in ret['reference_loot_template']):
                ret['reference_loot_template'][a['id']].append(a)
            else:
                ret['reference_loot_template'][a['id']] = []
                ret['reference_loot_template'][a['id']].append(a)

        print("  SELECT gameobject_template")
        dictCursor.execute("SELECT entry AS id, data1, type FROM gameobject_template WHERE type IN(3, 25)")
        oTemplate = dictCursor.fetchall()
        # create loot lookup dict for objects
        ret["ObjectlootIDs"] = {}
        ret["ObjectlootIDsRef"] = {}
        for gameobject in oTemplate:
            if gameobject["data1"] in gameobject_loot_template_lootid:
                for cLootTable in gameobject_loot_template_lootid[gameobject["data1"]]:
                    if cLootTable["mincountOrRef"] > 0:
                        if cLootTable["item"] not in ret["ObjectlootIDs"]:
                            ret["ObjectlootIDs"][cLootTable["item"]] = []
                        if gameobject["id"] not in ret["ObjectlootIDs"][cLootTable["item"]]:
                            ret["ObjectlootIDs"][cLootTable["item"]].append(gameobject["id"])
                    else:
                        refID = abs(cLootTable["mincountOrRef"])
                        for rLootTable in ret['reference_loot_template'][refID]:
                            if rLootTable["mincountOrRef"] > 0:
                                if rLootTable["item"] not in ret["ObjectlootIDsRef"]:
                                    ret["ObjectlootIDsRef"][rLootTable["item"]] = []
                                if gameobject["id"] not in ret["ObjectlootIDsRef"][rLootTable["item"]]:
                                    ret["ObjectlootIDsRef"][rLootTable["item"]].append(gameobject["id"])

        
        print("  SELECT creature_template")
        dictCursor.execute("SELECT entry AS id, LootId, VendorTemplateId FROM creature_template") # PickpocketLootId and SkinningLootId might be good...
        cTemplate = dictCursor.fetchall()
        # create loot lookup table for NPCs
        ret["nlootIDs"] = {}
        ret["nlootIDsRef"] = {}
        for creature in cTemplate:
            if creature["LootId"] in creature_loot_template_lootid:
                for cLootTable in creature_loot_template_lootid[creature["LootId"]]:
                    if cLootTable["mincountOrRef"] > 0:
                        if cLootTable["item"] not in ret["nlootIDs"]:
                            ret["nlootIDs"][cLootTable["item"]] = []
                        if creature["id"] not in ret["nlootIDs"][cLootTable["item"]]:
                            ret["nlootIDs"][cLootTable["item"]].append(creature["id"])
                    else:
                        refID = abs(cLootTable["mincountOrRef"])
                        for rLootTable in ret['reference_loot_template'][refID]:
                            if rLootTable["mincountOrRef"] > 0:
                                if rLootTable["item"] not in ret["nlootIDsRef"]:
                                    ret["nlootIDsRef"][rLootTable["item"]] = []
                                if creature["id"] not in ret["nlootIDsRef"][rLootTable["item"]]:
                                    ret["nlootIDsRef"][rLootTable["item"]].append(creature["id"])

        ret['vendorTempIDs'] = {}
        for creature in cTemplate:
            if creature['VendorTemplateId'] not in ret['vendorTempIDs']:
                ret['vendorTempIDs'][creature['VendorTemplateId']] = []
            ret['vendorTempIDs'][creature['VendorTemplateId']].append(creature['id'])

        print("  SELECT npc_vendor_template")
        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor_template")
        ret['npc_vendor_template'] = {}
        for a in dictCursor.fetchall():
            if(a['item'] in ret['npc_vendor_template']):
                ret['npc_vendor_template'][a['item']].append(a)
            else:
                ret['npc_vendor_template'][a['item']] = []
                ret['npc_vendor_template'][a['item']].append(a)

        print("  SELECT npc_vendor")
        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor")
        ret['npc_vendor'] = {}#dictCursor.fetchall()
        for a in dictCursor.fetchall():
            if(a['item'] in ret['npc_vendor']):
                ret['npc_vendor'][a['item']].append(a)
            else:
                ret['npc_vendor'][a['item']] = []
                ret['npc_vendor'][a['item']].append(a)

        print("  SELECT quest_template")
        dictCursor.execute("SELECT entry AS id, RewChoiceItemId1, RewChoiceItemId2, RewChoiceItemId3,RewChoiceItemId4 ,RewChoiceItemId5, RewChoiceItemId6, RewItemId1, RewItemId2, RewItemId3, RewItemId4 FROM quest_template")
        ret['quest_template'] = dictCursor.fetchall()
        qtemplate = {}
        for quest in ret['quest_template']:
            for key in quest:
                if key != 'id' and quest[key] != 0:
                    if quest[key] in qtemplate:
                        qtemplate[quest[key]].append(quest['id'])
                    else:
                        qtemplate[quest[key]] = []
                        qtemplate[quest[key]].append(quest['id'])
        ret['quest_template'] = qtemplate

        print("Done getting tables.")

        return ret

    def writeFile(self, file = 'output/itemDB.lua'):
        print("  Printing Item file '%s'" % file)
        outfile = open(file, "w", encoding='utf-8')

        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

---@type QuestieDB
local QuestieDB = QuestieLoader:ImportModule("QuestieDB");

QuestieDB.itemKeys = {
    ['name'] = 1, -- string
    ['npcDrops'] = 2, -- table or nil, NPC IDs
    ['objectDrops'] = 3, -- table or nil, object IDs
    ['itemDrops'] = 4, -- table or nil, item IDs
    ['startQuest'] = 5, -- int or nil, ID of the quest started by this item
    ['questRewards'] = 6, -- table or nil, quest IDs
    ['flags'] = 7, -- int or nil, see: https://github.com/cmangos/issues/wiki/Item_template#flags
    ['foodType'] = 8, -- int or nil, see https://github.com/cmangos/issues/wiki/Item_template#foodtype
    ['itemLevel'] = 9, -- int, the level of this item
    ['requiredLevel'] = 10, -- int, the level required to equip/use this item
    ['ammoType'] = 11, -- int,
    ['class'] = 12, -- int,
    ['subClass'] = 13, -- int,
    ['vendors'] = 14, -- table or nil, NPC IDs
    ['relatedQuests'] = 15, -- table or nil, IDs of quests that are related to this item
}

QuestieDB.itemData = [[return {
""")
        outString = ""
        for itemID in self.itemList:
            outString += (f'[{itemID}] = {{')
            item = self.itemList[itemID]

            name = item.name.replace("'","\\'")
            outString += (f"'{name}',") #1
            #2
            if item.npcs:
                outString += ('{')
                outString += ",".join(map(str, sorted(item.npcs)))
                outString += ('},')
            else:
                outString += ('nil,')
            #3
            if item.objects:
                outString += ('{')
                outString += ",".join(map(str, sorted(item.objects)))
                outString += ('},')
            else:
                outString += ('nil,')
            outString = self.getList(outString, item.items) #4

            if hasattr(item, "startQuest") and item.startQuest != 0: #5
                outString += (f'{item.startQuest},')
            else:
                outString += ('nil,')

            if len(item.quests) > 0: #6
                outString += ('{')
                outString += ",".join(map(str, sorted(item.quests)))
                outString += ('},')
            else:
                outString += ('nil,')
            
            if hasattr(item, "flags") and item.flags != 0: #7
                outString += (f'{item.flags},')
            else:
                outString += ('nil,')

            if hasattr(item, "foodType") and item.foodType != 0: #8
                outString += (f"{item.foodType},")
            else:
                outString += ('nil,')
            outString += (f"{item.itemlevel},") #9
            outString += (f"{item.requiredlevel},") #10
            outString += (f"{item.ammoType},") #11
            outString += (f"{item.cls},") #12
            outString += (f"{item.subClass},") #13

            if len(item.vendors) > 0: #14
                outString += ('{')
                outString += ",".join(map(str, sorted(item.vendors)))
                outString += ('},')
            else:
                outString += ('nil,')

            outString += ('},\n')
        # EOF
        outString += ('}]]\n')

        outfile.write(removeTrailingData(outString))
        outfile.close()


    def writeList(self, fd, theList):
        if len(theList) > 0:
            fd.write('{')
            for thing in theList:
                val = 0
                if thing['mincountOrRef'] < 0:
                    val = thing['mincountOrRef']
                else:
                    val = thing['id']
                fd.write(f'{val},')
            fd.write('},')
        else:
            fd.write('nil,')

    def getList(self, fd, theList):
        if len(theList) > 0:
            fd += ('{')
            for thing in theList:
                val = 0
                if thing['mincountOrRef'] < 0:
                    val = thing['mincountOrRef']
                else:
                    val = thing['id']
                fd += (f'{val},')
            fd += ('},')
        else:
            fd += ('nil,')
        return fd
