from slpp import slpp as lua

import requests
import re

#Look at the bottom of the file on how we combine QuestieCorrections with our own


ItemCorrections = {
  # 2594:{"name":"Woot"},
  32380:{
    "npcs":[20600],
    "objects":[185569]
  }
}

ItemBlacklist = {

}

itemKeys = {
    "name":"name",            # string
    "flags":"flags",             # int or nil, see: https://github.com/cmangos/issues/wiki/Item_template#flags
    "startQuest":"startquest",            # int or nil, ID of the quest started by this item
    "foodType":"foodtype",            # int or nil, see https://github.com/cmangos/issues/wiki/Item_template#foodtype
    "itemLevel":"itemlevel",             # int, the level of this item
    "requiredLevel":"requiredlevel",             # int, the level required to equip/use this item
    "ammoType":"ammoType",            # int, which type of ammo this item is (if applicable). 
    "class":"cls",             # int, the class of the item. see class/subclas breakdown below
    "subClass":"subClass",            # int, the subclass of the item. see class/subclas breakdown below
    "npcDrops":"npcs",             # table or nil, !not! the npc IDs, see lootid: https://github.com/cmangos/issues/wiki/Creature_template#lootid
    "objectDrops":"objects",            # table or nil, !not! the object IDs, see data1: https://github.com/cmangos/issues/wiki/Gameobject_template#data0-23
    "itemDrops":"items",            # table or nil, IDs of the items
    "vendors":"vendors",            # table or nil, IDs of NPCs selling this
    "questRewards":"quests",             # table or nil, IDs of the quests rewarding this
    "relatedQuests":"relatedQuests",            # table or nil, IDs of quests that are related to this item
}

#Change this when Questie is released
#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcItemFixes.lua
QuestieTBCItemCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcItemFixes.lua")
QuestieTBCItemCorrections = r.text
QuestieTBCItemCorrections = re.sub("\-\-.+?\n", "", QuestieTBCItemCorrections)
QuestieTBCItemCorrections = QuestieTBCItemCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieTBCItemCorrections)
QuestieTBCItemCorrections = regRet[0]

#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicItemFixes.lua
QuestieClassicItemCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicItemFixes.lua")
QuestieClassicItemCorrections = r.text
QuestieClassicItemCorrections = re.sub("\-\-.+?\n", "", QuestieClassicItemCorrections)
QuestieClassicItemCorrections = QuestieClassicItemCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieClassicItemCorrections)
QuestieClassicItemCorrections = regRet[0]

#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/QuestieItemBlacklist.lua
QuestieItemBlacklist = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/QuestieItemBlacklist.lua")
QuestieItemBlacklist = r.text
QuestieItemBlacklist = re.sub("\-\-.+?\n", "", QuestieItemBlacklist)
QuestieItemBlacklist = QuestieItemBlacklist.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieItemBlacklist)
QuestieItemBlacklist = regRet[0]




#Replace with the indexes used in the itemObject
for key in itemKeys:
  QuestieTBCItemCorrections = QuestieTBCItemCorrections.replace("itemKeys."+str(key), '"'+str(itemKeys[key])+'"')
  QuestieClassicItemCorrections = QuestieClassicItemCorrections.replace("itemKeys."+str(key), '"'+str(itemKeys[key])+'"')

ClassicData = lua.decode(QuestieClassicItemCorrections)
TBCData =  lua.decode(QuestieTBCItemCorrections)
blacklistData = lua.decode(QuestieItemBlacklist)

def postProcessData(data):
  for id in data:
    if id not in ItemCorrections:
      ItemCorrections[id] = data[id]
    else:
      ItemCorrections[id] = dict(list(data[id].items()) + list(ItemCorrections[id].items()))

for id in blacklistData:
  ItemBlacklist[id] = blacklistData[id]

postProcessData(ClassicData)
postProcessData(TBCData)

print("ItemCorrections Loaded")