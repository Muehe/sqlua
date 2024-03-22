from db.QuestList import QuestList

import os.path
import pickle


class CataQuestList(QuestList):

    def __init__(self, version):
        super().__init__(version)

    def run(self, cursor, dictCursor, recache=False):
        if (not os.path.isfile(f'data/cata/quests.pkl') or recache):
            print('Caching quests...')
            dicts = self.__getQuestTables(cursor, dictCursor)
            self.cacheQuests(cursor, dictCursor, dicts)
        else:
            try:
                with open(f'data/cata/quests.pkl', 'rb') as f:
                    self.qList = pickle.load(f)
                print('Using cached quests.')
            except:
                print('ERROR: Something went wrong while loading cached quests. Re-caching.')
                dicts = self.__getQuestTables(cursor, dictCursor)
                self.cacheQuests(cursor, dictCursor, dicts)

    def __getQuestTables(self, cursor, dictCursor):
        """only used by constructor"""
        print("Selecting quest related MySQL tables...")
        print("  SELECT quest_template")
        cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort, Method, ObjectiveText1, ObjectiveText2, ObjectiveText3, ObjectiveText4, EndText, Details, SpecialFlags, RewRepFaction1, RewRepFaction2, RewRepFaction3, RewRepFaction4, RewRepFaction5, RewRepValue1, RewRepValue2, RewRepValue3, RewRepValue4, RewRepValue5 FROM quest_template")
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

        print("  SELECT quest_relation")
        creature_involvedrelation = {}  # Creature quest end
        creature_questrelation = {}  # Creature quest start
        gameobject_involvedrelation = {}  # Object quest end
        gameobject_questrelation = {}  # Object quest start
        # actor 0=creature, 1=gameobject
        # entry=creature_template.entry or gameobject_template.entry
        # quest=quest_template.entry
        # role 0=start, 1=end
        cursor.execute("SELECT actor, entry, quest, role FROM quest_relations")
        for a in cursor.fetchall():
            entry = a[1]
            quest = a[2]
            if a[0] == 0:
                if a[3] == 0:
                    if quest in creature_questrelation:
                        creature_questrelation[quest].append((entry, quest))
                    else:
                        creature_questrelation[quest] = []
                        creature_questrelation[quest].append((entry, quest))
                elif a[3] == 1:
                    if quest in creature_involvedrelation:
                        creature_involvedrelation[quest].append((entry, quest))
                    else:
                        creature_involvedrelation[quest] = []
                        creature_involvedrelation[quest].append((entry, quest))
            elif a[0] == 1:
                if a[3] == 0:
                    if quest in gameobject_questrelation:
                        gameobject_questrelation[quest].append((entry, quest))
                    else:
                        gameobject_questrelation[quest] = []
                        gameobject_questrelation[quest].append((entry, quest))
                elif a[3] == 1:
                    if quest in gameobject_involvedrelation:
                        gameobject_involvedrelation[quest].append((entry, quest))
                    else:
                        gameobject_involvedrelation[quest] = []
                        gameobject_involvedrelation[quest].append((entry, quest))

        print("  SELECT item_template")
        cursor.execute("SELECT entry, startquest FROM item_template")
        item_questrelation = {}
        for a in cursor.fetchall():
            if (a[1] in item_questrelation):
                item_questrelation[a[1]].append(a)
            else:
                item_questrelation[a[1]] = []
                item_questrelation[a[1]].append(a)

        print("  SELECT areatrigger_involvedrelation")
        cursor.execute("SELECT id, quest FROM areatrigger_involvedrelation")
        areatrigger_involvedrelation = {}
        for a in cursor.fetchall():
            if (a[1] in areatrigger_involvedrelation):
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
        return {'quest_template': quest_template,
                'creature_killcredit': creature_killcredit,
                'creature_involvedrelation': creature_involvedrelation,
                'gameobject_involvedrelation': gameobject_involvedrelation,
                'creature_questrelation': creature_questrelation,
                'gameobject_questrelation': gameobject_questrelation,
                'item_questrelation': item_questrelation,
                'areatrigger_involvedrelation': areatrigger_involvedrelation,
                'locales_quest': loc_quests}
