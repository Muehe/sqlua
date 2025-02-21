def read_mangos_obj_list(cursor):
    print("Selecting object related MySQL tables...")
    print("  SELECT gameobject_template")
    cursor.execute("SELECT entry, name, type, faction, data1 FROM gameobject_template")
    obj_tpl = []
    for a in cursor.fetchall():
        obj_tpl.append(a)

    print(" SELECT gameobject")
    cursor.execute("SELECT id, map, position_x, position_y, guid, 0 as PhaseId FROM gameobject")
    obj = {}
    for a in cursor.fetchall():
        if a[0] not in obj:
            obj[a[0]] = []
        obj[a[0]].append(a)

    print("  SELECT quest_relation")
    obj_start = {}
    obj_end = {}
    # actor 0=creature, 1=gameobject
    # entry=creature_template.entry or gameobject_template.entry
    # quest=quest_template.entry
    # role 0=start, 1=end
    cursor.execute("SELECT entry, quest, role FROM quest_relations WHERE actor=1")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if a[2] == 0:
            if entry not in obj_start:
                obj_start[entry] = []
            obj_start[entry].append((entry, quest))
        elif a[2] == 1:
            if entry not in obj_end:
                obj_end[entry] = []
            obj_end[entry].append((entry, quest))

    print("  SELECT locales_gameobject")
    cursor.execute("SELECT * FROM locales_gameobject")
    loc_obj = {}
    for a in cursor.fetchall():
        if (a[0] in loc_obj):
            loc_obj[a[0]].append(a)
        else:
            loc_obj[a[0]] = []
            loc_obj[a[0]].append(a)

    print("Done.")
    return {
        'object_template': obj_tpl,
        'object': obj,
        'object_start': obj_start,
        'object_end': obj_end,
        'locales_object': loc_obj
    }
