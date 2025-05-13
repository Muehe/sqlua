
def read_trinity_quest_list(cursor, dictCursor):
    print("Selecting quest related MySQL tables...")
    print("  SELECT quest_template")
    cursor.execute("""
        SELECT
        qt.ID,  # 0
        qt.MinLevel as MinLevel,  # 1
        qt.QuestLevel as QuestLevel,  # 2
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
        qta.BreadcrumbForQuestId, # 52
        qt.RewardFactionID1,  # 53
        qt.RewardFactionID2,  # 54
        qt.RewardFactionID3,  # 55
        qt.RewardFactionID4,  # 56
        qt.RewardFactionID5,  # 57
        qt.RewardFactionValue1,  # 58
        qt.RewardFactionValue2,  # 59
        qt.RewardFactionValue3,  # 60
        qt.RewardFactionValue4,  # 61
        qt.RewardFactionValue5,  # 62
        qt.AreaDescription  # 63
        
        FROM quest_template as qt LEFT JOIN quest_template_addon as qta ON qt.ID = qta.ID
    """)

    # TODO: Use BreadcrumbForQuestId to mark quests as breadcrumb

    quest_template_cache = {}
    for a in cursor.fetchall():
        quest_template_cache[a[0]] = a

    quest_template = []

    print("  SELECT quest_objectives")
    # Type: 0 = creature, 1 = item, 2 = object, 3 = creature, 4 = currency, 5 = spell, 6 = reputation (positive), 7 = reputation (negative), 8 = money, 9 = killPlayer, 10 = areatrigger/event
    cursor.execute("SELECT QuestID, Type, `Order`, ObjectID, Amount FROM quest_objectives")
    
    quest_objectives = {}
    for a in cursor.fetchall():
        if not a[0] in quest_objectives:
            quest_objectives[a[0]] = []
        quest_objectives[a[0]].append(a)
        
    for quest_id, quest in quest_template_cache.items():
        objectives = quest_objectives.get(quest_id)
        entry = list(quest)
        if not objectives:
            quest_template.append(entry)
            continue
        objectives = list(objectives)

        for o in objectives:
            q_type = o[1]
            q_order = o[2]
            target = o[3]
            if q_type == 0 or q_type == 3:  # creature
                if q_order == 0:
                    entry[29] = target
                elif q_order == 1:
                    entry[30] = target
                elif q_order == 2:
                    entry[31] = target
                elif q_order == 3:
                    entry[32] = target
            if q_type == 2:  # object
                if q_order == 0:
                    entry[29] = -target
                elif q_order == 1:
                    entry[30] = -target
                elif q_order == 2:
                    entry[31] = -target
                elif q_order == 3:
                    entry[32] = -target
            if q_type == 1:  # item
                if q_order == 0:
                    entry[21] = target
                elif q_order == 1:
                    entry[22] = target
                elif q_order == 2:
                    entry[23] = target
                elif q_order == 3:
                    entry[24] = target
            if q_type == 5:  # spell
                if q_order == 0:
                    entry[33] = target
                elif q_order == 1:
                    entry[34] = target
                elif q_order == 2:
                    entry[35] = target
                elif q_order == 3:
                    entry[36] = target
            if (q_type == 6 or q_type == 7) and q_order == 0:  # reputation (only take the first one)
                entry[8] = target
                entry[9] = o[4]
            quest_template.append(entry)

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

    # TODO: Do this later `quest_template_locale`
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
