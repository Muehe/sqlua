def getQuestTables(cursor, dictCursor, version):
    """only used by constructor"""
    print("Selecting quest related MySQL tables...")
    print("  SELECT quest_template")
    if version not in ['classic', 'tbc']:
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
