
def read_mangos_quest_list(cursor, dictCursor):
    print("Selecting quest related MySQL tables...")
    print("  SELECT quest_template")
    cursor.execute("""
        SELECT
        entry,  # 0
        MinLevel,  # 1
        QuestLevel,  # 2
        Type,  # 3
        RequiredClasses,  # 4
        RequiredRaces,  # 5
        RequiredSkill,  # 6
        RequiredSkillValue,  # 7
        RepObjectiveFaction,  # 8
        RepObjectiveValue,  # 9
        RequiredMinRepFaction,  # 10
        RequiredMinRepValue,  # 11
        RequiredMaxRepFaction,  # 12
        RequiredMaxRepValue,  # 13
        QuestFlags,  # 14
        PrevQuestId,  # 15
        NextQuestId,  # 16
        NextQuestInChain,  # 17
        ExclusiveGroup,  # 18
        Title,  # 19
        Objectives,  # 20
        ReqItemId1,  # 21
        ReqItemId2,  # 22
        ReqItemId3,  # 23
        ReqItemId4,  # 24
        ReqSourceId1,  # 25
        ReqSourceId2,  # 26
        ReqSourceId3,  # 27
        ReqSourceId4,  # 28
        ReqCreatureOrGOId1,  # 29
        ReqCreatureOrGOId2,  # 30
        ReqCreatureOrGOId3,  # 31
        ReqCreatureOrGOId4,  # 32
        ReqSpellCast1,  # 33
        ReqSpellCast2,  # 34
        ReqSpellCast3,  # 35
        ReqSpellCast4,  # 36
        PointMapId,  # 37
        PointX,  # 38
        PointY,  # 39
        StartScript,  # 40
        CompleteScript,  # 41
        SrcItemId,  # 42
        ZoneOrSort,  # 43
        Method,  # 44
        ObjectiveText1,  # 45
        ObjectiveText2,  # 46
        ObjectiveText3,  # 47
        ObjectiveText4,  # 48
        EndText,  # 49
        Details,  # 50
        SpecialFlags,  # 51
        0 as BreadcrumbForQuestId, # 52
        RewRepFaction1,  # 53
        RewRepFaction2,  # 54
        RewRepFaction3,  # 55
        RewRepFaction4,  # 56
        RewRepFaction5,  # 57
        RewRepValue1,  # 58
        RewRepValue2,  # 59
        RewRepValue3,  # 60
        RewRepValue4,  # 61
        RewRepValue5  # 62
    
        FROM quest_template
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
    return {
        'quest_template': quest_template,
        'creature_killcredit': creature_killcredit,
        'creature_involvedrelation': creature_involvedrelation,
        'gameobject_involvedrelation': gameobject_involvedrelation,
        'creature_questrelation': creature_questrelation,
        'gameobject_questrelation': gameobject_questrelation,
        'item_questrelation': item_questrelation,
        'areatrigger_involvedrelation': areatrigger_involvedrelation,
        'locales_quest': loc_quests
    }
