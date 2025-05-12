from db.ItemList import ItemList

import os.path
import pickle


class MopItemList(ItemList):
    def __init__(self, version):
        super().__init__(version)

    def run(self, dictCursor, locale="enGB", recache=False):
        if not os.path.isfile(f'data/mop/items.pkl') or recache:
            tables = self.__getItemTables(dictCursor)
            print('Caching items...')
            self.cacheItems(tables, locale)
        else:
            try:
                with open(f'data/mop/items.pkl', 'rb') as f:
                    self.itemList = pickle.load(f)
                print('Using cached items.')
            except:
                print('ERROR: Something went wrong while loading cached items. Re-caching.')
                tables = self.__getItemTables(dictCursor)
                self.cacheItems(tables, locale)

    # Trinity does not have item_template because retail has the ItemSparse.db2 file
    def __getItemTables(self, dictCursor):
        print("Getting item related MySQL tables...")

        ret = {}

        print("  SELECT item_template")
        # TODO: Fix ammo_type even though we don't need it?
        # TODO: Do we need FoodType in MoP?
        dictCursor.execute("SELECT entry AS id, name, Flags, startquest, 0 as FoodType, ItemLevel, RequiredLevel, 0 as ammo_type, class, subclass FROM item_template ORDER BY id")
        ret['item_template'] = dictCursor.fetchall()

        print("  SELECT creature_loot_template")
        dictCursor.execute("SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM creature_loot_template")
        ret['creature_loot_template'] = {}
        creature_loot_template_lootid = {}
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
        ret['gameobject_loot_template'] = {}
        gameobject_loot_template_lootid = {}
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
        ret['item_loot_template'] = {}
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

        ret['reference_loot_template'] = {}
        for a in dictCursor.fetchall():
            if(a['item'] in ret['reference_loot_template']):
                ret['reference_loot_template'][a['item']].append(a)
            else:
                ret['reference_loot_template'][a['item']] = []
                ret['reference_loot_template'][a['item']].append(a)

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
                        if refID not in ret['reference_loot_template']:
                            print(f"WARNING: reference_loot_template {refID} not found in gameobject_template")
                            continue

                        for rLootTable in ret['reference_loot_template'][refID]:
                            if rLootTable["mincountOrRef"] > 0:
                                if rLootTable["item"] not in ret["ObjectlootIDsRef"]:
                                    ret["ObjectlootIDsRef"][rLootTable["item"]] = []
                                if gameobject["id"] not in ret["ObjectlootIDsRef"][rLootTable["item"]]:
                                    ret["ObjectlootIDsRef"][rLootTable["item"]].append(gameobject["id"])

        
        # print("  SELECT creature_template")
        # dictCursor.execute("SELECT entry AS id, LootId, VendorTemplateId FROM creature_template") # PickpocketLootId and SkinningLootId might be good...
        # cTemplate = dictCursor.fetchall()
        # create loot lookup table for NPCs
        ret["nlootIDs"] = {}
        ret["nlootIDsRef"] = {}
        # for creature in cTemplate:
        #     if creature["LootId"] in creature_loot_template_lootid:
        #         for cLootTable in creature_loot_template_lootid[creature["LootId"]]:
        #             if cLootTable["mincountOrRef"] > 0:
        #                 if cLootTable["item"] not in ret["nlootIDs"]:
        #                     ret["nlootIDs"][cLootTable["item"]] = []
        #                 if creature["id"] not in ret["nlootIDs"][cLootTable["item"]]:
        #                     ret["nlootIDs"][cLootTable["item"]].append(creature["id"])
        #             else:
        #                 refID = abs(cLootTable["mincountOrRef"])
        #                 for rLootTable in ret['reference_loot_template'][refID]:
        #                     if rLootTable["mincountOrRef"] > 0:
        #                         if rLootTable["item"] not in ret["nlootIDsRef"]:
        #                             ret["nlootIDsRef"][rLootTable["item"]] = []
        #                         if creature["id"] not in ret["nlootIDsRef"][rLootTable["item"]]:
        #                             ret["nlootIDsRef"][rLootTable["item"]].append(creature["id"])

        ret['vendorTempIDs'] = {}
        # for creature in cTemplate:
        #     if creature['VendorTemplateId'] not in ret['vendorTempIDs']:
        #         ret['vendorTempIDs'][creature['VendorTemplateId']] = []
        #     ret['vendorTempIDs'][creature['VendorTemplateId']].append(creature['id'])

        ret['npc_vendor_template'] = {}

        print("  SELECT npc_vendor")
        dictCursor.execute("SELECT entry AS id, item, maxcount, incrtime FROM npc_vendor")
        ret['npc_vendor'] = {}
        for a in dictCursor.fetchall():
            if(a['item'] in ret['npc_vendor']):
                ret['npc_vendor'][a['item']].append(a)
            else:
                ret['npc_vendor'][a['item']] = []
                ret['npc_vendor'][a['item']].append(a)

        print("  SELECT quest_template")
        dictCursor.execute("SELECT id, RewardChoiceItemId1, RewardChoiceItemId2, RewardChoiceItemId3, RewardChoiceItemId4, RewardChoiceItemId5, RewardChoiceItemId6, RewardItemId1, RewardItemId2, RewardItemId3, RewardItemId4 FROM quest_template")
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
