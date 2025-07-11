from db.Item import *
from db.Utilities import *

import os.path
import pickle

class ItemList():
    def __init__(self, version, flavor, dictCursor, locale='enGB', recache=False):
        self.version = version
        self.flavor = flavor

        if flavor in ['cmangos']:
            from db.flavor.readCmangosItemList import getItemTables
        elif flavor in ['mangos']:
            from db.flavor.readMangosItemList import getItemTables
        elif flavor in ['trinity']:
            from db.flavor.readTrinityItemList import getItemTables
        elif flavor in ['skyfire']:
            from db.flavor.readSkyfireItemList import getItemTables
        else:
            return

        if (not os.path.isfile(f'data/{version}/{flavor}/items.pkl') or recache):
            print('Caching items...')
            self.cacheItems(getItemTables(dictCursor, version, flavor), locale)
        else:
            try:
                with open(f'data/{version}/{flavor}/items.pkl', 'rb') as f:
                    self.itemList = pickle.load(f)
                print('Using cached items.')
            except:
                print('ERROR: Something went wrong while loading cached items. Re-caching.')
                self.cacheItems(getItemTables(dictCursor, version, flavor), locale)

    def cacheItems(self, tables, locale='enGB'):
        self.itemList = {}
        count = len(tables["item_template"])
        print(f'Caching {count} items...')
        for item in tables["item_template"]:
            self.__addItem(item, tables, locale)
            if ((count % 250) == 0):
                print(str(count)+"...")
            count -= 1
        with open(f'data/{self.version}/{self.flavor}/items.pkl', 'wb') as f:
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
            outString += self.getList(item.items) #4

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

    def getList(self, theList):
        fd = ''
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

    def getDict(self):
        d = {}
        fields = [
            "id",
            "name",
            "flags",
            "startquest",
            "foodtype",
            "itemLevel",
            "requiredLevel",
            "ammoType",
            "cls",
            "subClass",
            "npcs",
            "objects",
            "items",
            "vendors",
            "quests",
        ]
        for i in self.itemList:
            itm = self.itemList[i]
            d[i] = {}
            for field in fields:
                if hasattr(itm, field):
                    d[i][field] = getattr(itm, field)
        return d

    def writeDict(self, filepath=None):
        if filepath == None:
            filepath = f'output/{self.version}/{self.flavor}/itemDump.py'
        writeDict(self.getDict(), filepath)
