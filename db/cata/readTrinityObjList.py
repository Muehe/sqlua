def read_trinity_obj_list(cursor):
    print("Selecting object related MySQL tables...")
    print("  SELECT gameobject_template")
    # TODO: faction is unused in Questie
    cursor.execute("SELECT entry, name, type, 0 as faction, data1 FROM gameobject_template")
    obj_tpl = []
    for a in cursor.fetchall():
        obj_tpl.append(a)

    print(" SELECT gameobject")
    cursor.execute("SELECT id, map, position_x, position_y, guid, PhaseId FROM gameobject WHERE PhaseId <= 670")
    obj = {}
    for a in cursor.fetchall():
        if a[0] not in obj:
            obj[a[0]] = []
        obj[a[0]].append(a)

    print("  SELECT gameobject_queststarter")
    obj_start = {}
    cursor.execute("SELECT id, quest FROM gameobject_queststarter")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if quest not in obj_start:
            obj_start[quest] = []
        obj_start[quest].append((entry, quest))

    print("  SELECT gameobject_questender")
    obj_end = {}
    cursor.execute("SELECT id, quest FROM gameobject_questender")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if quest not in obj_end:
            obj_end[quest] = []
        obj_end[quest].append((entry, quest))

    # print("  SELECT locales_gameobject")
    # cursor.execute("SELECT * FROM locales_gameobject")
    loc_obj = {}
    # for a in cursor.fetchall():
    #     if (a[0] in loc_obj):
    #         loc_obj[a[0]].append(a)
    #     else:
    #         loc_obj[a[0]] = []
    #         loc_obj[a[0]].append(a)

    print("Done.")
    return {
        'object_template': obj_tpl,
        'object': obj,
        'object_start': obj_start,
        'object_end': obj_end,
        'locales_object': loc_obj
    }
