
def read_trinity_quest_list(cursor, dictCursor):
    print("Selecting quest related MySQL tables...")
    print("  SELECT quest_template")
    cursor.execute("""
        SELECT
        qt.ID,  # 0
        0 as MinLevel,  # 1
        -1 as QuestLevel,  # 2
        qt.QuestType,  # 3
        qta.AllowableClasses,  # 4
        qt.AllowableRaces,  # 5
        qta.RequiredSkillID,  # 6
        qta.RequiredSkillPoints,  # 7
        0 as RepObjectiveFaction,  # 8
        0 as RepObjectiveValue,  # 9
        qta.RequiredMinRepFaction,  # 10
        qta.RequiredMinRepValue,  # 11
        qta.RequiredMaxRepFaction,  # 12
        qta.RequiredMaxRepValue,  # 13
        qt.Flags,  # 14
        qta.PrevQuestId,  # 15
        qta.NextQuestId,  # 16
        0 as NextQuestInChain,  # 17
        qta.ExclusiveGroup,  # 18
        qt.LogTitle,  # 19
        qt.LogDescription,  # 20
        0 as ReqItemId1,  # 21
        0 as ReqItemId2,  # 22
        0 as ReqItemId3,  # 23
        0 as ReqItemId4,  # 24
        0 as ReqSourceId1,  # 25
        0 as ReqSourceId2,  # 26
        0 as ReqSourceId3,  # 27
        0 as ReqSourceId4,  # 28
        0 as ReqCreatureOrGOId1,  # 29
        0 as ReqCreatureOrGOId2,  # 30
        0 as ReqCreatureOrGOId3,  # 31
        0 as ReqCreatureOrGOId4,  # 32
        0 as ReqSpellCast1,  # 33
        0 as ReqSpellCast2,  # 34
        0 as ReqSpellCast3,  # 35
        0 as ReqSpellCast4,  # 36
        qt.POIContinent,  # 37
        qt.POIx,  # 38
        qt.POIy,  # 39
        NULL as StartScript,  # 40
        NULL as CompleteScript,  # 41
        qt.StartItem,  # 42
        qt.QuestSortID as ZoneOrSort,  # 43
        2 as Method,  # 44
        '' as ObjectiveText1,  # 45
        '' as ObjectiveText2,  # 46
        '' as ObjectiveText3,  # 47
        '' as ObjectiveText4,  # 48
        '' as EndText,  # 49
        qt.QuestDescription,  # 50
        qta.SpecialFlags,  # 51
        qt.RewardFactionID1,  # 52
        qt.RewardFactionID2,  # 53
        qt.RewardFactionID3,  # 54
        qt.RewardFactionID4,  # 55
        qt.RewardFactionID5,  # 56
        qt.RewardFactionValue1,  # 57
        qt.RewardFactionValue2,  # 58
        qt.RewardFactionValue3,  # 59
        qt.RewardFactionValue4,  # 60
        qt.RewardFactionValue5  # 61
        
        FROM quest_template as qt INNER JOIN quest_template_addon as qta ON qt.ID = qta.ID
    """)

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

    print("  SELECT creature_queststarter")
    creature_quest_starter = {}
    cursor.execute("SELECT id, quest FROM creature_queststarter")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if not quest in creature_quest_starter:
            creature_quest_starter[quest] = []
        creature_quest_starter[quest].append((entry, quest))

    print("  SELECT creature_questender")
    creature_quest_ender = {}
    cursor.execute("SELECT id, quest FROM creature_questender")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if not quest in creature_quest_ender:
            creature_quest_ender[quest] = []
        creature_quest_ender[quest].append((entry, quest))

    print("  SELECT gameobject_queststarter")
    gameobject_quest_starter = {}
    cursor.execute("SELECT id, quest FROM gameobject_queststarter")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if not quest in gameobject_quest_starter:
            gameobject_quest_starter[quest] = []
        gameobject_quest_starter[quest].append((entry, quest))

    print("  SELECT gameobject_questender")
    gameobject_quest_ender = {}
    cursor.execute("SELECT id, quest FROM gameobject_questender")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if not quest in gameobject_quest_ender:
            gameobject_quest_ender[quest] = []
        gameobject_quest_ender[quest].append((entry, quest))

    # TODO: Where do we get this data from?
    # print("  SELECT item_template")
    # cursor.execute("SELECT entry, startquest FROM item_template")
    item_quest_starter = {}
    # for a in cursor.fetchall():
    #     if (a[1] in item_questrelation):
    #         item_questrelation[a[1]].append(a)
    #     else:
    #         item_questrelation[a[1]] = []
    #         item_questrelation[a[1]].append(a)

    print("  SELECT areatrigger_involvedrelation")
    cursor.execute("SELECT id, quest FROM areatrigger_involvedrelation")
    areatrigger_involvedrelation = {}
    for a in cursor.fetchall():
        if a[1] in areatrigger_involvedrelation:
            areatrigger_involvedrelation[a[1]].append(a)
        else:
            areatrigger_involvedrelation[a[1]] = []
            areatrigger_involvedrelation[a[1]].append(a)

    # TODO: Do this later
    # print("  SELECT locales_quest")
    # count = dictCursor.execute("SELECT * FROM locales_quest")
    loc_quests = {}
    # for _ in range(0, count):
    #     q = dictCursor.fetchone()
    #     loc_quests[q['entry']] = q
    print("Done.")
    return {
        'quest_template': quest_template,
        'creature_killcredit': creature_killcredit,
        'creature_involvedrelation': creature_quest_ender,
        'gameobject_involvedrelation': gameobject_quest_ender,
        'creature_questrelation': creature_quest_starter,
        'gameobject_questrelation': gameobject_quest_starter,
        'item_questrelation': item_quest_starter,
        'areatrigger_involvedrelation': areatrigger_involvedrelation,
        'locales_quest': loc_quests
    }
