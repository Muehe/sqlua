class Item():
    def __init__(self, item, tables, locale='enGB'):
        self.id = item['id']
        self.name = item['name']
        self.flags = item['Flags']
        self.startquest = item['startquest']
        self.foodtype = item['FoodType']
        self.itemlevel = item['ItemLevel']
        self.requiredlevel = item['RequiredLevel']

        # check if item is lootable, i.e. a container like clams
        if 4 & item['Flags']:
            self.lootable = True
        else:
            self.lootable = False

        self.npcs = self.get(self.id, 'item', tables['creature_loot_template'])
        self.objects = self.get(self.id, 'item', tables['gameobject_loot_template'])
        self.items = self.get(self.id, 'item', tables['item_loot_template'])
        # self.references = self.get(self.id, 'item', tables['reference_loot_template'])
        # TODO replacing lootid/data1, merging references
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
