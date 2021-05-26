from slpp import slpp as lua
from Corrections.ZoneIDs import ZoneID
from RaceIDs import raceKeys
import re, requests, json

QuestCorrections = {
  #9711:{
  #  "triggerEnd":[
  #    ["Matis the Cruel Captured", {ZoneID["BLOODMYST_ISLE"]:[[32.74,48.02],[29.51,51.36],[25.63,53.52],[37.81,46.44],[40.88,45.13]]}]
  #  ],
  #},
}

quest_data_minLevel_xp_json = open("data/WoWHead-Data/quest_data_tbc_mLvl_xp.json", "r")
wowheadQuestJSON = json.loads(quest_data_minLevel_xp_json.read())
wowheadQuest = {}
for quest in wowheadQuestJSON:
    questId = int(quest["id"])
    if(quest["minLevel"] != None):
        if questId not in QuestCorrections:
          QuestCorrections[questId] = {}
        if questId in QuestCorrections and not hasattr(QuestCorrections[questId], "MinLevel"):
          QuestCorrections[questId]["MinLevel"] = int(quest["minLevel"])
    if(quest["experience"] != None):
      if questId not in QuestCorrections:
          QuestCorrections[questId] = {}   
      if questId in QuestCorrections and not hasattr(QuestCorrections[questId], "experience"):
          QuestCorrections[questId]["experience"] = int(quest["experience"])


#Not yet implemented
#StartedBy, FinishedBy, Objectives
questKeys = {
    "name":"Title",                # string
    "startedBy":"startedByFIX",                 # table
        #"creatureStart":1,                # table {creature(int),...}
        #"objectStart":2,                # table {object(int),...}
        #"itemStart":3,                # table {item(int),...}
    "finishedBy":"finishedByFIX",                # table
        #"creatureEnd":1,                # table {creature(int),...}
        #"objectEnd":2,                # table {object(int),...}
    "requiredLevel":"MinLevel",                 # int
    "questLevel":"QuestLevel",                # int
    "requiredRaces":"RequiredRaces",                 # bitmask
    "requiredClasses":"RequiredClasses",                 # bitmask
    "objectivesText":"ObjectivesTextFIX",                # table: {string,...}, Description of the quest. Auto-complete if nil.
    "triggerEnd":"triggerEnd",                # table: {text, {[zoneID] = {coordPair,...},...}}
    "objectives":"objectivesFIX",                 # table
        #"creatureObjective":1,                # table {{creature(int), text(string)},...}, If text is nil the default "<Name> slain x/y" is used
        #"objectObjective":2,                # table {{object(int), text(string)},...}
        #"itemObjective":3,                # table {{item(int), text(string)},...}
        #"reputationObjective":4,                # table: {faction(int), value(int)}
    "sourceItemId":"SrcItemId",                 # int, item provided by quest starter
    "preQuestGroup":"PreQuestGroup",                # table: {quest(int)}
    "preQuestSingle":"PreQuestSingle",                 # table: {quest(int)}
    "childQuests":"ChildQuests",                # table: {quest(int)}
    "inGroupWith":"InGroupWith",                # table: {quest(int)}
    "exclusiveTo":"ExclusiveTo",                # table: {quest(int)}
    "zoneOrSort":"ZoneOrSort",                 # int, >0: AreaTable.dbc ID; <0: QuestSort.dbc ID
    "requiredSkill":"RequiredSkillFIX",                # table: {skill(int), value(int)}
    "requiredMinRep":"RequiredMinRepFactionFIX",                 # table: {faction(int), value(int)}
    "requiredMaxRep":"RequiredMaxRepFactionFIX",                 # table: {faction(int), value(int)}
    "requiredSourceItems":"ReqSourceId",                # table: {item(int), ...} Items that are not an objective but still needed for the quest.
    "nextQuestInChain":"NextQuestInChain",                 # int: if this quest is active/finished, the current quest is not available anymore
    "questFlags":"QuestFlags",                 # bitmask: see https://github.com/cmangos/issues/wiki/Quest_template#questflags
    "specialFlags":"SpecialFlags",                 # bitmask: 1 = Repeatable, 2 = Needs event, 4 = Monthly reset (req. 1). See https://github.com/cmangos/issues/wiki/Quest_template#specialflags
    "parentQuest":"ParentQuest",                # int, the ID of the parent quest that needs to be active for the current one to be available. See also 'childQuests' (field 14)
}

#Change this when Questie is released
#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicQuestFixes.lua
QuestieClassicQuestCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/Classic/classicQuestFixes.lua")
QuestieClassicQuestCorrections = r.text
QuestieClassicQuestCorrections = re.sub("\-\-.+?\n", "", QuestieClassicQuestCorrections)
QuestieClassicQuestCorrections = QuestieClassicQuestCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieClassicQuestCorrections)
QuestieClassicQuestCorrections = regRet[0]

#https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcQuestFixes.lua
QuestieTBCQuestCorrections = ""
r = requests.get("https://raw.githubusercontent.com/Questie/Questie/master/Database/Corrections/TBC/tbcQuestFixes.lua")
QuestieTBCQuestCorrections = r.text
QuestieTBCQuestCorrections = re.sub("\-\-.+?\n", "", QuestieTBCQuestCorrections)
QuestieTBCQuestCorrections = QuestieTBCQuestCorrections.replace("""\n""", " ")
regRet = re.findall("return (\{.*?\}) end", QuestieTBCQuestCorrections)
QuestieTBCQuestCorrections = regRet[0]

#Replace with the indexes used in the itemObject
for key in questKeys:
  QuestieClassicQuestCorrections = QuestieClassicQuestCorrections.replace("questKeys."+str(key), '"'+str(questKeys[key])+'"')
  QuestieTBCQuestCorrections = QuestieTBCQuestCorrections.replace("questKeys."+str(key), '"'+str(questKeys[key])+'"')

for key in ZoneID:
  QuestieClassicQuestCorrections = QuestieClassicQuestCorrections.replace("zoneIDs."+str(key), str(ZoneID[key]))
  QuestieTBCQuestCorrections = QuestieTBCQuestCorrections.replace("zoneIDs."+str(key), str(ZoneID[key]))

for key in raceKeys:
  QuestieClassicQuestCorrections = QuestieClassicQuestCorrections.replace("raceIDs."+str(key), str(raceKeys[key]))
  QuestieTBCQuestCorrections = QuestieTBCQuestCorrections.replace("raceIDs."+str(key), str(raceKeys[key]))

ClassicData = lua.decode(QuestieClassicQuestCorrections)
TBCData = lua.decode(QuestieTBCQuestCorrections)

def postProcessData(data):
  #Add only the ones that does not already exist
  for id in data:
    if id not in QuestCorrections:
      QuestCorrections[id] = {}

    #if id == 9711:
    #  print("++")

    questData = data[id]
    #ObjectivesText
    if "ObjectivesTextFIX" in questData:
      objectivesText = questData["ObjectivesTextFIX"]
      if len(objectivesText) > 0:
        data[id]["Objectives"] = " ".join(objectivesText)
      else:
        data[id]["Objectives"] = None
      del(data[id]["ObjectivesTextFIX"])

    #Objectives
    if "objectivesFIX" in questData:
      objectives = questData["objectivesFIX"]
      if len(objectives) > 0 and objectives[0] == None:
        data[id]["ReqCreatureId"] = None
      elif len(objectives) > 0:
        skip = False
        setData = []
        for npc in objectives[0]:
          #Sometimes it loops through the list, sometimes it values in the list...
          use = npc
          if(type(npc) == int):
            use = objectives[0]
          if(use[0] < 40000): #Questie Fake corrections
            if len(use) > 1 and use[1] != None and use[1] != '':
              setData.append([use[0], use[1]])
            else:
              setData.append([use[0]])
          else:
            print("Skipping Correction for id: "+str(id)+ "  Skipped ID:"+str(use[0]))
            skip = True
          #Sometimes it loops through the list, sometimes it values in the list... break
          if(type(npc) == int):
            break
        if not skip:
          data[id]["ReqCreatureId"] = setData

      if len(objectives) > 1 and objectives[1] == None:
        data[id]["ReqGOId"] = None
      elif len(objectives) > 1:
        skip = False
        setData = []
        for object in objectives[1]:
          if(object[0] < 40000): #Questie Fake corrections
            setData.append([object[0], object[1]])
          else:
            print("Skipping Correction for id: "+str(id)+ "  Skipped ID:"+str(object[0]))
            skip = True
        if not skip:
          data[id]["ReqGOId"] = setData

      if len(objectives) > 2 and objectives[2] == None:
        data[id]["ReqItemId"] = None
      elif len(objectives) > 2:
        skip = False
        setData = []
        for item in objectives[2]:
          if(item[0] < 40000): #Questie Fake corrections
            setData.append(item[0])
          else:
            print("Skipping Correction for id: "+str(id)+ "  Skipped ID:"+str(item[0]))
            skip = True
        if not skip:
          data[id]["ReqItemId"] = setData

      #This will never be used to the nature of the objective
      if len(objectives) > 3 and objectives[3] == None:
        data[id]["RepObjectiveFaction"] = None
      #elif len(objectives) > 3:
      #  print("3")
      del(data[id]["objectivesFIX"])

    #Reputation
    if "RequiredMinRepFactionFIX" in questData:
      minReputation = questData["RequiredMinRepFactionFIX"]
      if(len(minReputation) > 0):
        data[id]["RequiredMinRepFaction"] = minReputation[0]
        data[id]["RequiredMinRepValue"] = minReputation[1]
      del(data[id]["RequiredMinRepFactionFIX"])
    if "RequiredMaxRepFactionFIX" in questData:
      maxReputation = questData["RequiredMaxRepFactionFIX"]
      if(len(maxReputation) > 0):
        data[id]["RequiredMaxRepFaction"] = maxReputation[0]
        data[id]["RequiredMaxRepValue"] = maxReputation[1]
      del(data[id]["RequiredMaxRepFactionFIX"])

    if "RequiredSkillFIX" in questData:
      requiredSkill = questData["RequiredSkillFIX"]
      if(len(requiredSkill) > 0):
        data[id]["RequiredSkill"] = requiredSkill[0]
        data[id]["RequiredSkillValue"] = requiredSkill[1]
      del(data[id]["RequiredSkillFIX"])

    #Start
    if "startedByFIX" in questData:
      startedBy = questData["startedByFIX"]
      if len(startedBy) > 0 and startedBy[0] == None:
        data[id]["creatureStart"] = None
      elif len(startedBy) > 0:
        #data[id]["creatureStart"] = startedBy[0]
        repl = [[number] for number in startedBy[0] if number < 40000]
        if len(repl) > 0:
          data[id]["creatureStart"] = repl

      if len(startedBy) > 1 and startedBy[1] == None:
        data[id]["goStart"] = None
      elif len(startedBy) > 1:
        #data[id]["goStart"] = startedBy[1]
        repl = [[number] for number in startedBy[1] if number < 40000]
        if len(repl) > 0:
          data[id]["goStart"] = repl

      if len(startedBy) > 2 and startedBy[2] == None:
        data[id]["itemStart"] = None
      elif len(startedBy) > 2:
        #data[id]["itemStart"] = startedBy[2]
        repl = [[number] for number in startedBy[2] if number < 40000]
        if len(repl) > 0:
          data[id]["itemStart"] = repl
      del(data[id]["startedByFIX"])

    #End
    if "finishedByFIX" in questData:
      finishedBy = questData["finishedByFIX"]
      if len(finishedBy) > 0 and finishedBy[0] == None:
        data[id]["creatureEnd"] = None
      elif len(finishedBy) > 0:
        #data[id]["creatureEnd"] = finishedBy[0]
        repl = [[number] for number in finishedBy[0] if number < 40000]
        if len(repl) > 0:
          data[id]["creatureEnd"] = repl

      if len(finishedBy) > 1 and finishedBy[1] == None:
        data[id]["goEnd"] = None
      elif len(finishedBy) > 1:
        #data[id]["goEnd"] = finishedBy[1]
        repl = [[number] for number in finishedBy[1] if number < 40000]
        if len(repl) > 0:
          data[id]["goEnd"] = repl
      del(data[id]["finishedByFIX"])

    if "ReqSourceId" in questData:
        repl = [number for number in questData["ReqSourceId"] if number < 40000]
        data[id]["ReqSourceId"] = repl

    if "triggerEnd" in questData:
      repl = []
      repl.append(questData["triggerEnd"])
      data[id]["triggerEnd"] = repl

    QuestCorrections[id] = dict(list(data[id].items()) + list(QuestCorrections[id].items()))
    #debugTestVar = QuestCorrections[id]
    #debugTestVar = QuestCorrections[id]
      

postProcessData(ClassicData)
postProcessData(TBCData)

print("QuestCorrections Loaded")