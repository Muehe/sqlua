def read_mangos_npc_list(cursor, dictCursor):
    print("Selecting NPC related MySQL tables...")

    print("  SELECT creature_template")
    cursor.execute("SELECT entry, name, minlevel, maxlevel, minlevelhealth, maxlevelhealth, `Rank`, FactionAlliance, SubName, NpcFlags, KillCredit1, KillCredit2 FROM creature_template")
    npc_tpl = []
    for a in cursor.fetchall():
        npc_tpl.append(a)
    print('  SELECT creature')
    cursor.execute('SELECT id, map, position_x, position_y, guid, 0 as PhaseId FROM creature')
    npc = {}
    for a in cursor.fetchall():
        if a[0] not in npc:
            npc[a[0]] = []
        npc[a[0]].append(a)

    print("  SELECT quest_relation")
    npc_start = {}
    npc_end = {}
    cursor.execute("SELECT entry, quest, role FROM quest_relations WHERE actor=0")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if a[2] == 0:
            if entry not in npc_start:
                npc_start[entry] = []
            npc_start[entry].append((entry, quest))
        elif a[2] == 1:
            if entry not in npc_end:
                npc_end[entry] = []
            npc_end[entry].append((entry, quest))

    # print("  SELECT creature_movement")
    # cursor.execute("SELECT point, id, position_x, position_y FROM creature_movement")
    npc_mov = {}
    # for a in cursor.fetchall():
    #     if(a[1] in npc_mov):
    #         npc_mov[a[1]].append(a)
    #     else:
    #         npc_mov[a[1]] = []
    #         npc_mov[a[1]].append(a)
    #
    # print("  SELECT creature_movement_template")
    # cursor.execute("SELECT point, entry, position_x, creature_movement_template.position_y, PathId FROM creature_movement_template")
    npc_mov_tpl = {}
    # for a in cursor.fetchall():
    #     if(a[1] in npc_mov_tpl):
    #         npc_mov_tpl[a[1]].append(a)
    #     else:
    #         npc_mov_tpl[a[1]] = []
    #         npc_mov_tpl[a[1]].append(a)

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
