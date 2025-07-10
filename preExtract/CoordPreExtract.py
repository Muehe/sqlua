from db.CoordData import *

def printCoordFiles(cursor, version, flavor):
    log = open(f'preExtract/{version}/{flavor}/preExtract.log', 'w')
    # creatures
    cursor.execute("SELECT id, map, position_x, position_y, position_z, guid FROM creature")
    npc = {}
    ## sort by guid
    for a in cursor.fetchall():
        npc[a[5]] = a
    fileName = f"preExtract/{version}/{flavor}/creature_preExtract.csv"
    outfile = open(fileName, "w")
    for guid in npc: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(npc[guid][1])+","+str(npc[guid][2])+","+str(npc[guid][3])+","+str(npc[guid][4])+",\n")
    outfile.close()


    ## sort npcs by ID for map lookup
    npcById = {}
    for guid in npc:
        if npc[guid][0] not in npcById:
            npcById[npc[guid][0]] = npc[guid]

    if flavor in ['mangos', 'cmangos']:
        # creature_movement
        if flavor == "mangos":
            cursor.execute("SELECT point, id, position_x, position_y, position_z FROM creature_movement")
        else: # cmangos
            cursor.execute("SELECT point, id, PositionX, PositionY, PositionZ FROM creature_movement")
        npc_mov = {}
        ## sort by guid#point
        for a in cursor.fetchall():
            npc_mov[str(a[1])+"#"+str(a[0])] = a
        fileName = f"preExtract/{version}/{flavor}/creature_movement_preExtract.csv"
        outfile = open(fileName, "w")
        for guid in npc_mov: # (guid#point, map, x, y, z)
            if npc_mov[guid][1] in npc:
                outfile.write(guid+","+str(npc[npc_mov[guid][1]][1])+","+str(npc_mov[guid][2])+","+str(npc_mov[guid][3])+","+str(npc_mov[guid][4])+",\n")
            else:
                print("No spawn for creature_movement with guid "+str(guid)+". Skipped!", file=log)
        outfile.close()

        # creature_movement_template
        ## TODO: figure out a way to get the map for every creature, there are about 10 who don't have one
        ## get template waypoints
        if flavor == "mangos":
            cursor.execute("SELECT point, entry, position_x, position_y, position_z, wpguid FROM creature_movement_template")
        else: #cmangos
            cursor.execute("SELECT point, entry, PositionX, PositionY, PositionZ, PathId FROM creature_movement_template")
        npc_mov_tpl = []
        for a in cursor.fetchall():
            npc_mov_tpl.append(a)
        fileName = f"preExtract/{version}/{flavor}/creature_movement_template_preExtract.csv"
        outfile = open(fileName, "w")
        for point in npc_mov_tpl: # (id#pointid#pathid, map, x, y, z)
            if point[1] in npcById:
                outfile.write(str(point[1])+"#"+str(point[0])+"#"+str(point[5])+","+str(npcById[point[1]][1])+","+str(point[2])+","+str(point[3])+","+str(point[4])+",\n")
            else:
                print("No spawn for creature_movement_template with id "+str(point[1])+" point "+str(point[0])+". Skipped!", file=log)
        outfile.close()
    elif flavor in ['trinity', 'skyfire']:
        if flavor == 'trinity':
            cursor.execute("""
                SELECT c.guid, ca.PathId, wa.NodeId, c.map, wa.PositionX, wa.PositionY, wa.PositionZ
                FROM creature_addon as ca
                INNER JOIN creature as c ON c.guid = ca.guid
                INNER JOIN waypoint_path_node as wa ON wa.PathId = ca.PathId
                WHERE ca.PathId != 0;
            """)
        else: # skyfire
            cursor.execute("""
                SELECT c.guid, ca.path_id, wa.point, c.map, wa.position_x, wa.position_y, wa.position_z
                FROM creature_addon as ca
                INNER JOIN creature as c ON c.guid = ca.guid
                INNER JOIN waypoint_data as wa ON wa.id = ca.path_id
                WHERE ca.path_id != 0;
            """)
        npc_mov = []
        check = {}
        for a in cursor.fetchall():
            if str(a[0])+str(a[2]) in check:
                continue
            else:
                npc_mov.append(a)
                check[str(a[0])+str(a[2])] = True
        fileName = f"preExtract/{version}/{flavor}/creature_movement_preExtract.csv"
        outfile = open(fileName, "w")
        for l in npc_mov:
            if None not in l:
                outfile.write(str(l[0])+"#"+str(l[2])+","+str(l[3])+","+str(l[4])+","+str(l[5])+","+str(l[6])+",\n")
        if flavor == 'trinity':
            cursor.execute("""
                SELECT ca.entry, ca.PathId, wa.NodeId, c.map, wa.PositionX, wa.PositionY, wa.PositionZ
                FROM creature_template_addon as ca
                INNER JOIN creature as c ON c.id = ca.entry
                INNER JOIN waypoint_path_node as wa ON wa.PathId = ca.PathId
                WHERE ca.PathId != 0;
            """)
        else: # skyfire
            cursor.execute("""
                SELECT ca.entry, ca.path_id, wa.point, c.map, wa.position_x, wa.position_y, wa.position_z
                FROM creature_template_addon as ca
                INNER JOIN creature as c ON c.id = ca.entry
                INNER JOIN waypoint_data as wa ON wa.id = ca.path_id
                WHERE ca.path_id != 0;
            """)
        outfile.close()
        npc_mov_tpl = []
        check = {}
        for a in cursor.fetchall():
            if str(a[0])+str(a[2])+str(a[1]) in check:
                continue
            else:
                npc_mov_tpl.append(a)
                check[str(a[0])+str(a[2])+str(a[1])] = True
        fileName = f"preExtract/{version}/{flavor}/creature_movement_template_preExtract.csv"
        outfile = open(fileName, "w")
        for l in npc_mov_tpl:
            if None not in l:
                outfile.write(f"{l[0]}#{l[2]}#{l[1]},{l[3]},{l[4]},{l[5]},{l[6]},\n")
        outfile.close()

    # gameobjects
    cursor.execute("SELECT id, map, position_x, position_y, position_z, guid FROM gameobject")
    obj = {}
    ## sort by guid
    for a in cursor.fetchall():
        obj[a[5]] = a
    fileName = f"preExtract/{version}/{flavor}/gameobject_preExtract.csv"
    outfile = open(fileName, "w")
    for guid in obj: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(obj[guid][1])+","+str(obj[guid][2])+","+str(obj[guid][3])+","+str(obj[guid][4])+",\n")
    outfile.close()

    # areaTriggers
    areaTriggers = getAreaTriggers(version)
    fileName = f"preExtract/{version}/{flavor}/areaTrigger_preExtract.csv"
    with open(fileName, 'w') as outfile:
        for trigger in areaTriggers:
            outfile.write(str(trigger[0])+','+str(trigger[1])+','+str(trigger[2])+','+str(trigger[3])+','+str(trigger[4])+",\n")
        outfile.close()
    f.close()
