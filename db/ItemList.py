from db.Item import *

import os.path
import pickle

class ItemList():
    def __init__(self, dictCursor, version, locale = "enGB", recache = False):
        self.version = version
        if (not os.path.isfile(f'data/{version}/items.pkl') or recache):
            print('Caching items...')
            self.cacheItems(dictCursor, locale)
        else:
            try:
                with open(f'data/{version}/items.pkl', 'rb') as f:
                    self.itemList = pickle.load(f)
                print('Using cached items.')
            except:
                print('ERROR: Something went wrong while loading cached items. Re-caching.')
                self.cacheItems(dictCursor, locale)

    def cacheItems(self, dictCursor, locale = 'enGB'):
        self.itemList = {}
        tables = self.__getItemTables(dictCursor)
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

        dictCursor.execute("SELECT entry AS id, name, Flags, startquest, FoodType, ItemLevel, RequiredLevel, ammo_type, class, subclass FROM item_template")
        ret['item_template'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM creature_loot_template")
        ret['creature_loot_template'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM gameobject_loot_template")
        ret['gameobject_loot_template'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM item_loot_template")
        ret['item_loot_template'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM reference_loot_template")
        ret['reference_loot_template'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, data1 FROM gameobject_template WHERE type IN(3, 25)")
        a = dictCursor.fetchall()
        # create loot lookup dict for objects
        b = {}
        for x in a:
            if x['data1'] not in b:
                b[x['data1']] = []
            b[x['data1']].append(x['id'])
        ret['gameobject_template'] = a
        ret['data1'] = b
        dictCursor.execute("SELECT entry AS id, LootId, VendorTemplateId FROM creature_template") # PickpocketLootId and SkinningLootId might be good...
        a = dictCursor.fetchall()
        # create loot lookup table for NPCs
        b = {}
        for x in a:
            if x['LootId'] not in b:
                b[x['LootId']] = []
            b[x['LootId']].append(x['id'])
        ret['creature_template'] = a
        ret['lootIDs'] = b

        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor_template")
        ret['npc_vendor_template'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor")
        ret['npc_vendor'] = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, RewChoiceItemId1, RewChoiceItemId2, RewChoiceItemId3,RewChoiceItemId4 ,RewChoiceItemId5, RewChoiceItemId6, RewItemId1, RewItemId2, RewItemId3, RewItemId4 FROM quest_template")
        ret['quest_template'] = dictCursor.fetchall()

        print("Done getting tables.")

        return ret

    def writeFile(self, file = 'output/itemDB.lua'):
        fo = open(file, "w")

        fo.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

-------------------------
--Import modules.
-------------------------
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

QuestieDB.items = {
""")

        for itemID in self.itemList:
            fo.write(f'[{itemID}] = {{')
            item = self.itemList[itemID]

            name = item.name.replace("'","\\'")
            fo.write(f"'{name}',") #1
            #2
            if item.npcs:
                fo.write('{')
                for npc in item.npcs:
                    fo.write(f'{npc},')
                fo.write('},',)
            else:
                fo.write('nil,')
            #3
            if item.objects:
                fo.write('{')
                for objectID in item.objects:
                    fo.write(f'{objectID},')
                fo.write('},',)
            else:
                fo.write('nil,')
            self.writeList(fo, item.items) #4
            fo.write(f"{item.startquest}," if item.startquest != 0 else 'nil,') #5
            if len(item.quests) > 0: #6
                fo.write('{')
                for thing in item.quests:
                    fo.write(f'{thing},')
                fo.write('},',)
            else:
                fo.write('nil,')
            fo.write(f"{item.flags}," if item.flags != 0 else 'nil,') #7

            fo.write(f"{item.foodtype}," if item.foodtype != 0 else 'nil,') #8
            fo.write(f"{item.itemlevel},") #9
            fo.write(f"{item.requiredlevel},") #10
            fo.write(f"{item.ammoType},") #11
            fo.write(f"{item.cls},") #12
            fo.write(f"{item.subClass},") #13

            if len(item.vendors) > 0: #14
                fo.write('{')
                for thing in item.vendors:
                    fo.write(f'{thing["id"]},')
                fo.write('},',)
            else:
                fo.write('nil,')

            fo.write('},\n')
        # EOF
        fo.write('}\n')


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
