from db.CoordList import *
from db.Utilities import *

class Quest():
    def __init__(self, quest, dicts, areaTrigger, version, translations=False):
        self.version = version
        self.id = quest[0]
        self.MinLevel = quest[1]
        self.QuestLevel = quest[2]
        self.Type = quest[3]
        self.RequiredRaces = quest[5]
        # Fix TBC+ masks in Classic data, change quests available to all races to 0 (no requirements)
        if version == 'cata':
            if quest[5] == 2099199:
                self.RequiredRaces = 0
        elif version == 'classic':
            if quest[5] == 690:
                self.RequiredRaces = 178
            elif quest[5] == 1101:
                self.RequiredRaces = 77
            elif quest[5] == 255:
                self.RequiredRaces = 0
        else:
            if quest[5] == 1791:
                self.RequiredRaces = 0
        self.Title = escapeDoubleQuotes(quest[19])
        self.locales_Title = {}
        for x in range(1, 9):
            if not translations:
                continue
            self.locales_Title[x] = dicts['locales_quest'][self.id]['Title_loc'+str(x)]
        self.Method = quest[44]
        if (quest[40] != 0):
            self.StartScript = quest[40]
        if (quest[41] != 0):
            self.CompleteScript = quest[41]
        if (quest[4] != 0):
            self.RequiredClasses = quest[4]
        if (quest[6] != 0):
            self.RequiredSkill = quest[6]
            self.RequiredSkillValue = quest[7]
        if (quest[8] != 0):
            self.RepObjectiveFaction = quest[8]
            self.RepObjectiveValue = quest[9]
        if (quest[10] != 0):
            self.RequiredMinRepFaction = quest[10]
            self.RequiredMinRepValue = quest[11]
        if (quest[12] != 0):
            self.RequiredMaxRepFaction = quest[12]
            self.RequiredMaxRepValue = quest[13]
        if (quest[14] != 0):
            self.QuestFlags = quest[14]
        if (quest[15] != 0):
            self.PrevQuestId = quest[15]
        if (quest[16] != 0):
            self.NextQuestId = quest[16]
        if (quest[17] != 0):
            self.NextQuestInChain = quest[17]
        if (quest[18] != 0):
            self.ExclusiveGroup = quest[18]
        if (quest[20] != '' and quest[20] != None):
            self.Objectives = self.objectivesText(quest[20])
            self.locales_Objectives = {}
            for x in range(1, 9):
                if not translations:
                    continue
                self.locales_Objectives[x] = dicts['locales_quest'][self.id]['Objectives_loc'+str(x)]
        self.ObjectiveList = [{},{},{},{},{}]
        self.ObjectiveList[0]['text'] = escapeDoubleQuotes(quest[45])
        self.ObjectiveList[1]['text'] = escapeDoubleQuotes(quest[46])
        self.ObjectiveList[2]['text'] = escapeDoubleQuotes(quest[47])
        self.ObjectiveList[3]['text'] = escapeDoubleQuotes(quest[48])
        self.ReqItemId = []
        if ((quest[21] != 0) and (quest[21] != quest[42])):
            self.ReqItemId.append(quest[21])
            self.ObjectiveList[0]['type'] = 'item'
            self.ObjectiveList[0]['id'] = quest[21]
        if ((quest[22] != 0) and (quest[22] != quest[42])):
            self.ReqItemId.append(quest[22])
            self.ObjectiveList[1]['type'] = 'item'
            self.ObjectiveList[1]['id'] = quest[22]
        if ((quest[23] != 0) and (quest[23] != quest[42])):
            self.ReqItemId.append(quest[23])
            self.ObjectiveList[2]['type'] = 'item'
            self.ObjectiveList[2]['id'] = quest[23]
        if ((quest[24] != 0) and (quest[24] != quest[42])):
            self.ReqItemId.append(quest[24])
            self.ObjectiveList[3]['type'] = 'item'
            self.ObjectiveList[3]['id'] = quest[24]
        if (self.ReqItemId == []):
            del self.ReqItemId
        self.ReqSourceId = []
        if (quest[25] != 0):
            self.ReqSourceId.append(quest[25])
        if (quest[26] != 0):
            self.ReqSourceId.append(quest[26])
        if (quest[27] != 0):
            self.ReqSourceId.append(quest[27])
        if (quest[28] != 0):
            self.ReqSourceId.append(quest[28])
        if (self.ReqSourceId == []):
            del self.ReqSourceId
        self.locales_ObjectiveTexts = {1:{}, 2:{}, 3:{}, 4:{}}
        for x in range(1, 5):
            for y in range(1, 9):
                if not translations:
                    continue
                if dicts['locales_quest'][self.id]['ObjectiveText'+str(x)+'_loc'+str(y)] != None:
                    self.locales_ObjectiveTexts[x][y] = escapeDoubleQuotes(dicts['locales_quest'][self.id]['ObjectiveText'+str(x)+'_loc'+str(y)]).replace("\n","\\n")

        #ReqCreatureId
        self.ReqCreatureId = []
        if ((quest[29] > 0)):
            self.ReqCreatureId.append((quest[29], escapeDoubleQuotes(quest[45]), self.locales_ObjectiveTexts[1]))
            self.ObjectiveList[0]['type'] = 'monster'
            self.ObjectiveList[0]['id'] = quest[29]
        if ((quest[30] > 0)):
            self.ReqCreatureId.append((quest[30], escapeDoubleQuotes(quest[46]), self.locales_ObjectiveTexts[2]))
            self.ObjectiveList[1]['type'] = 'monster'
            self.ObjectiveList[1]['id'] = quest[30]
        if ((quest[31] > 0)):
            self.ReqCreatureId.append((quest[31], escapeDoubleQuotes(quest[47]), self.locales_ObjectiveTexts[3]))
            self.ObjectiveList[2]['type'] = 'monster'
            self.ObjectiveList[2]['id'] = quest[31]
        if ((quest[32] > 0)):
            self.ReqCreatureId.append((quest[32], escapeDoubleQuotes(quest[48]), self.locales_ObjectiveTexts[4]))
            self.ObjectiveList[3]['type'] = 'monster'
            self.ObjectiveList[3]['id'] = quest[32]

        if self.version != 'classic':
            cleaned = []
            killCreditMobs = []
            for rootid in self.ReqCreatureId:
                if rootid[0] in dicts['creature_killcredit']:
                    killCreditMobs.append((dicts['creature_killcredit'][rootid[0]], rootid))
                else:
                    cleaned.append(rootid)
            if len(killCreditMobs) > 0:
                self.killCreditData = killCreditMobs
                self.ReqCreatureId = cleaned

        if (self.ReqCreatureId == []):
            del self.ReqCreatureId

        #ReqGoId
        self.ReqGOId = []
        if ((quest[29] < 0)):
            self.ReqGOId.append((abs(quest[29]), escapeDoubleQuotes(quest[45]), self.locales_ObjectiveTexts[1]))
            self.ObjectiveList[0]['type'] = 'object'
            self.ObjectiveList[0]['id'] = abs(quest[29])
        if ((quest[30] < 0)):
            self.ReqGOId.append((abs(quest[30]), escapeDoubleQuotes(quest[46]), self.locales_ObjectiveTexts[2]))
            self.ObjectiveList[1]['type'] = 'object'
            self.ObjectiveList[1]['id'] = abs(quest[30])
        if ((quest[31] < 0)):
            self.ReqGOId.append((abs(quest[31]), escapeDoubleQuotes(quest[47]), self.locales_ObjectiveTexts[3]))
            self.ObjectiveList[2]['type'] = 'object'
            self.ObjectiveList[2]['id'] = abs(quest[31])
        if ((quest[32] < 0)):
            self.ReqGOId.append((abs(quest[32]), escapeDoubleQuotes(quest[48]), self.locales_ObjectiveTexts[4]))
            self.ObjectiveList[3]['type'] = 'object'
            self.ObjectiveList[3]['id'] = abs(quest[32])
        if (self.ReqGOId == []):
            del self.ReqGOId
        
        #ReqSpellCast
        self.ReqSpellCast = []
        if (quest[33] != 0):
            self.ReqSpellCast.append((quest[33], quest[29], escapeDoubleQuotes(quest[45]), self.locales_ObjectiveTexts[1]))
            self.ObjectiveList[0]['reqSpellCast'] = quest[33]
        if (quest[34] != 0):
            self.ReqSpellCast.append((quest[34], quest[30], escapeDoubleQuotes(quest[46]), self.locales_ObjectiveTexts[2]))
            self.ObjectiveList[1]['reqSpellCast'] = quest[34]
        if (quest[35] != 0):
            self.ReqSpellCast.append((quest[35], quest[31], escapeDoubleQuotes(quest[47]), self.locales_ObjectiveTexts[3]))
            self.ObjectiveList[2]['reqSpellCast'] = quest[35]
        if (quest[36] != 0):
            self.ReqSpellCast.append((quest[36], quest[32], escapeDoubleQuotes(quest[48]), self.locales_ObjectiveTexts[4]))
            self.ObjectiveList[3]['reqSpellCast'] = quest[36]
        if (self.ReqSpellCast == []):
            del self.ReqSpellCast
        #??? what is this
        for i in range(0, 4):
            if len(self.ObjectiveList[i]) == 1:
                self.ObjectiveList[i] = False

        
        if (quest[37] != 0):
            self.PointMapId = quest[37]
            self.PointX = quest[38]
            self.PointY = quest[39]
        if (quest[42] != 0):
            self.SrcItemId = quest[42]
        if (quest[43] != 0):
            self.ZoneOrSort = quest[43]

        #CreatureEnd
        self.creatureEnd = []
        if self.id in dicts['creature_involvedrelation']:
            for (creatureId, questId) in dicts['creature_involvedrelation'][self.id]:
                if (questId == self.id):
                    self.creatureEnd.append(creatureId)
        if (self.creatureEnd == []):
            del self.creatureEnd

        #CreatureStart
        self.creatureStart = []
        if self.id in dicts['creature_questrelation']:
            for (creatureId, questId) in dicts['creature_questrelation'][self.id]:
                if (questId == self.id):
                    self.creatureStart.append(creatureId)
        if (self.creatureStart == []):
            del self.creatureStart
        
        #goEnd
        self.goEnd = []
        if self.id in dicts['gameobject_involvedrelation']:
            for (goId, questId) in dicts['gameobject_involvedrelation'][self.id]:
                if (questId == self.id):
                    self.goEnd.append(goId)
        if (self.goEnd == []):
            del self.goEnd
        
        #goStart
        self.goStart = []
        if self.id in dicts['gameobject_questrelation']:
            for (goId, questId) in dicts['gameobject_questrelation'][self.id]:
                if (questId == self.id):
                    self.goStart.append(goId)
        if (self.goStart == []):
            del self.goStart

        #itemStart
        self.itemStart = []
        if self.id in dicts['item_questrelation']:
            for (itemId, questId) in dicts['item_questrelation'][self.id]:
                if (questId == self.id):
                    self.itemStart.append(itemId)
        if (self.itemStart == []):
            del self.itemStart

        # AreaTriggers
        self.triggerEnd = []
        triggers = []
        triggerZoneDict = {}
        with open(f'data/{version}/areaTrigger_preExtract.csvzone_and_area.csv', 'r') as infile:
            import csv
            reader = csv.reader(infile)
            next(reader)
            for row in reader:
                triggerZoneDict[int(row[0])] = int(row[1])
            infile.close()
                
        if self.id in dicts['areatrigger_involvedrelation']:
            for (triggerId, questId) in dicts['areatrigger_involvedrelation'][self.id]:
                if (questId == self.id):
                    for trigger in areaTrigger:
                        if trigger[0] == triggerId:
                            if triggerId in triggerZoneDict:
                                triggers.append((trigger[1], trigger[2], trigger[3], triggerZoneDict[triggerId]))
                            else:
                                triggers.append((trigger[1], trigger[2], trigger[3]))
        if (triggers == []):
            del self.triggerEnd
        else:
            if version == 'cata' and quest[62]:  # AreaDescription
                text = quest[62]
            elif quest[49] == '':
                text = self.Objectives
            else:
                text = escapeDoubleQuotes(quest[49])
            self.triggerEnd = (text, CoordList(triggers, version))
            self.ObjectiveList[4] = {'text': text, 'type': 'areaTrigger', 'coords': CoordList(triggers, version)}
            self.locales_EndText = {}
            for x in range(1, 9):
                if not translations:
                    continue
                self.locales_EndText[x] = dicts['locales_quest'][self.id]['EndText_loc'+str(x)]

        self.Details = escapeDoubleQuotes(quest[50])
        self.locales_Details = {}
        for x in range(1, 9):
            if not translations:
                continue
            if dicts['locales_quest'][self.id]['Details_loc'+str(x)] != None:
                self.locales_Details[x] = escapeDoubleQuotes(dicts['locales_quest'][self.id]['Details_loc'+str(x)])
        self.ExclusiveTo = []
        self.InGroupWith = []
        self.PreQuestGroup = []
        self.PreQuestSingle = []
        self.ChildQuests = []
        if (quest[51] != 0):
            self.SpecialFlags = quest[51]

        #Reputation reward
        self.RepReward = self.getRep(quest)
            

    def getRep(self, quest):
        self.RepReward = {}
        if self.version == "wotlk":
            data = [0, 10, 25, 75, 150, 250, 350, 500, 1000, 5]
            for i in range(0, 5):
                if (quest[52+i] != 0):  #RewRepFaction
                    if quest[57+i] != 0 and quest[57+i] > 1000: #RewRepValue
                        self.RepReward[quest[52+i]] = int(quest[57+i]/100)
                    elif(quest[57+5+i] != 0): #RewRepValueId
                        self.RepReward[quest[52+i]] = int(data[abs(quest[57+5+i])] * (quest[57+5+i] / abs(quest[57+5+i])))
        else:
            for i in range(0, 5):
                if (quest[52+i] != 0): #RewRepFaction
                    self.RepReward[quest[52+i]] = quest[57+i] #RewRepValueId

        return self.RepReward



    def __repr__(self):
        return str(self.id)

    def printQuest(self):
        keys = ['id',
                'Title',
                'locales_Title',
                'ZoneOrSort',
                'MinLevel',
                'QuestLevel',
                'Type',
                'Method',
                'QuestFlags',
                'PrevQuestId',
                'NextQuestId',
                'NextQuestInChain',
                'ExclusiveGroup',
                'ExclusiveTo',
                'InGroupWith',
                'PreQuestGroup',
                'PreQuestSingle',
                'ChildQuests',
                'StartScript',
                'creatureStart',
                'goStart',
                'itemStart',
                'CompleteScript',
                'creatureEnd',
                'goEnd',
                'triggerEnd',
                'RequiredRaces',
                'RequiredClasses',
                'RequiredSkill',
                'RequiredSkillValue',
                'RequiredMinRepFaction',
                'RequiredMinRepValue',
                'RequiredMaxRepFaction',
                'RequiredMaxRepValue',
                'Objectives',
                'RepObjectiveFaction',
                'RepObjectiveValue',
                'ReqItemId',
                'ReqCreatureId',
                'ReqGOId',
                'ReqSpellCast',
                'ReqSourceId',
                'SrcItemId',
                'SpecialFlags',
               ]
        for k in keys:
            if hasattr(self, k):
                print(k, ": ", getattr(self, k))

    def match(self, **kwargs):
        for (key, val) in kwargs.items():
            if not (hasattr(self, key)):
                return False
        return all(getattr(self,key) == val for (key, val) in kwargs.items())

    def objectivesText(self, objectives):
        split0 = objectives.split('$B')
        temp = '\\n'.join(split0)
        split1 = temp.split('$b')
        temp = '\\n'.join(split1)
        split2 = temp.split('$c')
        temp = '$C'.join(split2)
        split3 = temp.split('$r')
        temp = '$R'.join(split3)
        split4 = temp.split('$n')
        temp = '$N'.join(split4)
        split5 = temp.split('  ')
        temp = ' '.join(split5)
        # Remove trailing \n
        while temp[-2:] == '\\n':
            temp = temp[:-2]
        return escapeDoubleQuotes(temp)

    def addGroup(self, value):
        if value not in self.InGroupWith:
            self.InGroupWith.append(value)

    def addExclusive(self, value):
        if value not in self.ExclusiveTo:
            self.ExclusiveTo.append(value)

    def addPreGroup(self, value):
        if value not in self.PreQuestGroup:
            self.PreQuestGroup.append(value)

    def addPreSingle(self, value):
        if value not in self.PreQuestSingle:
            self.PreQuestSingle.append(value)

    def addChild(self, value):
        if value not in self.ChildQuests:
            self.ChildQuests.append(value)

    def setParent(self, value):
        self.ParentQuest = value
