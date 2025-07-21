def getNpcTables(cursor, dictCursor):
    print("Selecting NPC related MySQL tables...")

    print("  SELECT creature_template")
    cursor.execute("SELECT entry, name, minlevel, maxlevel, minlevelhealth, maxlevelhealth, rank, Faction, SubName, NpcFlags, KillCredit1, KillCredit2 FROM creature_template")
    npc_tpl = []
    for a in cursor.fetchall():
        npc_tpl.append(a)

    print('  SELECT creature_spawn_entry')
    cursor.execute('SELECT * FROM creature_spawn_entry')
    npc_spawn_entry = {}
    for guid, entry in cursor.fetchall():
        if guid not in npc_spawn_entry:
            npc_spawn_entry[guid] = []
        npc_spawn_entry[guid].append(entry)

    print("  SELECT creature")
    cursor.execute("SELECT id, map, position_x, position_y, guid FROM creature")
    npc = {}
    for a in cursor.fetchall():
        if (a[0] == 0):
            if a[4] in npc_spawn_entry:
                for entry in npc_spawn_entry[a[4]]:
                    if entry not in npc:
                        npc[entry] = []
                    npc[entry].append(a)
            #else:
                #print(f'Missing entry for GUID {a[4]}')
            continue
        elif(a[0] not in npc):
            npc[a[0]] = []
        npc[a[0]].append(a)

    print("  SELECT spawn_group")
    cursor.execute("""
        SELECT sge.entry, s.map, s.position_x, s.position_y, s.guid
        FROM spawn_group_entry AS sge
        INNER JOIN spawn_group AS sg
        ON (sg.id = sge.id AND sg.Type = 0)
        INNER JOIN spawn_group_spawn AS sgs
        ON sge.id = sgs.id
        INNER JOIN creature as s
        ON sgs.guid = s.guid;
    """)
    for a in cursor.fetchall():
        if a[0] not in npc:
            npc[a[0]] = [a]
        else:
            npc[a[0]].append(a)

    print("  SELECT creature_questrelation")
    cursor.execute("SELECT * FROM creature_questrelation")
    npc_start = {}
    for a in cursor.fetchall():
        if(a[0] in npc_start):
            npc_start[a[0]].append(a)
        else:
            npc_start[a[0]] = []
            npc_start[a[0]].append(a)

    print("  SELECT creature_involvedrelation")
    cursor.execute("SELECT * FROM creature_involvedrelation")
    npc_end = {}
    for a in cursor.fetchall():
        if(a[0] in npc_end):
            npc_end[a[0]].append(a)
        else:
            npc_end[a[0]] = []
            npc_end[a[0]].append(a)

    print("  SELECT creature_movement")
    cursor.execute("SELECT point, id, PositionX, PositionY FROM creature_movement")
    npc_mov = {}
    for a in cursor.fetchall():
        if(a[1] in npc_mov):
            npc_mov[a[1]].append(a)
        else:
            npc_mov[a[1]] = []
            npc_mov[a[1]].append(a)

    print("  SELECT creature_movement_template")
    cursor.execute("SELECT point, entry, PositionX, PositionY, PathId FROM creature_movement_template")
    npc_mov_tpl = {}
    for a in cursor.fetchall():
        if(a[1] in npc_mov_tpl):
            npc_mov_tpl[a[1]].append(a)
        else:
            npc_mov_tpl[a[1]] = []
            npc_mov_tpl[a[1]].append(a)

    print("  SELECT locales_creature")
    count = dictCursor.execute("SELECT * FROM locales_creature")
    loc_npc = {}
    for _ in range(0, count):
        q = dictCursor.fetchone()
        loc_npc[q['entry']] = q

    print("Done.")
    return {'npc_template':npc_tpl,
            'npc':npc,
            'npc_start':npc_start,
            'npc_end':npc_end,
            'npc_movement':npc_mov,
            'npc_movement_template':npc_mov_tpl,
            'locales_npc':loc_npc,
            }
