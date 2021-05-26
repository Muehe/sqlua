from slpp import slpp as lua
from Corrections.ZoneIDs import ZoneID
import re, requests

npcKeys = {
    "name":"name",             # string
    "minLevel":"minlevel",             # int
    "maxLevel":"maxlevel",             # int
    "rank":"rank",             # int, see https://github.com/cmangos/issues/wiki/creature_template#rank
    "spawns":"spawns",             # table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    "waypoints":"waypoints",            # table {[zoneID(int)] = {coordPair(floatVector2D),...},...}
    "questStarts":"start",             # table {questID(int),...}
    "questEnds":"end",             # table {questID(int),...}
    "factionID":"faction",             # int, see https://github.com/cmangos/issues/wiki/FactionTemplate.dbc
    "friendlyToFaction":"friendlyToFactionFIX",             # string, Contains "A" and/or "H" depending on NPC being friendly towards those factions. nil if hostile to both.
    "subName":"subName",             # string, The title or function of the NPC, e.g. "Weapon Vendor"
    "npcFlags":"npcFlags",            # int, Bitmask containing various flags about the NPCs function (Vendor, Trainer, Flight Master, etc.).
                                  # For flag values see https://github.com/cmangos/mangos-classic/blob/172c005b0a69e342e908f4589b24a6f18246c95e/src/game/Entities/Unit.h#L536
    #unused
    "zoneID":"zoneId"
}

NpcCorrections = {}

NpcBlacklist = {}

NpcQuestieCorrectionsBlacklist = {
  17350:True #Too few spawns in the correction
}

npcFlags = {
    "NONE":0,
    "GOSSIP":1,
    "QUEST_GIVER":2,
    "VENDOR":4,
    "FLIGHT_MASTER":8,
    "TRAINER":16,
    "SPIRIT_HEALER":32,
    "SPIRIT_GUIDE":64,
    "INNKEEPER":128,
    "BANKER":256,
    "PETITIONER":512,
    "TABARD_DESIGNER":1024,
    "BATTLEMASTER":2048,
    "AUCTIONEER":4096,
    "STABLEMASTER":8192,
    "REPAIR":16384
}
#QuestieDB.npcFlags = _Questie_IsTBC and {
#    NONE = 0,
#    GOSSIP = 1,
#    QUEST_GIVER = 2,
#    TRAINER = 16,
#    VENDOR = 128,
#    REPAIR = 4096,
#    FLIGHT_MASTER = 8192,
#    SPIRIT_HEALER = 16384,
#    SPIRIT_GUIDE = 32768,
#    INNKEEPER = 65536,
#    BANKER = 131072,
#    PETITIONER = 262144,
#    TABARD_DESIGNER = 524288,
#    BATTLEMASTER = 1048576,
#    AUCTIONEER = 2097152,
#    STABLEMASTER = 4194304,
#} or {
#    NONE = 0,
#    GOSSIP = 1,
#    QUEST_GIVER = 2,
#    VENDOR = 4,
#    FLIGHT_MASTER = 8,
#    TRAINER = 16,
#    SPIRIT_HEALER = 32,
#    SPIRIT_GUIDE = 64,
#    INNKEEPER = 128,
#    BANKER = 256,
#    PETITIONER = 512,
#    TABARD_DESIGNER = 1024,
#    BATTLEMASTER = 2048,
#    AUCTIONEER = 4096,
#    STABLEMASTER = 8192,
#    REPAIR = 16384
#}

#Change this when Questie is released
#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicNPCFixes.lua
QuestieClassicNpcCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicNPCFixes.lua")
QuestieClassicNpcCorrections = r.text
QuestieClassicNpcCorrections = re.sub("\-\-\[\[.*\]\]", "", QuestieClassicNpcCorrections)
#Remove a comment structure that exist in the file for graveyards
start = QuestieClassicNpcCorrections.find("[[")
end = QuestieClassicNpcCorrections.find("]]")
start = QuestieClassicNpcCorrections[:start]
end = QuestieClassicNpcCorrections[end:]
QuestieClassicNpcCorrections = start + end
QuestieClassicNpcCorrections = re.sub("\-\-.+?\n", "", QuestieClassicNpcCorrections)
QuestieClassicNpcCorrections = QuestieClassicNpcCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieClassicNpcCorrections)
QuestieClassicNpcCorrections = regRet[0]

#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcNPCFixes.lua
QuestieTBCNpcCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcNPCFixes.lua")
QuestieTBCNpcCorrections = r.text
QuestieTBCNpcCorrections = re.sub("\-\-.+?\n", "", QuestieTBCNpcCorrections)
QuestieTBCNpcCorrections = QuestieTBCNpcCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieTBCNpcCorrections)
QuestieTBCNpcCorrections = regRet[0]

#Replace with the indexes used in the itemObject
for key in npcKeys:
  QuestieClassicNpcCorrections = QuestieClassicNpcCorrections.replace("npcKeys."+str(key), '"'+str(npcKeys[key])+'"')
  QuestieTBCNpcCorrections = QuestieTBCNpcCorrections.replace("npcKeys."+str(key), '"'+str(npcKeys[key])+'"')

for key in ZoneID:
  QuestieClassicNpcCorrections = QuestieClassicNpcCorrections.replace("zoneIDs."+str(key), str(ZoneID[key]))
  QuestieTBCNpcCorrections = QuestieTBCNpcCorrections.replace("zoneIDs."+str(key), str(ZoneID[key]))

for key in npcFlags:
  QuestieClassicNpcCorrections = QuestieClassicNpcCorrections.replace("npcFlags."+str(key), str(npcFlags[key]))
  QuestieTBCNpcCorrections = QuestieTBCNpcCorrections.replace("npcFlags."+str(key), str(npcFlags[key]))

ClassicData = lua.decode(QuestieClassicNpcCorrections)
TBCData = lua.decode(QuestieTBCNpcCorrections)

def postProcessData(data):
  for id in data:
    if id in NpcQuestieCorrectionsBlacklist:
      continue
    if id not in NpcCorrections:
      NpcCorrections[id] = {}
    npcData = data[id]
    if "friendlyToFactionFIX" in npcData:
      if "AH" in npcData["friendlyToFactionFIX"]:
        data[id]["hostileToA"] = False
        data[id]["hostileToH"] = False
      elif "A" in npcData["friendlyToFactionFIX"]:
        data[id]["hostileToA"] = False
        data[id]["hostileToH"] = True
      elif "H" in npcData["friendlyToFactionFIX"]:
        data[id]["hostileToA"] = True
        data[id]["hostileToH"] = False
      else:
        data[id]["hostileToA"] = True
        data[id]["hostileToH"] = True

    NpcCorrections[id] = dict(list(data[id].items()) + list(NpcCorrections[id].items()))

postProcessData(ClassicData)
postProcessData(TBCData)

print("NpcCorrections Loaded")