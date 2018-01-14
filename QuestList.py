from Quest import *
import re

class QuestList():
    """Holds a list of Quest() objects. Requires a pymysql cursor to cmangos classicdb."""
    def __init__(self, cursor, locale = "enGB"):
        self.qList = {}
        tables = self.__getQuestTables(cursor)
        infile = open("data/AreaTrigger.dbc.CSV", "r")
        a = infile.read()
        infile.close()
        b = re.findall("(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),", a)
        areaTrigger = []
        for x in b:
            areaTrigger.append((int(x[0]), int(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5]), float(x[6]), float(x[7]), float(x[8]), float(x[9])))
        if locale == "deDE":
            questNames = {}
            for quest in tables[7]: # fill the dictionary
                questNames[quest[0]] = quest
            count = 0;
            for quest in tables[0]: # replace enGB names
                if quest[0] in questNames: # only when translation is found
                    # 0entry, 19Title, 20Objectives, 45ObjectiveText1, 46ObjectiveText2, 47ObjectiveText3, 48ObjectiveText4, 49EndText
                    # 0entry, 1Title_loc3, 2Objectives_loc3, 3ObjectiveText1_loc3, 4ObjectiveText2_loc3, 5ObjectiveText3_loc3, 6ObjectiveText4_loc3, 7EndText_loc3
                    q = list(quest)
                    if questNames[quest[0]][1] != None:
                        q[19] = questNames[quest[0]][1]
                    else:
                        if q[19] and q[19] != '':
                            q[19] = "TRANSLATION MISSING IN GMDB: "+q[19]
                    if questNames[quest[0]][2] != None:
                        q[20] = questNames[quest[0]][2]
                    else:
                        if q[20] and q[20] != '':
                            q[20] = "TRANSLATION MISSING IN GMDB: "+q[20]
                    if questNames[quest[0]][3] != None:
                        q[45] = questNames[quest[0]][3]
                    else:
                        if q[45] and q[45] != '':
                            q[45] = "TRANSLATION MISSING IN GMDB: "+q[45]
                    if questNames[quest[0]][4] != None:
                        q[46] = questNames[quest[0]][4]
                    else:
                        if q[46] and q[46] != '':
                            q[46] = "TRANSLATION MISSING IN GMDB: "+q[46]
                    if questNames[quest[0]][5] != None:
                        q[47] = questNames[quest[0]][5]
                    else:
                        if q[47] and q[47] != '':
                            q[47] = "TRANSLATION MISSING IN GMDB: "+q[47]
                    if questNames[quest[0]][6] != None:
                        q[48] = questNames[quest[0]][6]
                    else:
                        if q[48] and q[48] != '':
                            q[48] = "TRANSLATION MISSING IN GMDB: "+q[48]
                    if questNames[quest[0]][7] != None:
                        q[49] = questNames[quest[0]][7]
                    else:
                        if q[49] and q[49] != '':
                            q[49] = "TRANSLATION MISSING IN GMDB: "+q[49]
                    tables[0][count] = tuple(q)
                count += 1
        print("Adding Quests...")
        count = len(tables[0])
        for quest in tables[0]:
            self.__addQuest(quest, tables[1:], areaTrigger)
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
                    self.qList[abs(quest.PrevQuestId)].addSub(questId)
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
                    quest.addSub(abs(quest.NextQuestId))
        for questId in self.qList:
            quest = self.qList[questId]
            if quest.PreQuestSingle == []:
                delattr(quest, "PreQuestSingle")
            if quest.PreQuestGroup == []:
                delattr(quest, "PreQuestGroup")
            if quest.SubQuests == []:
                delattr(quest, "SubQuests")
        print("Done.")

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
        newQuest = Quest(quest, tables, areaTrigger)
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

    def __getQuestTables(self, cursor):
        """only used by constructor"""
        print("Selecting quest related MySQL tables...")
        # SrcItemId needed to check for spell_script_target (type and targetEntry) via item_template.spellId
        cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort, Method, ObjectiveText1, ObjectiveText2, ObjectiveText3, ObjectiveText4, EndText FROM quest_template")
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
        cursor.execute("SELECT entry, Title_loc3, Objectives_loc3, ObjectiveText1_loc3, ObjectiveText2_loc3, ObjectiveText3_loc3, ObjectiveText4_loc3, EndText_loc3 FROM locales_quest")
        loc_quest_deDE = []
        for a in cursor.fetchall():
            loc_quest_deDE.append(a)
        print("Done.")
        return [quest_template, creature_involvedrelation, gameobject_involvedrelation, creature_questrelation, gameobject_questrelation, item_questrelation, areatrigger_involvedrelation, loc_quest_deDE]

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

    def printQuestFile(self, file="qData.lua"):
        outfile = open(file, "w")
        functionString = """function deleteFaction(str)
    if (CdbSettings.dbMode) then
        return;
    end
    local before = CdbGetTableLength(qData);
    for key, data in pairs(qData) do
        if (data[DB_REQ_RACE] == "AH") or (data[DB_REQ_RACE] ~= str) then
            data[DB_REQ_RACE] = nil;
        else
            qData[key] = nil;
        end
    end
    local after = CdbGetTableLength(qData);
    CdbDebugPrint(2, before-after.." opposite faction quests deleted");
end
function deleteClasses()
    if (not CdbSettings.class) or (CdbSettings.dbMode) then
        return;
    end
    local before = CdbGetTableLength(qData);
    local classes = {"Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight", "Shaman", "Mage", "Warlock", "Druid"};
    local playerClass = false;
    for key, name in pairs(classes) do
        if name == CdbSettings.class then
            playerClass = key - 1;
        end
    end
    if playerClass then
        for key, data in pairs(qData) do
            if data[DB_REQ_CLASS] then
                local found = false;
                for k, class in pairs(data[DB_REQ_CLASS]) do
                    if class == playerClass then
                        found = true;
                    end
                end
                if not found then
                    qData[key] = nil;
                end
            end
        end
    end
    local after = CdbGetTableLength(qData);
    CdbDebugPrint(2, before-after.." other class quests deleted");
end
qLookup = {};
function fillQuestLookup()
    local checkedNames = {};
    for key, data in pairs(qData) do
        local name = data[DB_NAME];
        local checked = checkedNames[name];
        if not checked then
            checkedNames[name] = true;
            qLookup[name] = {};
            for k, d in pairs(qData) do
                if (d[DB_NAME] == name) then
                    if d[DB_OBJECTIVES] then
                        qLookup[name][k] = d[DB_OBJECTIVES];
                    else
                        qLookup[name][k] = '';
                    end
                end
            end
        end
    end
end
"""
        outfile.write(functionString)
        outfile.write("qData = {\n")
        excluded = self.checkStartEnd()
        for id in sorted(self.qList):
            quest = self.qList[id]
            if quest in excluded:
                continue
            outfile.write("\t["+str(quest.id)+"] = {") #key
            outfile.write("\""+quest.Title+"\",") #name = 1
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
            outfile.write("\""+self.getFactionString(quest.RequiredRaces)+"\",") #RequiredRaces = 6
            if (hasattr(quest, "RequiredClasses")): #RequiredClasses = 7
                outfile.write("{")
                for n in self.unpackBitMask(quest.RequiredClasses):
                    outfile.write(str(n)+",")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "Objectives")) and (len(self.allQuests(Title = quest.Title)) > 1): #objectives = 8
                if quest.id == 4641:
                    quest.Objectives = quest.Objectives[0:-5]
                outfile.write("\""+quest.Objectives+"\",")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "triggerEnd")): #trigger = 9
                outfile.write("{\""+quest.triggerEnd[0]+"\",{")
                for tri in quest.triggerEnd[1].cByZone:
                    outfile.write("["+str(tri)+"]={")
                    for c in quest.triggerEnd[1].cByZone[tri]:
                        outfile.write("{"+str(c[0])+","+str(c[1])+"},")
                    outfile.write("},")
                outfile.write("}},")
            else:
                outfile.write("nil,")
            outfile.write("{") #ReqCreatureOrGOOrItm = 10
            if (hasattr(quest, "ReqCreatureId")): #npc = ReqCreatureOrGOOrItm1
                outfile.write("{")
                for npc in quest.ReqCreatureId:
                    outfile.write("{"+str(npc[0]))
                    if (npc[1] != ''):
                        outfile.write(",\""+npc[1]+"\"},")
                    else:
                        outfile.write(",nil},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ReqGOId")): #obj = ReqCreatureOrGOOrItm2
                outfile.write("{")
                for obj in quest.ReqGOId:
                    outfile.write("{"+str(abs(obj[0]))+",\""+str(obj[1])+"\"},")
                outfile.write("},")
            else:
                outfile.write("nil,")
            if (hasattr(quest, "ReqSourceId")) or (hasattr(quest, "ReqItemId")): #itm = ReqCreatureOrGOOrItm3
                outfile.write("{")
                if (hasattr(quest, "ReqSourceId")):
                    done = []
                    for itm in quest.ReqSourceId:
                        if itm in done:
                            continue
                        outfile.write("{"+str(itm)+",nil},")
                        done.append(itm)
                if (hasattr(quest, "ReqItemId")):
                    for itm in quest.ReqItemId:
                        outfile.write("{"+str(itm)+",nil},")
                outfile.write("},")
            else:
                outfile.write("nil,")
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
            if (hasattr(quest, "SubQuests")): # 14
                outfile.write("{")
                for questId in quest.SubQuests:
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
            outfile.write("},\n")
        outfile.write("};\n")
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
