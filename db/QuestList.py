from db.Quest import *
from db.Utilities import *

import re
import os.path
import pickle


class QuestList():
    """Holds a list of Quest() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, cursor, dictCursor, version, recache=False):
        self.version = version
        if (not os.path.isfile(f'data/{version}/quests.pkl') or recache):
            print('Caching quests...')
            self.cacheQuests(cursor, dictCursor)
        else:
            try:
                with open(f'data/{version}/quests.pkl', 'rb') as f:
                    self.qList = pickle.load(f)
                print('Using cached quests.')
            except:
                print('ERROR: Something went wrong while loading cached quests. Re-caching.')
                self.cacheQuests(cursor, dictCursor)

    def cacheQuests(self, cursor, dictCursor):
        self.qList = {}
        self.dictCursor = dictCursor
        dicts = self.__getQuestTables(cursor, dictCursor)
        infile = open(f'data/{self.version}/AreaTrigger.dbc.CSV', 'r')
        a = infile.read()
        infile.close()
        b = re.findall("(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),?\n", a)
        areaTrigger = []
        for x in b:
            areaTrigger.append((int(x[0]), int(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5]), float(x[6]), float(x[7]), float(x[8]), float(x[9])))
        count = len(dicts['quest_template'])
        print(f'Caching {count} quests...')
        for quest in dicts['quest_template']:
            self.__addQuest(quest, dicts, areaTrigger, cursor)
            if ((count % 500) == 0):
                print(str(count)+"...")
            count -= 1
        print("Done.")
        print("Sort quest chain information...")
        excluded = self.checkStartEnd() # quests that have no start or end point
        for questId in self.qList:
            quest = self.qList[questId]
            if quest in excluded:
                continue
            if hasattr(quest, "ExclusiveGroup"):
                group = self.allQuests(ExclusiveGroup = quest.ExclusiveGroup)
                for q in group:
                    if q in excluded:
                        group.remove(q)
                if quest.ExclusiveGroup > 0:
                    for q in group:
                        if q.id != quest.id:
                            quest.addExclusive(q.id)
                else: # quest.ExclusiveGroup < 0
                    for q in group:
                        if q.id != quest.id:
                            quest.addGroup(q.id)
        for questId in self.qList:
            quest = self.qList[questId]
            if quest.ExclusiveTo == []:
                delattr(quest, "ExclusiveTo")
            if quest.InGroupWith == []:
                delattr(quest, "InGroupWith")
        for questId in self.qList:
            quest = self.qList[questId]
            if quest in excluded:
                continue
            if hasattr(quest, "PrevQuestId"):
                if quest.PrevQuestId > 0:
                    # this should be the proper way to do it according to wiki, but due to the core handeling it differently the following fragment is deactivated
                    # left here in case I want to debug the core/db later
                    """
                    if hasattr(self.qList[quest.PrevQuestId], "InGroupWith"):
                        quest.addPreGroup(quest.PrevQuestId)
                    else: # has either ExclusiveTo or no ExclusiveGroup
                        quest.addPreSingle(quest.PrevQuestId)
                    """
                    # replacement for how core works atm.:
                    quest.addPreSingle(quest.PrevQuestId)
                else: # quest.PrevQuestId < 0
                    self.qList[abs(quest.PrevQuestId)].addChild(questId)
                    self.qList[questId].setParent(abs(quest.PrevQuestId))
            if hasattr(quest, "NextQuestId"):
                if quest.NextQuestId > 0:
                    postQuest = self.qList[quest.NextQuestId]
                    if hasattr(quest, "InGroupWith"):
                        postQuest.addPreGroup(questId)
                        for questId2 in quest.InGroupWith:
                            postQuest.addPreGroup(questId2)
                    else:
                        postQuest.addPreSingle(questId)
                else: # quest.NextQuestId < 0
                    quest.addChild(abs(quest.NextQuestId))
        for questId in self.qList:
            quest = self.qList[questId]
            if quest.PreQuestSingle == []:
                delattr(quest, "PreQuestSingle")
            if quest.PreQuestGroup == []:
                delattr(quest, "PreQuestGroup")
            if quest.ChildQuests == []:
                delattr(quest, "ChildQuests")
        with open(f'data/{self.version}/quests.pkl', 'wb') as f:
            pickle.dump(self.qList, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Done caching quests.")

    def unpackBitMask(self, bitMask):
        bits = []
        numBits=1
        while(pow(2, numBits) < bitMask):
            numBits += 1
        for x in range(-numBits, 1):
            potency = 1 << -x #pow(2, -x)
            if (bitMask >= potency):
                bitMask = bitMask - potency
                #s = "Flag on bit " + str(-x) + " is set (value " + str(potency) +")"
                #print (s)
                bits.insert(0, -x)
        return bits

    def __addQuest(self, quest, tables, areaTrigger, cursor):
        """only used by constructor"""
        newQuest = Quest(quest, tables, areaTrigger, cursor, self.version)
        self.qList[newQuest.id] = newQuest

    def findQuest(self, **kwargs):
        """find one quest by keyword = value, ..."""
        return next(self.__iterQuest(**kwargs))

    def allQuests(self, **kwargs):
        """find all quests by keyword = value, ..."""
        return list(self.__iterQuest(**kwargs))

    def allQuestsWith(self, *args):
        """find all quests by keyword, ..."""
        return list(self.__iterQuestWith(*args))

    def __iterQuestWith(self, *args):
        return (self.qList[quest] for quest in self.qList if hasattr(self.qList[quest], *args))

    def __iterQuest(self, **kwargs):
        return (self.qList[quest] for quest in self.qList if self.qList[quest].match(**kwargs))

    def __getQuestTables(self, cursor, dictCursor):
        """only used by constructor"""
        print("Selecting quest related MySQL tables...")
        # SrcItemId needed to check for spell_script_target (type and targetEntry) via item_template.spellId
        cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort, Method, ObjectiveText1, ObjectiveText2, ObjectiveText3, ObjectiveText4, EndText, Details, SpecialFlags FROM quest_template")
        quest_template = []
        for a in cursor.fetchall():
            quest_template.append(a)
        cursor.execute("SELECT id, quest FROM creature_involvedrelation")
        creature_involvedrelation = []
        for a in cursor.fetchall():
            creature_involvedrelation.append(a)
        cursor.execute("SELECT id, quest FROM gameobject_involvedrelation")
        gameobject_involvedrelation = []
        for a in cursor.fetchall():
            gameobject_involvedrelation.append(a)
        cursor.execute("SELECT id, quest FROM creature_questrelation")
        creature_questrelation = []
        for a in cursor.fetchall():
            creature_questrelation.append(a)
        cursor.execute("SELECT id, quest FROM gameobject_questrelation")
        gameobject_questrelation = []
        for a in cursor.fetchall():
            gameobject_questrelation.append(a)
        cursor.execute("SELECT entry, startquest FROM item_template")
        item_questrelation = []
        for a in cursor.fetchall():
            item_questrelation.append(a)
        cursor.execute("SELECT id, quest FROM areatrigger_involvedrelation")
        areatrigger_involvedrelation = []
        for a in cursor.fetchall():
            areatrigger_involvedrelation.append(a)
        count = dictCursor.execute("SELECT * FROM locales_quest")
        loc_quests = {}
        for _ in range(0, count):
            q = dictCursor.fetchone()
            loc_quests[q['entry']] = q
        print("Done.")
        return {'quest_template':quest_template,
                'creature_involvedrelation':creature_involvedrelation,
                'gameobject_involvedrelation':gameobject_involvedrelation,
                'creature_questrelation':creature_questrelation,
                'gameobject_questrelation':gameobject_questrelation,
                'item_questrelation':item_questrelation,
                'areatrigger_involvedrelation':areatrigger_involvedrelation,
                'locales_quest':loc_quests}

    def checkStartEnd(self):
        """Find quests with missing start or end points.
        Returns a list of all quest objects in qList missing either.
        """
        cs = self.allQuestsWith('creatureStart')
        gs = self.allQuestsWith('goStart')
        its = self.allQuestsWith('itemStart')
        xs = []
        for q in self.qList:
            if (self.qList[q] not in cs) and (self.qList[q] not in gs) and (self.qList[q] not in its):
                xs.append(self.qList[q])
        ge = self.allQuestsWith('goEnd')
        ce = self.allQuestsWith('creatureEnd')
        xe = []
        for q in self.qList:
            if (self.qList[q] not in ce) and (self.qList[q] not in ge):
                xe.append(self.qList[q])
        xx = []
        for q in xs:
            if (q in xe):
                xx.append(q)
        noS = []
        for q in xs:
            if (q not in xe):
                noS.append(q)
        noE = []
        for q in xe:
            if (q not in xs):
                noE.append(q)
        for q in noE:
            xx.append(q)
        for q in noS:
            xx.append(q)
        return xx

    def checkRequiredRaces(self, npcs):
        actualRequiredRaces = {}
        for quest in self.qList:
            tempRace = 0
            if hasattr(self.qList[quest], "creatureStart"):
                for creature in self.qList[quest].creatureStart:
                    if ((self.qList[quest].RequiredRaces & 77) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (77,178)) and npcs.nList[creature].hostileToA:
                        tempRace = tempRace | 178
                    if ((self.qList[quest].RequiredRaces & 178) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (77,178)) and npcs.nList[creature].hostileToH:
                        tempRace = tempRace | 77
            if hasattr(self.qList[quest], "creatureEnd"):
                for creature in self.qList[quest].creatureEnd:
                    if ((self.qList[quest].RequiredRaces & 77) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (77,178)) and npcs.nList[creature].hostileToA:
                        tempRace = tempRace | 178
                    if ((self.qList[quest].RequiredRaces & 178) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (77,178)) and npcs.nList[creature].hostileToH:
                        tempRace = tempRace | 77
            if tempRace not in (0,255):
                actualRequiredRaces[self.qList[quest].id] = tempRace
        return actualRequiredRaces

    def printQuestFile(self, file="output/questDB.lua", locale="enGB"):
        outfile = open(file, "w")
        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

---@type QuestieDB
local QuestieDB = QuestieLoader:ImportModule("QuestieDB");

local isTBCClient = string.byte(GetBuildInfo(), 1) == 50;

if (not isTBCClient) then
    return
end

QuestieDB.questKeys = {
    ['name'] = 1, -- string
    ['startedBy'] = 2, -- table
        --['creatureStart'] = 1, -- table {creature(int),...}
        --['objectStart'] = 2, -- table {object(int),...}
        --['itemStart'] = 3, -- table {item(int),...}
    ['finishedBy'] = 3, -- table
        --['creatureEnd'] = 1, -- table {creature(int),...}
        --['objectEnd'] = 2, -- table {object(int),...}
    ['requiredLevel'] = 4, -- int
    ['questLevel'] = 5, -- int
    ['requiredRaces'] = 6, -- bitmask
    ['requiredClasses'] = 7, -- bitmask
    ['objectivesText'] = 8, -- table: {string,...}, Description of the quest. Auto-complete if nil.
    ['triggerEnd'] = 9, -- table: {text, {[zoneID] = {coordPair,...},...}}
    ['objectives'] = 10, -- table
        --['creatureObjective'] = 1, -- table {{creature(int), text(string)},...}, If text is nil the default "<Name> slain x/y" is used
        --['objectObjective'] = 2, -- table {{object(int), text(string)},...}
        --['itemObjective'] = 3, -- table {{item(int), text(string)},...}
        --['reputationObjective'] = 4, -- table: {faction(int), value(int)}
        --['killCreditObjective'] = 5, -- table: {{creature(int), ...}, baseCreatureID, baseCreatureText}
    ['sourceItemId'] = 11, -- int, item provided by quest starter
    ['preQuestGroup'] = 12, -- table: {quest(int)}
    ['preQuestSingle'] = 13, -- table: {quest(int)}
    ['childQuests'] = 14, -- table: {quest(int)}
    ['inGroupWith'] = 15, -- table: {quest(int)}
    ['exclusiveTo'] = 16, -- table: {quest(int)}
    ['zoneOrSort'] = 17, -- int, >0: AreaTable.dbc ID; <0: QuestSort.dbc ID
    ['requiredSkill'] = 18, -- table: {skill(int), value(int)}
    ['requiredMinRep'] = 19, -- table: {faction(int), value(int)}
    ['requiredMaxRep'] = 20, -- table: {faction(int), value(int)}
    ['requiredSourceItems'] = 21, -- table: {item(int), ...} Items that are not an objective but still needed for the quest.
    ['nextQuestInChain'] = 22, -- int: if this quest is active/finished, the current quest is not available anymore
    ['questFlags'] = 23, -- bitmask: see https://github.com/cmangos/issues/wiki/Quest_template#questflags
    ['specialFlags'] = 24, -- bitmask: 1 = Repeatable, 2 = Needs event, 4 = Monthly reset (req. 1). See https://github.com/cmangos/issues/wiki/Quest_template#specialflags
    ['parentQuest'] = 25, -- int, the ID of the parent quest that needs to be active for the current one to be available. See also 'childQuests' (field 14)
    ['extraObjectives'] = 26, -- table: {{spawnlist, iconFile, text},...}, a list of hidden special objectives for a quest. Similar to requiredSourceItems
}

QuestieDB.questData = [[return {
""")
        #excluded = self.checkStartEnd()
        for id in sorted(self.qList):
            quest = self.qList[id]
            #if quest in excluded:
            #    continue
            outfile.write("["+str(quest.id)+"] = {") #key
            title = quest.Title
            if locale != 'enGB' and quest.locales_Title[localesMap[locale]] != None:
                title = escapeDoubleQuotes(quest.locales_Title[localesMap[locale]])
            outfile.write("\""+title+"\",") #name = 1
            outfile.write("{") #starts = 2
            if (hasattr(quest, "creatureStart")):
                outfile.write("{") #npc = starts1
                for npc in quest.creatureStart:
                    outfile.write(str(npc)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "goStart")):
                outfile.write("{") #obj = starts2
                for obj in quest.goStart:
                    outfile.write(str(obj)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "itemStart")):
                outfile.write("{") #itm = starts3
                for itm in quest.itemStart:
                    outfile.write(str(itm)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            outfile.write("},")
            outfile.write("{") #ends = 3
            if (hasattr(quest, "creatureEnd")): #npc = ends1
                outfile.write("{")
                for npc in quest.creatureEnd:
                    outfile.write(str(npc)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "goEnd")): #obj = ends2
                outfile.write("{")
                for obj in quest.goEnd:
                    outfile.write(str(obj)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            outfile.write("},")
            outfile.write(str(quest.MinLevel)+",") #minLevel = 4
            outfile.write(str(quest.QuestLevel)+",") #level = 5
            outfile.write(f'{quest.RequiredRaces},') #RequiredRaces = 6
            if (hasattr(quest, "RequiredClasses")): #RequiredClasses = 7
                outfile.write(f"{quest.RequiredClasses},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "Objectives")): # and (len(self.allQuests(Title = quest.Title)) > 1): #objectives = 8
                objectives = self.questieObjectivesText(quest.Objectives)
                if locale != 'enGB' and quest.locales_Title[localesMap[locale]] != None:
                    objectives = self.questieObjectivesText(quest.locales_Title[localesMap[locale]])
                outfile.write('{')
                for line in objectives:
                    outfile.write(f'"{line}",')
                outfile.write('},')
            else:
                outfile.write("nil,")
            if (hasattr(quest, "triggerEnd")): #trigger = 9
                outfile.write("{\""+quest.triggerEnd[0]+"\",{")
                for zone in quest.triggerEnd[1].cByZone:
                    if zone not in validZoneList:
                        continue
                    outfile.write("["+str(zone)+"]={")
                    for c in quest.triggerEnd[1].cByZone[zone]:
                        outfile.write("{"+str(c[0])+","+str(c[1])+"},")
                    outfile.write("},")
                outfile.write("}},")
            else:
                outfile.write("nil,")
            outfile.write("{") #objectives = 10
            if (hasattr(quest, "ReqCreatureId")): #npc = objectives1
                outfile.write("{")
                for npc in quest.ReqCreatureId:
                    outfile.write("{"+str(npc[0]))
                    if npc[1] and (npc[1] != ''):
                        outfile.write(",\""+npc[1]+"\"},")
                    else:
                        outfile.write(",nil},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ReqGOId")): #obj = objectives2
                outfile.write("{")
                for obj in quest.ReqGOId:
                    outfile.write("{"+str(abs(obj[0]))+",\""+str(obj[1])+"\"},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ReqItemId")): #itm = objectives3
                outfile.write("{")
                if (hasattr(quest, "ReqItemId")):
                    for itm in quest.ReqItemId:
                        outfile.write("{"+str(itm)+",nil},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "RepObjectiveFaction")): #rep = objectives4
                outfile.write("{"+str(quest.RepObjectiveFaction)+","+str(quest.RepObjectiveValue)+"},")
            else:
                outfile.write("nil,")

            if (hasattr(quest, "killCreditData")): #multi-creatureID = objectives5
                outfile.write("{{")
                for kills in quest.killCreditData[0]:
                    outfile.write(str(kills)+",")
                outfile.write(str(quest.killCreditData[1][0])+",")
                if len(quest.killCreditData[1][1]) > 0:
                    outfile.write("},"+str(quest.killCreditData[1][0]) + ","+"\""+quest.killCreditData[1][1]+"\"},")
                else:
                    outfile.write("},"+str(quest.killCreditData[1][0]) + "},")

            outfile.write("},")
            if (hasattr(quest, "SrcItemId")): #SrcItemId = 11
                outfile.write(str(quest.SrcItemId)+",")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "PreQuestGroup")): # 12
                outfile.write("{")
                for questId in quest.PreQuestGroup:
                    outfile.write(str(questId)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "PreQuestSingle")): # 13
                outfile.write("{")
                for questId in quest.PreQuestSingle:
                    outfile.write(str(questId)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ChildQuests")): # 14
                outfile.write("{")
                for questId in quest.ChildQuests:
                    outfile.write(str(questId)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "InGroupWith")): # 15
                outfile.write("{")
                for questId in quest.InGroupWith:
                    outfile.write(str(questId)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ExclusiveTo")): # 16
                outfile.write("{")
                for questId in quest.ExclusiveTo:
                    outfile.write(str(questId)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ZoneOrSort")): #17
                outfile.write(str(quest.ZoneOrSort)+",")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "RequiredSkill")): #18
                outfile.write("{"+str(quest.RequiredSkill)+","+str(quest.RequiredSkillValue)+"},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "RequiredMinRepFaction")): #19
                outfile.write("{"+str(quest.RequiredMinRepFaction)+","+str(quest.RequiredMinRepValue)+"},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "RequiredMaxRepFaction")): #20
                outfile.write("{"+str(quest.RequiredMaxRepFaction)+","+str(quest.RequiredMaxRepValue)+"},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, 'ReqSourceId')): #21
                outfile.write('{')
                done = []
                for itm in quest.ReqSourceId:
                    if itm in done:
                        continue
                    outfile.write(f'{itm},')
                    done.append(itm)
                outfile.write('},')
            else:
                outfile.write('nil,')
            if (hasattr(quest, 'NextQuestInChain')): #22
                outfile.write(f'{quest.NextQuestInChain},')
            else:
                outfile.write('nil,')
            if (hasattr(quest, 'QuestFlags')): # 23
                outfile.write(f'{quest.QuestFlags},')
            else:
                outfile.write('nil,')
            if (hasattr(quest, 'SpecialFlags')): # 24
                outfile.write(f'{quest.SpecialFlags},')
            else:
                outfile.write('nil,')
            if (hasattr(quest, 'ParentQuest')): # 25
                outfile.write(f'{quest.ParentQuest},')
            else:
                outfile.write('nil,')
            outfile.write("},\n")
        outfile.write("}]]\n")
        outfile.close();

    def pfQuestFile(self, file='quests.lua', locale='enGB'):
        outfile = open(file, 'w')
        outfile.write('pfDB["quests"]["'+locale+'"] = {\n')
        excluded = self.checkStartEnd()
        for id in sorted(self.qList):
            quest = self.qList[id]
            if quest in excluded:
                continue
            outfile.write('[\"'+str(quest.id)+'\"] = {\n') #key
            title = quest.Title
            if locale != 'enGB' and quest.locales_Title[localesMap[locale]] != None:
                title = escapeDoubleQuotes(quest.locales_Title[localesMap[locale]])
            outfile.write('\tid = {},\n'.format(quest.id)) #id = 0
            outfile.write('\ttitle = "{}",\n'.format(title)) #name = 1
            outfile.write('\t["start"] = {\n') #starts = 2
            if (hasattr(quest, 'creatureStart')):
                outfile.write('\t\t["NPC"] = {\n') #npc = starts1
                for npc in quest.creatureStart:
                    outfile.write('\t\t\t{},\n'.format(npc))
                outfile.write('\t\t},\n')
            if (hasattr(quest, 'goStart')):
                outfile.write('\t\t["OBJECT"] = {\n') #obj = starts2
                for obj in quest.goStart:
                    outfile.write('\t\t\t{},\n'.format(obj))
                outfile.write('\t\t},\n')
            if (hasattr(quest, 'itemStart')):
                outfile.write('\t\t["ITEM"] = {\n') #itm = starts3
                for itm in quest.itemStart:
                    outfile.write('\t\t\t{},\n'.format(itm))
                outfile.write('\t\t},\n')
            outfile.write('\t},\n')
            outfile.write('\t["end"] = {\n') #ends = 3
            if (hasattr(quest, 'creatureEnd')): #npc = ends1
                outfile.write('\t\t["NPC"] = {\n')
                for npc in quest.creatureEnd:
                    outfile.write('\t\t\t{},\n'.format(npc))
                outfile.write('\t\t},\n')
            if (hasattr(quest, 'goEnd')): #obj = ends2
                outfile.write('\t\t["OBJECT"] = {\n')
                for obj in quest.goEnd:
                    outfile.write('\t\t\t{},\n'.format(obj))
                outfile.write('\t\t},\n')
            outfile.write('\t},\n')
            outfile.write('\t["min"] = {},\n'.format(quest.MinLevel)) #minLevel = 4
            outfile.write('\t["lvl"] = {},\n'.format(quest.QuestLevel)) #level = 5
            outfile.write('\t["race"] = {},\n'.format(quest.RequiredRaces)) #RequiredRaces = 6
            if (hasattr(quest, 'RequiredClasses')): #RequiredClasses = 7
                outfile.write('\t["min"] = {},\n'.format(quest.RequiredClasses))
            if (hasattr(quest, 'Objectives')): #objectives = 8
                if quest.id == 4641:
                    quest.Objectives = quest.Objectives[0:-5]
                objectives = quest.Objectives
                if locale != 'enGB' and quest.locales_Title[localesMap[locale]] != None:
                    objectives = quest.locales_Title[localesMap[locale]]
                outfile.write('\t["obj"] = "{}",\n'.format(objectives))
            if (hasattr(quest, 'Details')):
                details = quest.Details
                if locale != 'enGB' and hasattr(quest, 'locales_Details') and localesMap[locale] in quest.locales_Details and quest.locales_Details[localesMap[locale]] != None:
                    details = quest.locales_Details[localesMap[locale]]
                outfile.write('\t["log"] = "{}",\n'.format(details))
            if (hasattr(quest, 'triggerEnd')): #trigger = 9
                outfile.write('\t["trigger"] = {\n')
                outfile.write('\t\t"{}",\n'.format(quest.triggerEnd[0]))
                outfile.write('\t\t{\n')
                for tri in quest.triggerEnd[1].cByZone:
                    outfile.write('\t\t\t['+str(tri)+'] = {\n')
                    for c in quest.triggerEnd[1].cByZone[tri]:
                        outfile.write('\t\t\t\t{'+str(c[0])+','+str(c[1])+'},\n')
                    outfile.write('\t\t\t},\n')
                outfile.write('\t\t},\n\t},\n')
            outfile.write('\t["targets"] = {\n') #ReqCreatureOrGOOrItm = 10
            if (hasattr(quest, 'ReqCreatureId')): #npc = ReqCreatureOrGOOrItm1
                outfile.write('\t\t["NPC"] = {\n')
                for npc in quest.ReqCreatureId:
                    outfile.write('\t\t\t{["id"]='+str(npc[0]))
                    if (npc[1] != ''):
                        text = npc[1]
                        if locale != 'enGB' and localesMap[locale] in npc[2]:
                            text = npc[2][localesMap[locale]]
                        outfile.write(',["text"]="'+text+'"},\n')
                    else:
                        outfile.write('},\n')
                outfile.write('\t\t},\n')
            if (hasattr(quest, 'ReqGOId')): #obj = ReqCreatureOrGOOrItm2
                outfile.write('\t\t["OBJECT"] = {\n')
                for obj in quest.ReqGOId:
                    outfile.write('\t\t\t{["id"]='+str(abs(obj[0])))
                    if (obj[1] != ''):
                        text = obj[1]
                        if locale != 'enGB' and localesMap[locale] in obj[2]:
                            text = obj[2][localesMap[locale]]
                        outfile.write(',["text"]="'+text+'"},\n')
                    else:
                        outfile.write('},\n')
                outfile.write('\t\t},\n')
            if (hasattr(quest, 'ReqSourceId')) or (hasattr(quest, 'ReqItemId')): #itm = ReqCreatureOrGOOrItm3
                outfile.write('\t\t["ITEM"] = {\n')
                if (hasattr(quest, 'ReqSourceId')):
                    done = []
                    for itm in quest.ReqSourceId:
                        if itm in done:
                            continue
                        outfile.write('\t\t\t{["id"]='+str(itm)+'},\n')
                        done.append(itm)
                if (hasattr(quest, 'ReqItemId')):
                    for itm in quest.ReqItemId:
                        outfile.write('\t\t\t{["id"]='+str(itm)+'},\n')
                outfile.write('\t\t},\n')
            outfile.write('\t},\n')
            if (hasattr(quest, 'SrcItemId')): #SrcItemId = 11
                outfile.write('\t["providedItem"] = {},\n'.format(quest.SrcItemId))
            if (hasattr(quest, 'PreQuestGroup')): # 12
                outfile.write('\t["preQuestGroup"] = {\n')
                for questId in quest.PreQuestGroup:
                    outfile.write('\t\t{},\n'.format(questId))
                outfile.write('\t},\n')
            if (hasattr(quest, 'PreQuestSingle')): # 13
                outfile.write('\t["preQuestSingle"] = {\n')
                for questId in quest.PreQuestSingle:
                    outfile.write('\t\t{},\n'.format(questId))
                outfile.write('\t},\n')
            if (hasattr(quest, 'ChildQuests')): # 14
                outfile.write('\t["childQuests"] = {\n')
                for questId in quest.ChildQuests:
                    outfile.write('\t\t{},\n'.format(questId))
                outfile.write('\t},\n')
            if (hasattr(quest, 'InGroupWith')): # 15
                outfile.write('\t["inGroupWith"] = {\n')
                for questId in quest.InGroupWith:
                    outfile.write('\t\t{},\n'.format(questId))
                outfile.write('\t},\n')
            if (hasattr(quest, 'ExclusiveTo')): # 16
                outfile.write('\t["exclusiveTo"] = {\n')
                for questId in quest.ExclusiveTo:
                    outfile.write('\t\t{},\n'.format(questId))
                outfile.write('\t},\n')
            outfile.write('},\n')
        outfile.write('}; -- End of pfDB["quests"]["'+locale+'"]\n')
        outfile.close();

    def printQuestieAddendum(self, file='addendum.lua'):
        questSort = {}
        excluded = self.checkStartEnd()
        print("Sorting quests by title...")
        for id in sorted(self.qList):
            quest = self.qList[id]
            if quest in excluded:
                continue
            if quest.Title in questSort:
                questSort[quest.Title].append(quest.id)
            else:
                questSort[quest.Title] = [quest.id]
        print("Done.")
        print("Printing file "+file)
        outfile = open(file, "w")

        outfile.write("local N = UnitName(\"player\");\nlocal R = UnitRace(\"player\");\nQuestieLevLookup = {\n")

        for title in questSort:
            outfile.write(" [\"")
            outfile.write(title)
            outfile.write("\"]={\n")
            for id in questSort[title]:
                quest = self.qList[id]
                outfile.write("  [\"")
                if (hasattr(quest, "Objectives")):
                    if quest.id == 4641:
                        quest.Objectives = quest.Objectives[0:-5]
                    outfile.write(quest.Objectives)
                outfile.write("\"]={")
                outfile.write(str(quest.RequiredRaces))
                outfile.write(",")
                outfile.write(str(id))
                outfile.write("},\n")
            outfile.write(" },\n")

        """
        outfile.write("}\n\nQuestieHashMap = {\n")
        for id in sorted(self.qList):
            quest = self.qList[id]
            if quest in excluded:
                continue
            outfile.write(" [")
            outfile.write(str(id))
            outfile.write("]={\n")
        print("Done.")
        """

    def getFactionString(self, requiredRaces):
        if requiredRaces == 0:
            return "AH"
        faction = ""
        if requiredRaces & 77:
            faction += "A"
        if requiredRaces & 178:
            faction += "H"
        return faction

    def questieObjectivesText(self, objectives, cutName=True):
        split = objectives.split('\\n')
        target = []
        for s in split:
            if (s != '') and not (('$n' in s) and cutName):
                target.append(s)
        target2 = []
        for s in target:
            if '  ' in s:
                split2 = s.split('  ')
                for x in split2:
                    target2.append(x)
            else:
                target2.append(s)
        return target2

    def lineWrap(self, source):
        target = []
        temp = source
        while(len(temp)>80):
            cutoff = 80
            while(temp[cutoff] != ' '):
                cutoff -= 1
            target.append(temp[:cutoff])
            temp = temp[cutoff+1:]
        target.append(temp)
        return target
