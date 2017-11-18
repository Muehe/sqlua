class Item():
    def __init__(self, item, tables, locale='enGB'):
        # tables =  [npc_loot_tpl, obj_loot_tpl, item_loot_tpl, ref_loot_tpl, npc_tpl, obj_tpl, npc_vendor_tpl, npc_vendor, quest_tpl, item_loc_deDE]
        self.id = item["id"]
        if locale == 'deDE' and self.id in tables[9]:
            self.name = tables[9][self.id]["name"]
        else:
            self.name = item["name"]

        if 4 & item["Flags"]:
            self.lootable = True
        else:
            self.lootable = False
        if item["startquest"] != 0:
            self.startquest = item["startquest"]

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        for (key, val) in kwargs.items():
            if not (hasattr(self, key)):
                return False
        return all(getattr(self,key) == val for (key, val) in kwargs.items())
