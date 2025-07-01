def getObjTables(cursor):
    print("Selecting object related MySQL tables...")
    print("  SELECT gameobject_template")
    cursor.execute("SELECT entry, name, type, faction, data1 FROM gameobject_template")
    obj_tpl = []
    for a in cursor.fetchall():
        obj_tpl.append(a)

    print('  SELECT gameobject_spawn_entry')
    cursor.execute('SELECT * FROM gameobject_spawn_entry')
    obj_spawn_entry = {}
    for guid, entry in cursor.fetchall():
        if guid not in obj_spawn_entry:
            obj_spawn_entry[guid] = []
        obj_spawn_entry[guid].append(entry)

    print("  SELECT gameobject")
    cursor.execute("SELECT id, map, position_x, position_y, guid FROM gameobject")
    obj = {}
    for a in cursor.fetchall():
        if (a[0] == 0):
            if a[4] in obj_spawn_entry:
                for entry in obj_spawn_entry[a[4]]:
                    if entry not in obj:
                        obj[entry] = []
                    obj[entry].append(a)
            #else:
                #print(f'Missing entry for GUID {a[4]}')
            continue
        elif(a[0] not in obj):
            obj[a[0]] = []
        obj[a[0]].append(a)

    print("  SELECT gameobject_questrelation")
    cursor.execute("SELECT * FROM gameobject_questrelation")
    obj_start = {}
    for a in cursor.fetchall():
        if(a[0] in obj_start):
            obj_start[a[0]].append(a)
        else:
            obj_start[a[0]] = []
            obj_start[a[0]].append(a)

    print("  SELECT gameobject_involvedrelation")
    cursor.execute("SELECT * FROM gameobject_involvedrelation")
    obj_end = {}
    for a in cursor.fetchall():
        if(a[0] in obj_end):
            obj_end[a[0]].append(a)
        else:
            obj_end[a[0]] = []
            obj_end[a[0]].append(a)

    print("  SELECT locales_gameobject")
    cursor.execute("SELECT * FROM locales_gameobject")
    loc_obj = {}
    for a in cursor.fetchall():
        if(a[0] in loc_obj):
            loc_obj[a[0]].append(a)
        else:
            loc_obj[a[0]] = []
            loc_obj[a[0]].append(a)

    print("Done.")
    return {'object_template':obj_tpl,
            'object':obj,
            'object_start':obj_start,
            'object_end':obj_end,
            'locales_object':loc_obj}
