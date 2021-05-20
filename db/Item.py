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
        # translate LootId (id) field to NPC IDs
        self.npcs = []
        if self.id in tables["nlootIDs"]:
            self.npcs = tables["nlootIDs"][self.id]

        # Add loots for quest items only.
        # This is basically culling information, otherwise the file explodes in size
        if self.id in tables["nlootIDsRef"] and len(tables["nlootIDsRef"][self.id]) > 0 and self.cls == 12:
            self.npcs += tables["nlootIDsRef"][self.id]
            #print(str(self.id) + " : " + self.name)

        # create list of object loot table entries containing this item
        # translate data1 (id) field to object IDs
        self.objects = []
        if self.id in tables["ObjectlootIDs"]:
            self.objects = tables["ObjectlootIDs"][self.id]

        # Add loots for quest items only.
        # This is basically culling information, otherwise the file explodes in size
        if self.id in tables["ObjectlootIDsRef"] and len(tables["ObjectlootIDsRef"][self.id]) > 0 and self.cls == 12:
            self.objects += tables["ObjectlootIDsRef"][self.id]
            #print(str(self.id) + " : " + self.name)


        self.items = []
        if self.id in tables['item_loot_template']:
            self.items = self.get(self.id, 'item', tables['item_loot_template'][self.id])

        # create list of NPC vendor table entries containing this item
        self.vendors = []
        if self.id in tables['npc_vendor']:
            for vendor in tables['npc_vendor'][self.id]:
                self.vendors.append(vendor["id"])

        # translate VendorTemplateId (id) field to NPC IDs
        if self.id in tables['npc_vendor_template']:
            for vendor in tables['npc_vendor_template'][self.id]:
                if vendor['id'] in tables['vendorTempIDs']:
                    for npcID in tables['vendorTempIDs'][vendor['id']]:
                        if npcID not in self.vendors:
                            self.vendors.append(npcID)
        

        self.quests = []
        if self.id in tables['quest_template']:
            self.quests = tables['quest_template'][self.id]

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
