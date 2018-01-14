from Item import *

class ItemList():
    def __init__(self, dictCursor, locale = "enGB"):
        self.itemList = {}
        # [item_tpl, npc_loot_tpl, obj_loot_tpl, item_loot_tpl, ref_loot_tpl, npc_tpl, obj_tpl, npc_vendor_tpl, npc_vendor, quest_tpl, item_loc_deDE]
        tables = self.__getItemTables(dictCursor)
        if locale == "enGB":
            for item in tables[0]:
                self.__addItem(item, tables[1:])
        elif locale == "deDE":
            for item in tables[0]:
                self.__addItem(item, tables[1:], "deDE")

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
        print("Selecting item related MySQL tables...")

        dictCursor.execute("SELECT entry AS id, name, Flags, startquest FROM item_template")
        item_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM creature_loot_template")
        npc_loot_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM gameobject_loot_template")
        obj_loot_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM item_loot_template")
        item_loot_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM reference_loot_template")
        ref_loot_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, data1 FROM gameobject_template WHERE type = 3")
        obj_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, LootId, VendorTemplateId FROM creature_template") # PickpocketLootId and SkinningLootId might be good...
        npc_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor_template")
        npc_vendor_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor")
        npc_vendor = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, RewChoiceItemId1, RewChoiceItemId2, RewChoiceItemId3,RewChoiceItemId4 ,RewChoiceItemId5, RewChoiceItemId6, RewItemId1, RewItemId2, RewItemId3, RewItemId4 FROM quest_template")
        quest_tpl = dictCursor.fetchall()

        dictCursor.execute("SELECT entry AS id, name_loc3 FROM locales_item")
        item_loc_deDE = self.__sortDictById(dictCursor.fetchall())

        print("Done.")

        return [item_tpl, npc_loot_tpl, obj_loot_tpl, item_loot_tpl, ref_loot_tpl, npc_tpl, obj_tpl, npc_vendor_tpl, npc_vendor, quest_tpl, item_loc_deDE]
