from sqlua.CoordList import *

class Quest():
    def __init__(self, quest, tables, areaTrigger):
        self.id = quest[0]
        self.MinLevel = quest[1]
        self.QuestLevel = quest[2]
        self.Type = quest[3]
        self.RequiredRaces = quest[5]
        self.Title = self.escapeName(quest[19])
        self.Method = quest[44]
        if (quest[40] != 0):
            self.StartScript = quest[40]
        if (quest[41] != 0):
            self.CompleteScript = quest[41]
        if (quest[4] != 0):
            self.RequiredClasses = quest[4]
        if (quest[6] != 0):
            self.RequiredSkill = quest[6]
        if (quest[7] != 0):
            self.RequiredSkillValue = quest[7]
        if (quest[8] != 0):
            self.RepObjectiveFaction = quest[8]
        if (quest[9] != 0):
            self.RepObjectiveValue = quest[9]
        if (quest[10] != 0):
            self.RequiredMinRepFaction = quest[10]
        if (quest[11] != 0):
            self.RequiredMinRepValue = quest[11]
        if (quest[12] != 0):
            self.RequiredMaxRepFaction = quest[12]
        if (quest[13] != 0):
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
        if (quest[20] != ''):
            self.Objectives = self.objectivesText(quest[20])
        self.ReqItemId = []
        if (quest[21] != 0):
            self.ReqItemId.append(quest[21])
        if (quest[22] != 0):
            self.ReqItemId.append(quest[22])
        if (quest[23] != 0):
            self.ReqItemId.append(quest[23])
        if (quest[24] != 0):
            self.ReqItemId.append(quest[24])
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
        self.ReqCreatureId = []
        if (quest[29] > 0):
            self.ReqCreatureId.append((quest[29], self.escapeName(quest[45])))
        if (quest[30] > 0):
            self.ReqCreatureId.append((quest[30], self.escapeName(quest[46])))
        if (quest[31] > 0):
            self.ReqCreatureId.append((quest[31], self.escapeName(quest[47])))
        if (quest[32] > 0):
            self.ReqCreatureId.append((quest[32], self.escapeName(quest[48])))
        if (self.ReqCreatureId == []):
            del self.ReqCreatureId
        self.ReqGOId = []
        if (quest[29] < 0):
            self.ReqGOId.append((quest[29], self.escapeName(quest[45])))
        if (quest[30] < 0):
            self.ReqGOId.append((quest[30], self.escapeName(quest[46])))
        if (quest[31] < 0):
            self.ReqGOId.append((quest[31], self.escapeName(quest[47])))
        if (quest[32] < 0):
            self.ReqGOId.append((quest[32], self.escapeName(quest[48])))
        if (self.ReqGOId == []):
            del self.ReqGOId
        self.ReqSpellCast = []
        if (quest[33] != 0):
            self.ReqSpellCast.append((quest[33], quest[29], self.escapeName(quest[45])))
        if (quest[34] != 0):
            self.ReqSpellCast.append((quest[34], quest[30], self.escapeName(quest[46])))
        if (quest[35] != 0):
            self.ReqSpellCast.append((quest[35], quest[31], self.escapeName(quest[47])))
        if (quest[36] != 0):
            self.ReqSpellCast.append((quest[36], quest[32], self.escapeName(quest[48])))
        if (self.ReqSpellCast == []):
            del self.ReqSpellCast
        if (quest[37] != 0):
            self.PointMapId = quest[37]
            self.PointX = quest[38]
            self.PointY = quest[39]
        if (quest[42] != 0):
            self.SrcItemId = quest[42]
        if (quest[43] != 0):
            self.ZoneOrSort = quest[43]
        self.creatureEnd = []
        for (creatureId, questId) in tables[0]:
            if (questId == self.id):
                self.creatureEnd.append(creatureId)
        if (self.creatureEnd == []):
            del self.creatureEnd
        self.creatureStart = []
        for (creatureId, questId) in tables[2]:
            if (questId == self.id):
                self.creatureStart.append(creatureId)
        if (self.creatureStart == []):
            del self.creatureStart
        self.goEnd = []
        for (goId, questId) in tables[1]:
            if (questId == self.id):
                self.goEnd.append(goId)
        if (self.goEnd == []):
            del self.goEnd
        self.goStart = []
        for (goId, questId) in tables[3]:
            if (questId == self.id):
                self.goStart.append(goId)
        if (self.goStart == []):
            del self.goStart
        self.itemStart = []
        for (itemId, questId) in tables[4]:
            if (questId == self.id):
                self.itemStart.append(itemId)
        if (self.itemStart == []):
            del self.itemStart
        self.triggerEnd = []
        triggers = []
        for (triggerId, questId) in tables[5]:
            if (questId == self.id):
                for trigger in areaTrigger:
                    if trigger[0] == triggerId:
                        triggers.append(trigger[1:])
        if (triggers == []):
            del self.triggerEnd
        else:
            text = ""
            if quest[49] == '':
                text = self.Objectives
            else:
                text = self.escapeName(quest[49])
            self.triggerEnd = (text, CoordList(triggers))
        """for locales in tables[6]:
            if locales[0] == self.id:
                self.nameDE = self.escapeName(locales[1])
                if (locales[2]):
                    self.objectivesDE = self.objectivesText(locales[2])"""

    def __repr__(self):
        return str(self.id)

    def match(self, **kwargs):
        for (key, val) in kwargs.items():
            if not (hasattr(self, key)):
                return False
        return all(getattr(self,key) == val for (key, val) in kwargs.items())

    def escapeName(self, string):
        name = string.replace('"', '\\"')
        name2 = name.replace("'", "\\'")
        return name2

    def objectivesText(self, objectives):
        split = objectives.split('$B')
        temp = '\\n'.join(split)
        split1 = temp.split('$b')
        temp = '\\n'.join(split1)
        split2 = temp.split('$c')
        temp = '$C'.join(split2)
        split3 = temp.split('$r')
        temp = '$R'.join(split3)
        split4 = temp.split('$n')
        temp = '$N'.join(split4)
        return self.escapeName(temp)
