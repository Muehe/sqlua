from db.Quest import *
from db.Utilities import *

import re
import os.path
import pickle


class QuestList:
    """Holds a list of Quest() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, version):
        self.version = version
        self.qList = {}
        self.raceIDs = {
            'NONE': 0,
            'HUMAN': 1,
            'ORC': 2,
            'DWARF': 4,
            'NIGHT_ELF': 8,
            'UNDEAD': 16,
            'TAUREN': 32,
            'GNOME': 64,
            'TROLL': 128,
            'GOBLIN': 256,
            'BLOOD_ELF': 512,
            'DRAENEI': 1024,
            'WORGEN': 2097152,
        }
        if version == 'classic':
            self.raceIDs['ALLIANCE'] = 77
            self.raceIDs['HORDE'] = 178
            self.raceIDs['ALL'] = 255
        if version == 'cata':
            self.raceIDs['ALLIANCE'] = 2098253
            self.raceIDs['HORDE'] = 946
            self.raceIDs['ALL'] = 2099199
        else:
            self.raceIDs['ALLIANCE'] = 1101
            self.raceIDs['HORDE'] = 690
            self.raceIDs['ALL'] = 1791

        self.skipList = {
            8731: {'cata'}, # Why the hell did I want to skip this? Some weird data in TrinityDB I think?
        }

    def run(self, cursor, dictCursor, db_flavor, recache=False):
        if not os.path.isfile(f'data/{self.version}/quests.pkl') or recache:
            dicts = self.__getQuestTables(cursor, dictCursor)
            print('Caching quests...')
            self.cacheQuests(dicts)
        else:
            try:
                with open(f'data/{self.version}/quests.pkl', 'rb') as f:
                    self.qList = pickle.load(f)
                print('Using cached quests.')
            except:
                print('ERROR: Something went wrong while loading cached quests. Re-caching.')
                dicts = self.__getQuestTables(cursor, dictCursor)
                self.cacheQuests(dicts)

    def validQuestName(self, name):
        for string in ['Deprecated', 'DEPRECATED', 'ZZOLD', 'zzOLD', 'zzold', '(REMOVED)', '<UNUSED>']:
            if string in name:
                return False
        return True

    def skipQuest(self, qid):
        if qid in self.skipList and self.version in self.skipList[qid]:
            return True
        return False

    def cacheQuests(self, dicts):
        # TODO: Use proper CSV reader
        infile = open(f'data/{self.version}/AreaTrigger.dbc.CSV', 'r')
        a = infile.read()
        infile.close()
        b = re.findall("(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),?\n", a)
        areaTrigger = []
        for x in b:
            areaTrigger.append((int(x[0]), int(x[1]), float(x[2]), float(x[3])))
        count = len(dicts['quest_template'])
        print(f'Caching {count} quests...')
        for quest in dicts['quest_template']:
            if not self.skipQuest(quest[0]):
                self.__addQuest(quest, dicts, areaTrigger)
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
            if hasattr(quest, "ExclusiveGroup") and quest.ExclusiveGroup is not None:
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
            if hasattr(quest, "BreadcrumbForQuestId") and quest.BreadcrumbForQuestId is not None and quest.BreadcrumbForQuestId in self.qList:
                self.qList[quest.BreadcrumbForQuestId].addBreadcrumb(quest.id)
        for questId in self.qList:
            quest = self.qList[questId]
            if quest.ExclusiveTo == []:
                delattr(quest, "ExclusiveTo")
            if quest.InGroupWith == []:
                delattr(quest, "InGroupWith")
            if quest.Breadcrumbs == []:
                delattr(quest, "Breadcrumbs")
        for questId in self.qList:
            quest = self.qList[questId]
            if quest in excluded:
                continue
            if hasattr(quest, "PrevQuestId") and quest.PrevQuestId is not None:
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
            if hasattr(quest, "NextQuestId") and quest.NextQuestId is not None:
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

    def __addQuest(self, quest, tables, areaTrigger):
        """only used by constructor"""
        newQuest = Quest(quest, tables, areaTrigger, self.version)
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
        print("  SELECT quest_template")
        if self.version == "wotlk":
            cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort, Method, ObjectiveText1, ObjectiveText2, ObjectiveText3, ObjectiveText4, EndText, Details, SpecialFlags, BreadCrumbForQuestId, RewRepFaction1, RewRepFaction2, RewRepFaction3, RewRepFaction4, RewRepFaction5, RewRepValue1, RewRepValue2, RewRepValue3, RewRepValue4, RewRepValue5, RewRepValueId1, RewRepValueId2, RewRepValueId3, RewRepValueId4, RewRepValueId5 FROM quest_template")
        else: # SrcItemId needed to check for spell_script_target (type and targetEntry) via item_template.spellId
            cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort, Method, ObjectiveText1, ObjectiveText2, ObjectiveText3, ObjectiveText4, EndText, Details, SpecialFlags, BreadCrumbForQuestId, RewRepFaction1, RewRepFaction2, RewRepFaction3, RewRepFaction4, RewRepFaction5, RewRepValue1, RewRepValue2, RewRepValue3, RewRepValue4, RewRepValue5 FROM quest_template")
        quest_template = []
        for a in cursor.fetchall():
            quest_template.append(a)

        print("  SELECT creature_template")
        cursor.execute("SELECT entry, KillCredit1, KillCredit2 FROM creature_template WHERE KillCredit1 != 0 OR KillCredit2 != 0")
        creature_killcredit = {}
        for a in cursor.fetchall():
            if a[1] != 0:
                if not (a[1] in creature_killcredit):
                    creature_killcredit[a[1]] = []
                creature_killcredit[a[1]].append(a[0])
            if a[2] != 0:
                if not (a[2] in creature_killcredit):
                    creature_killcredit[a[2]] = []
                creature_killcredit[a[2]].append(a[0])

        print("  SELECT creature_involvedrelation")
        cursor.execute("SELECT id, quest FROM creature_involvedrelation")
        creature_involvedrelation = {}
        for a in cursor.fetchall():
            if(a[1] in creature_involvedrelation):
                creature_involvedrelation[a[1]].append(a)
            else:
                creature_involvedrelation[a[1]] = []
                creature_involvedrelation[a[1]].append(a)

        print("  SELECT gameobject_involvedrelation")
        cursor.execute("SELECT id, quest FROM gameobject_involvedrelation")
        gameobject_involvedrelation = {}
        for a in cursor.fetchall():
            if(a[1] in gameobject_involvedrelation):
                gameobject_involvedrelation[a[1]].append(a)
            else:
                gameobject_involvedrelation[a[1]] = []
                gameobject_involvedrelation[a[1]].append(a)

        print("  SELECT creature_questrelation")
        cursor.execute("SELECT id, quest FROM creature_questrelation")
        creature_questrelation = {}
        for a in cursor.fetchall():
            if(a[1] in creature_questrelation):
                creature_questrelation[a[1]].append(a)
            else:
                creature_questrelation[a[1]] = []
                creature_questrelation[a[1]].append(a)

        print("  SELECT gameobject_questrelation")
        cursor.execute("SELECT id, quest FROM gameobject_questrelation")
        gameobject_questrelation = {}
        for a in cursor.fetchall():
            if(a[1] in gameobject_questrelation):
                gameobject_questrelation[a[1]].append(a)
            else:
                gameobject_questrelation[a[1]] = []
                gameobject_questrelation[a[1]].append(a)
                
        print("  SELECT item_template")
        cursor.execute("SELECT entry, startquest FROM item_template")
        item_questrelation = {}
        for a in cursor.fetchall():
            if(a[1] in item_questrelation):
                item_questrelation[a[1]].append(a)
            else:
                item_questrelation[a[1]] = []
                item_questrelation[a[1]].append(a)

        print("  SELECT areatrigger_involvedrelation")
        cursor.execute("SELECT id, quest FROM areatrigger_involvedrelation")
        areatrigger_involvedrelation = {}
        for a in cursor.fetchall():
            if(a[1] in areatrigger_involvedrelation):
                areatrigger_involvedrelation[a[1]].append(a)
            else:
                areatrigger_involvedrelation[a[1]] = []
                areatrigger_involvedrelation[a[1]].append(a)

        print("  SELECT locales_quest")
        count = dictCursor.execute("SELECT * FROM locales_quest")
        loc_quests = {}
        for _ in range(0, count):
            q = dictCursor.fetchone()
            loc_quests[q['entry']] = q
        print("Done.")
        return {'quest_template':quest_template,
                'creature_killcredit': creature_killcredit,
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
                    if ((self.qList[quest].RequiredRaces & self.raceIDs['ALLIANCE']) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (self.raceIDs['ALLIANCE'],self.raceIDs['HORDE'])) and npcs.nList[creature].hostileToA:
                        tempRace = tempRace | self.raceIDs['HORDE']
                    if ((self.qList[quest].RequiredRaces & self.raceIDs['HORDE']) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (self.raceIDs['ALLIANCE'],self.raceIDs['HORDE'])) and npcs.nList[creature].hostileToH:
                        tempRace = tempRace | self.raceIDs['ALLIANCE']
            if hasattr(self.qList[quest], "creatureEnd"):
                for creature in self.qList[quest].creatureEnd:
                    if ((self.qList[quest].RequiredRaces & self.raceIDs['ALLIANCE']) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (self.raceIDs['ALLIANCE'],self.raceIDs['HORDE'])) and npcs.nList[creature].hostileToA:
                        tempRace = tempRace | self.raceIDs['HORDE']
                    if ((self.qList[quest].RequiredRaces & self.raceIDs['HORDE']) != 0 or self.qList[quest].RequiredRaces == 0) and (self.qList[quest].RequiredRaces not in (self.raceIDs['ALLIANCE'],self.raceIDs['HORDE'])) and npcs.nList[creature].hostileToH:
                        tempRace = tempRace | self.raceIDs['ALLIANCE']
            if tempRace not in (0,self.raceIDs['ALL']):
                actualRequiredRaces[self.qList[quest].id] = tempRace
        return actualRequiredRaces

    def printQuestFile(self, file="output/questDB.lua", locale="enGB"):
        print("  Printing Quests file '%s'" % file)

        outfile = open(file, "w", encoding='utf-8')
        outfile.write("""-- AUTO GENERATED FILE! DO NOT EDIT!

---@type QuestieDB
local QuestieDB = QuestieLoader:ImportModule("QuestieDB");

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
        --['creatureObjective'] = 1, -- table {{creature(int), text(string), iconFile},...}, If text is nil the default "<Name> slain x/y" is used
        --['objectObjective'] = 2, -- table {{object(int), text(string), iconFile},...}
        --['itemObjective'] = 3, -- table {{item(int), text(string), iconFile},...}
        --['reputationObjective'] = 4, -- table: {faction(int), value(int)}
        --['killCreditObjective'] = 5, -- table: {{{creature(int), ...}, baseCreatureID, baseCreatureText, iconFile}, ...}
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
    ['reputationReward'] = 26, --table: {{faction(int), value(int)},...}, a list of reputation rewarded upon quest completion
    ['breadcrumbForQuestId'] = 27, -- int: quest ID for the quest this optional breadcrumb quest leads to
    ['breadcrumbs'] = 28, -- table: {questID(int), ...} quest IDs of the breadcrumbs that lead to this quest
    ['extraObjectives'] = 29, -- table: {{spawnlist, iconFile, text, objectiveIndex (optional), {{dbReferenceType, id}, ...} (optional)},...}, a list of hidden special objectives for a quest. Similar to requiredSourceItems
    ['requiredSpell'] = 30, -- int: quest is only available if character has this spellID
    ['requiredSpecialization'] = 31, -- int: quest is only available if character meets the spec requirements. Use QuestieProfessions.specializationKeys for having a spec, or QuestieProfessions.professionKeys to indicate having the profession with no spec. See QuestieProfessions.lua for more info.
    ['requiredMaxLevel'] = 32, -- int: quest is only available up to a certain level
}

QuestieDB.questData = [[return {
""")
        #excluded = self.checkStartEnd()
        outString = ""
        for id in sorted(self.qList):
            quest = self.qList[id]
            if not self.validQuestName(quest.Title):
                continue
            #if quest in excluded:
            #    continue
            outString += ("["+str(quest.id)+"] = {") #key
            title = quest.Title
            if locale != 'enGB' and quest.locales_Title[localesMap[locale]] != None:
                title = escapeDoubleQuotes(quest.locales_Title[localesMap[locale]])
            outString += ("\""+title+"\",") #name = 1
            outString += ("{") #starts = 2
            if hasattr(quest, "creatureStart") and quest.creatureStart is not None:
                outString += ("{") #npc = starts1
                for npc in quest.creatureStart:
                    outString += (str(npc)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "goStart") and quest.goStart is not None:
                outString += ("{") #obj = starts2
                for obj in quest.goStart:
                    outString += (str(obj)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "itemStart") and quest.itemStart is not None:
                outString += ("{") #itm = starts3
                for itm in quest.itemStart:
                    outString += (str(itm)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            outString += ("},")
            outString += ("{") #ends = 3
            if hasattr(quest, "creatureEnd") and quest.creatureEnd is not None: #npc = ends1
                outString += ("{")
                for npc in quest.creatureEnd:
                    outString += (str(npc)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "goEnd") and quest.goEnd is not None: #obj = ends2
                outString += ("{")
                for obj in quest.goEnd:
                    outString += (str(obj)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            outString += ("},")
            outString += (str(quest.MinLevel)+",") #minLevel = 4
            outString += (str(quest.QuestLevel)+",") #level = 5
            outString += (f'{quest.RequiredRaces},') #RequiredRaces = 6
            if hasattr(quest, "RequiredClasses") and quest.RequiredClasses is not None: #RequiredClasses = 7
                outString += (f"{quest.RequiredClasses},")
            else:
                outString += ("nil,")
            if hasattr(quest, 'Objectives') and quest.Objectives is not None: #objectives = 8
                objectives = quest.Objectives.split('\\n')
                if locale != 'enGB' and quest.locales_Title[localesMap[locale]] != None:
                    objectives = quest.locales_Title[localesMap[locale]].split('\\n')
                outString += ('{')
                for line in objectives:
                    outString += (f'"{line}",')
                outString += ('},')
            else:
                outString += ("nil,")
            if hasattr(quest, "triggerEnd") and quest.triggerEnd is not None: #trigger = 9
                outString += ("{\""+quest.triggerEnd[0]+"\",{")
                for zone in quest.triggerEnd[1].cByZone:
                    if zone not in validZoneList:
                        continue
                    outString += ("["+str(zone)+"]={")
                    for c in quest.triggerEnd[1].cByZone[zone]:
                        outString += ("{"+str(c[0])+","+str(c[1])+"},")
                    outString += ("},")
                outString += ("}},")
            else:
                outString += ("nil,")
            outString += ("{") #objectives = 10
            if hasattr(quest, "ReqCreatureId") and quest.ReqCreatureId is not None: #npc = objectives1
                outString += ("{")
                for npc in quest.ReqCreatureId:
                    outString += ("{"+str(npc[0]))
                    if npc[1] and (npc[1] != ''):
                        outString += (",\""+npc[1]+"\"},")
                    else:
                        outString += (",nil},")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "ReqGOId") and quest.ReqGOId is not None: #obj = objectives2
                outString += ("{")
                for obj in quest.ReqGOId:
                    outString += ("{"+str(obj[0]))
                    if obj[1] and (obj[1] != ''):
                        outString += (",\""+obj[1]+"\"},")
                    else:
                        outString += (",nil},")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "ReqItemId") and quest.ReqItemId is not None: #itm = objectives3
                outString += ("{")
                if (hasattr(quest, "ReqItemId")):
                    for itm in quest.ReqItemId:
                        outString += ("{"+str(itm)+",nil},")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "RepObjectiveFaction") and quest.RepObjectiveFaction is not None: #rep = objectives4
                outString += ("{"+str(quest.RepObjectiveFaction)+","+str(quest.RepObjectiveValue)+"},")
            else:
                outString += ("nil,")
            if (hasattr(quest, "killCreditData")): #multi-creatureID = objectives5
                outString += ("{")
                for collection in quest.killCreditData:
                    outString += ("{{")
                    for mobId in collection[0]:
                        outString += (str(mobId)+",")
                    outString += (str(collection[1][0])) # write baseID into spawns, because some baseIDs do have actual spawns
                    outString += ("},")
                    outString += (str(collection[1][0])+",")
                    if len(collection[1][1]) > 0:
                        outString += ("\""+collection[1][1]+"\"")
                    outString += ("},")
                outString += ("},")
            outString += ("},") #objectives = 10
            if hasattr(quest, "SrcItemId") and quest.SrcItemId is not None: #SrcItemId = 11
                outString += (str(quest.SrcItemId)+",")
            else:
                outString += ("nil,")
            if hasattr(quest, "PreQuestGroup") and quest.PreQuestGroup is not None: # 12
                outString += ("{")
                for questId in quest.PreQuestGroup:
                    outString += (str(questId)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "PreQuestSingle") and quest.PreQuestSingle is not None: # 13
                outString += ("{")
                for questId in quest.PreQuestSingle:
                    outString += (str(questId)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "ChildQuests") and quest.ChildQuests is not None: # 14
                outString += ("{")
                for questId in quest.ChildQuests:
                    outString += (str(questId)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "InGroupWith") and quest.InGroupWith is not None: # 15
                outString += ("{")
                for questId in quest.InGroupWith:
                    outString += (str(questId)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "ExclusiveTo") and quest.ExclusiveTo is not None: # 16
                outString += ("{")
                for questId in quest.ExclusiveTo:
                    outString += (str(questId)+",")
                outString += ("},")
            else:
                outString += ("nil,")
            if hasattr(quest, "ZoneOrSort") and quest.ZoneOrSort is not None: #17
                outString += (str(quest.ZoneOrSort)+",")
            else:
                outString += ("nil,")
            if hasattr(quest, "RequiredSkill") and quest.RequiredSkill is not None: #18
                outString += ("{"+str(quest.RequiredSkill)+","+str(quest.RequiredSkillValue)+"},")
            else:
                outString += ("nil,")
            if hasattr(quest, "RequiredMinRepFaction") and quest.RequiredMinRepFaction is not None: #19
                outString += ("{"+str(quest.RequiredMinRepFaction)+","+str(quest.RequiredMinRepValue)+"},")
            else:
                outString += ("nil,")
            if hasattr(quest, "RequiredMaxRepFaction") and quest.RequiredMaxRepFaction is not None: #20
                outString += ("{"+str(quest.RequiredMaxRepFaction)+","+str(quest.RequiredMaxRepValue)+"},")
            else:
                outString += ("nil,")
            if hasattr(quest, 'ReqSourceId') and quest.ReqSourceId is not None: #21
                outString += ('{')
                done = []
                for itm in quest.ReqSourceId:
                    if itm in done:
                        continue
                    outString += (f'{itm},')
                    done.append(itm)
                outString += ('},')
            else:
                outString += ('nil,')
            if hasattr(quest, 'NextQuestInChain') and quest.NextQuestInChain is not None: #22
                outString += (f'{quest.NextQuestInChain},')
            else:
                outString += ('nil,')
            if hasattr(quest, 'QuestFlags') and quest.QuestFlags is not None: # 23
                outString += (f'{quest.QuestFlags},')
            else:
                outString += ('nil,')
            if hasattr(quest, 'SpecialFlags') and quest.SpecialFlags is not None: # 24
                outString += (f'{quest.SpecialFlags},')
            else:
                outString += ('nil,')
            if hasattr(quest, 'ParentQuest') and quest.ParentQuest is not None: # 25
                outString += (f'{quest.ParentQuest},')
            else:
                outString += ('nil,')

            if hasattr(quest, 'RepReward') and len(quest.RepReward) > 0: #26
                outString += ('{')
                for factionId in sorted(quest.RepReward):
                    outString += ("{" + str(factionId) + ","+ str(quest.RepReward[factionId])+"},")
                outString += ('},')
            else:
                outString += ('nil,')

            if hasattr(quest, 'BreadcrumbForQuestId'): #27
                outString += (str(quest.BreadcrumbForQuestId)+",")
            else:
                outString += ('nil,')

            if hasattr(quest, 'Breadcrumbs'): #28
                outString += ('{')
                for qid in quest.Breadcrumbs:
                    outString += f'{qid},'
                outString += '},'
            else:
                outString += ('nil,')

            outString += ("},\n")
        outString += ("}]]\n")

        outfile.write(removeTrailingData(outString))
        outfile.close()

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
