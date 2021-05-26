from slpp import slpp as lua
from Corrections.ZoneIDs import ZoneID
import re, requests

objectKeys = {
    "name":"name",         # string
    "questStarts":"start",        # table {questID(int),...}
    "questEnds":"end",        # table {questID(int),...}
    "spawns":"spawns",         # table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    "zoneID":"zoneId",         # guess as to where this object is most common
    "factionID":"factionID",        # faction restriction mask (same as spawndb factionid)
}

ObjectCorrections = {}

ObjectBlacklist = {
    324:True, #Small Thorium Vein
    1617:True, #Silverleaf
    1618:True, #Peacebloom
    3724:True, #Peacebloom
    1619:True, #Earthroot
    3726:True, #Earthroot
    1624:True, #Kingsblood
    1731:True, #Copper Vein
    2055:True, #Copper Vein
    3763:True, #Copper Vein
    103713:True, #Copper Vein
    181248:True, #Copper Vein Ghostlands
    1732:True, #Tin Vein
    2054:True, #Tin Vein
    3764:True, #Tin Vein
    103711:True, #Tin Vein
    181249:True, #Tin Vein Ghostlands
    1733:True, #Silver Vein
    1734:True, #Gold Vein
    1735:True, #Iron Deposit
    2040:True, #Mithril Deposit
    2041:True, #Liferoot
    2045:True, #Stranglekelp
    2047:True, #Truesilver Deposit
    2866:True, #Firebloom
    105569:True, #Silver Vein
    123309:True, #Ooze Covered Truesilver Deposit
    73941:True,  #-||- gold vein
    123310:True, #-||- mithril Deposit
    123848:True, #-||- Thorium Vein
    177388:True, #-||- Rich Thorium Vein
    142141:True, #Arthas Tears
    176642:True, #Arthas Tears
    142145:True, #Gromsblood
    176637:True, #Gromsblood
    150079:True, #Mithril Deposit
    176645:True, #Mithril Deposit
    150080:True, #Gold Vein
    150081:True, #Truesilver Deposit
    150082:True, #Small Thorium Vein
    176643:True, #Small Thorium Vein
    165658:True, #Dark Iron Deposit
    175404:True, #Rich Thorium Vein
    176587:True, #Plaguebloom
    176641:True, #Plaguebloom
    181108:True, #Truesilver Deposit
    181109:True, #Gold Vein
    181555:True, #Fel Iron Deposit
    181556:True, #Adamantite Deposit
    181557:True, #Khorium Vein
    181569:True, #Rich Adamantite Deposit
    181570:True, #Rich Adamantite Deposit

    #Food crates / Barrels etc.
    3658:True,      #Water Barrel
    3705:True,      #Barrel of Milk
    3714:True,      #Alliance Strongbox
    105570:True,    #Alliance Strongbox

    #Food Crate
    3694:True,      #Food Crate
    153471:True,    #Food Crate
    3662:True,      #Food Crate
    3690:True,      #Food Crate
    3691:True,      #Food Crate
    3693:True,      #Food Crate
    3695:True,      #Food Crate
    3707:True,      #Food Crate
    3719:True,      #Food Crate
    153470:True,    #Food Crate
    153472:True,    #Food Crate
    153473:True,    #Food Crate


    #Chests
    #Battered Chest
    2843:True,      #Battered Chest
    106319:True,    #Battered Chest
    106318:True,    #Battered Chest
    2849:True,      #Battered Chest
    75293:True,     #Large Battered Chest
     
    #Solid Chest
    2852:True,      #Solid Chest
    2850:True,      #Solid Chest
    75298:True,     #Large Solid Chest
    153464:True,    #Large Solid Chest
    2857:True,      #Solid Chest
    4149:True,      #Solid Chest
    75299:True,     #Large Solid Chest
    153463:True,    #Large Solid Chest
    75300:True,     #Large Solid Chest
    74448:True,     #Large Solid Chest
    153453:True,    #Solid Chest
    153454:True,    #Solid Chest
    153451:True,    #Solid Chest
    2855:True,      #Solid Chest
    184930:True,    #Solid Fel Iron Chest
    184935:True,    #Solid Fel Iron Chest
    184933:True,    #Solid Fel Iron Chest
    184937:True,    #Solid Adamantite Chest

    #B/T-attered chest (Looks like TBC chest?)
    2844:True,
    2845:True, #Eversong Woods
    2846:True, #Bloodmyst Isle
    2847:True, #Ghostlands

    #Quest Objects
    112877:True,    #Talvash's Scrying Bowl Created by: https://tbc.wowhead.com/item=7667/talvashs-phial-of-scrying
    #10076:True,     #Scrying Bowl Created by: https://tbc.wowhead.com/item=5251/phial-of-scrying
}

#Change this when Questie is released
#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicObjectFixes.lua
QuestieClassicObjectCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicObjectFixes.lua")
QuestieClassicObjectCorrections = r.text
QuestieClassicObjectCorrections = re.sub("\-\-.+?\n", "", QuestieClassicObjectCorrections)
QuestieClassicObjectCorrections = QuestieClassicObjectCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieClassicObjectCorrections)
QuestieClassicObjectCorrections = regRet[0]

#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcObjectFixes.lua
QuestieTBCObjectCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcObjectFixes.lua")
QuestieTBCObjectCorrections = r.text
QuestieTBCObjectCorrections = re.sub("\-\-.+?\n", "", QuestieTBCObjectCorrections)
QuestieTBCObjectCorrections = QuestieTBCObjectCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieTBCObjectCorrections)
QuestieTBCObjectCorrections = regRet[0]


#Replace with the indexes used in the itemObject
for key in objectKeys:
  QuestieClassicObjectCorrections = QuestieClassicObjectCorrections.replace("objectKeys."+str(key), '"'+str(objectKeys[key])+'"')
  QuestieTBCObjectCorrections = QuestieTBCObjectCorrections.replace("objectKeys."+str(key), '"'+str(objectKeys[key])+'"')

for key in ZoneID:
  QuestieClassicObjectCorrections = QuestieClassicObjectCorrections.replace("zoneIDs."+str(key), str(ZoneID[key]))
  QuestieTBCObjectCorrections = QuestieTBCObjectCorrections.replace("zoneIDs."+str(key), str(ZoneID[key]))

ClassicData = lua.decode(QuestieClassicObjectCorrections)
TBCData = lua.decode(QuestieTBCObjectCorrections)

def postProcessData(data):
  for id in data:
    if id not in ObjectCorrections:
      ObjectCorrections[id] = data[id]
    else:
      ObjectCorrections[id] = dict(list(data[id].items()) + list(ObjectCorrections[id].items()))

postProcessData(ClassicData)
postProcessData(TBCData)

print("ObjectCorrections Loaded")