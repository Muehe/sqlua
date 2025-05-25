def read_trinity_npc_list(cursor, dictCursor, npc_ids = None):
    npc_ids_for_where_clause = ', '.join(map(str, npc_ids)) if npc_ids else ''
    print("Selecting NPC related MySQL tables...")

    print("  SELECT creature_template")
    # FactionAlliance and FactionHorde seem to contain the same data
    # TODO: Rank is coming from Classification
    cursor.execute(f"SELECT entry, name, 0 as MinLevel, 0 as MaxLevel, 0 as MinLevelHealth, 0 as MaxLevelHealth, 0 as `Rank`, faction, subname, npcflag, KillCredit1, KillCredit2 FROM creature_template {('WHERE entry IN (' + npc_ids_for_where_clause + ')') if npc_ids else 'WHERE entry != 211770'}")
    npc_tpl = []
    for a in cursor.fetchall():
        npc_tpl.append(a)

    print('  SELECT creature')
    cursor.execute(f"SELECT id, map, position_x, position_y, guid, PhaseId FROM creature {('WHERE id IN (' + npc_ids_for_where_clause + ')') if npc_ids else 'WHERE PhaseId <= 670'}")
    npc = {}
    for a in cursor.fetchall():
        if a[0] not in npc:
            npc[a[0]] = []
        npc[a[0]].append(a)

    print("  SELECT creature_queststarter")
    npc_start = {}
    cursor.execute(f"SELECT id, quest FROM creature_queststarter {('WHERE id IN (' + npc_ids_for_where_clause + ')') if npc_ids else ''}")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if entry not in npc_start:
            npc_start[entry] = []
        npc_start[entry].append((entry, quest))

    print("  SELECT creature_questender")
    npc_end = {}
    cursor.execute(f"SELECT id, quest FROM creature_questender {('WHERE id IN (' + npc_ids_for_where_clause + ')') if npc_ids else ''}")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if entry not in npc_end:
            npc_end[entry] = []
        npc_end[entry].append((entry, quest))

    # print("  SELECT creature_movement")
    # cursor.execute("SELECT point, id, position_x, position_y FROM creature_movement")
    npc_mov = {}
    # for a in cursor.fetchall():
    #     if (a[1] in npc_mov):
    #         npc_mov[a[1]].append(a)
    #     else:
    #         npc_mov[a[1]] = []
    #         npc_mov[a[1]].append(a)
    #
    # print("  SELECT creature_movement_template")
    # cursor.execute("SELECT point, entry, position_x, position_y, wpguid FROM creature_movement_template")
    npc_mov_tpl = {}
    # for a in cursor.fetchall():
    #     if (a[1] in npc_mov_tpl):
    #         npc_mov_tpl[a[1]].append(a)
    #     else:
    #         npc_mov_tpl[a[1]] = []
    #         npc_mov_tpl[a[1]].append(a)
    #
    # print("  SELECT locales_creature")
    # count = dictCursor.execute("SELECT * FROM locales_creature")
    loc_npc = {}
    # for _ in range(0, count):
    #     q = dictCursor.fetchone()
    #     loc_npc[q['entry']] = q

    print("Done.")
    return {
        'npc_template': npc_tpl,
        'npc': npc,
        'npc_start': npc_start,
        'npc_end': npc_end,
        'npc_movement': npc_mov,
        'npc_movement_template': npc_mov_tpl,
        'locales_npc': loc_npc,
    }
