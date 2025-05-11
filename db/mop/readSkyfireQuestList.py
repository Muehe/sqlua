
def read_skyfire_quest_list(cursor, dictCursor):
    print("Selecting quest related MySQL tables...")
    print("  SELECT quest_template")
    cursor.execute("""
        SELECT
        Id,  # 0
        MinLevel,  # 1
        Level,  # 2
        Type,  # 3
        RequiredClasses,  # 4
        RequiredRaces,  # 5
        RequiredSkillId,  # 6
        RequiredSkillPoints,  # 7
        NULL as RepObjectiveFaction,  # 8
        NULL as RepObjectiveValue,  # 9
        RequiredMinRepFaction,  # 10
        RequiredMinRepValue,  # 11
        RequiredMaxRepFaction,  # 12
        RequiredMaxRepValue,  # 13
        Flags,  # 14
        PrevQuestId,  # 15
        NextQuestId,  # 16
        NextQuestIdChain,  # 17
        ExclusiveGroup,  # 18
        Title,  # 19
        Objectives,  # 20
        NULL as ReqItemId1,  # 21
        NULL as ReqItemId2,  # 22
        NULL as ReqItemId3,  # 23
        NULL as ReqItemId4,  # 24
        NULL as ReqSourceId1,  # 25
        NULL as ReqSourceId2,  # 26
        NULL as ReqSourceId3,  # 27
        NULL as ReqSourceId4,  # 28
        NULL as ReqCreatureOrGOId1,  # 29
        NULL as ReqCreatureOrGOId2,  # 30
        NULL as ReqCreatureOrGOId3,  # 31
        NULL as ReqCreatureOrGOId4,  # 32
        NULL as ReqSpellCast1,  # 33
        NULL as ReqSpellCast2,  # 34
        NULL as ReqSpellCast3,  # 35
        NULL as ReqSpellCast4,  # 36
        PointMapId,  # 37
        PointX,  # 38
        PointY,  # 39
        NULL as StartScript,  # 40
        NULL as CompleteScript,  # 41
        SourceItemId,  # 42
        ZoneOrSort,  # 43
        Method,  # 44
        NULL as ObjectiveText1,  # 45
        NULL as ObjectiveText2,  # 46
        NULL as ObjectiveText3,  # 47
        NULL as ObjectiveText4,  # 48
        EndText,  # 49
        Details,  # 50
        SpecialFlags,  # 51
        RewardFactionId1,  # 52
        RewardFactionId2,  # 53
        RewardFactionId3,  # 54
        RewardFactionId4,  # 55
        RewardFactionId5,  # 56
        RewardFactionValueId1,  # 57
        RewardFactionValueId2,  # 58
        RewardFactionValueId3,  # 59
        RewardFactionValueId4,  # 60
        RewardFactionValueId5  # 61
    
        FROM quest_template
   """)

    quest_template = []
    for a in cursor.fetchall():
        quest_template.append(a)

    print("  SELECT quest_objective")
    cursor.execute("""
        SELECT
        questId,
        `index`,
            type,
            objectId,
            description
        
        FROM quest_objective
    """)

    for objectives in cursor.fetchall():
        quest_id = objectives[0]
        index = objectives[1]
        # Type: 0 = creature, 1 = item, 2 = object, 3 = creature, 4 = currency, 5 = spell, 6 = reputation (positive), 7 = reputation (negative), 8 = money, 9 = killPlayer, 10 = areatrigger/event
        objective_type = objectives[2]
        objective_id = objectives[3] # This is the ID matching the type
        description = objectives[4]

        if quest_id in quest_template:
            if objective_type == 0: # Creature
                quest_template[quest_id][29 + index] = objective_id
            elif objective_type == 1: # Item
                quest_template[quest_id][21 + index] = objective_id
            elif objective_type == 2: # Object
                quest_template[quest_id][29 + index] = -objective_id

            quest_template[quest_id][45 + index] = description

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
    return {
        'quest_template': quest_template,
        'creature_killcredit': creature_killcredit,
        'creature_involvedrelation': creature_quest_ender,
        'gameobject_involvedrelation': gameobject_quest_ender,
        'creature_questrelation': creature_quest_starter,
        'gameobject_questrelation': gameobject_quest_starter,
        'item_questrelation': item_questrelation,
        'areatrigger_involvedrelation': areatrigger_involvedrelation,
        'locales_quest': loc_quests
    }
