def read_skyfire_npc_list(cursor, dictCursor):
    print("Selecting NPC related MySQL tables...")

    print("  SELECT creature_template")
    cursor.execute("SELECT entry, name, minlevel, maxlevel, 0 as minlevelhealth, 0 as maxlevelhealth, npc_rank, faction_A, SubName, npcflag, KillCredit1, KillCredit2 FROM creature_template")
    npc_tpl = []
    for a in cursor.fetchall():
        npc_tpl.append(a)

    print('  SELECT creature')
    cursor.execute('SELECT id, map, position_x, position_y, guid, PhaseId FROM creature WHERE PhaseId <= 670')
    npc = {}
    for a in cursor.fetchall():
        if a[0] not in npc:
            npc[a[0]] = []
        npc[a[0]].append(a)

    print("  SELECT creature_queststarter")
    npc_start = {}
    cursor.execute("SELECT id, quest FROM creature_queststarter")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if entry not in npc_start:
            npc_start[entry] = []
        npc_start[entry].append((entry, quest))

    print("  SELECT creature_questender")
    npc_end = {}
    cursor.execute("SELECT id, quest FROM creature_questender")
    for a in cursor.fetchall():
        entry = a[0]
        quest = a[1]
        if entry not in npc_end:
            npc_end[entry] = []
        npc_end[entry].append((entry, quest))

    npc_mov = {}
    npc_mov_tpl = {}

    print("  SELECT locales_creature")
    count = dictCursor.execute("SELECT * FROM locales_creature")
    loc_npc = {}
    for _ in range(0, count):
        q = dictCursor.fetchone()
        loc_npc[q['entry']] = q

    print("Done.")
    return {
        'npc_template':npc_tpl,
        'npc':npc,
        'npc_start':npc_start,
        'npc_end':npc_end,
        'npc_movement':npc_mov,
        'npc_movement_template':npc_mov_tpl,
        'locales_npc':loc_npc,
    }
