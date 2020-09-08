class Item():
    def __init__(self, item, tables, locale='enGB'):
        self.id = item['id']
        self.name = item['name']
        self.flags = item['Flags']
        self.startquest = item['startquest']
        self.foodtype = item['FoodType']
        self.itemlevel = item['ItemLevel']
        self.requiredlevel = item['RequiredLevel']
        self.ammoType = item['ammo_type']
        self.cls = item['class']
        self.subClass = item['subclass']

        # check if item is lootable, i.e. a container like clams
        if 4 & item['Flags']:
            self.lootable = True
        else:
            self.lootable = False

        # create list of NPC loot table entries containing this item
        lootIDs = self.get(self.id, 'item', tables['creature_loot_template'])
        # translate LootId (id) field to NPC IDs
        self.npcs = []
        for loot in lootIDs:
            for npcID in tables['lootIDs'][loot['id']]:
                if npcID not in self.npcs:
                    self.npcs.append(npcID)
        # create list of object loot table entries containing this item
        dates = self.get(self.id, 'item', tables['gameobject_loot_template'])
        # translate data1 (id) field to object IDs
        self.objects = []
        for loot in dates:
            if loot['id'] not in tables['data1']:
                print(f'No object found for {loot} of item {self.name} ({self.id})')
                continue
            for objectID in tables['data1'][loot['id']]:
                if objectID not in self.objects:
                    self.objects.append(objectID)
        self.items = self.get(self.id, 'item', tables['item_loot_template'])
        # self.references = self.get(self.id, 'item', tables['reference_loot_template'])
        # TODO merging references
        self.vendors = list(filter(lambda step: step['item'] == self.id, tables['npc_vendor']))
        self.quests = []
        for quest in tables['quest_template']:
            for key in quest:
                if key != 'id' and quest[key] == self.id:
                    self.quests.append(quest['id'])
                    break

        self.drops = len(self.npcs) + len(self.objects) + len(self.items) + len(self.vendors) + len(self.quests)

    def __repr__(self):
        return str(self.id)

    def get(self, needle, field, stack):
        temp = list(filter(lambda step: step[field] == needle and not self.isReference(step), stack))
        return temp

    def isReference(self, loot):
        if loot['mincountOrRef'] < 0:
            return True
        else:
            return False
