def printCoordFiles(cursor):
    cursor.execute("SELECT id, map, position_x, position_y, position_z, guid FROM creature")
    npc = {}
    for a in cursor.fetchall():
        npc[a[5]] = a
    fileName = "sqlua/creature_coords.csv"
    outfile = open(fileName, "w")
    for guid in npc: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(npc[guid][1])+","+str(npc[guid][2])+","+str(npc[guid][3])+","+str(npc[guid][4])+",\n")
    outfile.close()
    cursor.execute("SELECT point, id, position_x, position_y, position_z FROM creature_movement")
    npc_mov = {}
    for a in cursor.fetchall():
        npc_mov[a[1]] = a
    fileName = "sqlua/creature_movement_coords.csv"
    outfile = open(fileName, "w")
    for guid in npc_mov: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(npc_mov[guid][3])+","+str(npc[guid][2])+","+str(npc_mov[guid][3])+","+str(npc_mov[guid][4])+",\n")
    outfile.close()
    cursor.execute("SELECT id, map, position_x, position_y, position_z, guid FROM gameobject")
    obj = {}
    for a in cursor.fetchall():
        obj[a[5]] = a
    fileName = "sqlua/gameobject_coords.csv"
    outfile = open(fileName, "w")
    for guid in obj: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(obj[guid][1])+","+str(obj[guid][2])+","+str(obj[guid][3])+","+str(obj[guid][4])+",\n")
    outfile.close()
    cursor.execute("SELECT point, entry, position_x, position_y, position_z FROM creature_movement_template")
    npc_mov_tpl = []
    for a in cursor.fetchall():
        npc_mov_tpl.append(a)
    npcById = {}
    for guid in npc:
        if npc[guid][0] not in npcById:
            npcById[npc[guid][0]] = npc[guid]
    fileName = "sqlua/creature_movement_template_coords.csv"
    outfile = open(fileName, "w")
    for point in npc_mov_tpl: # (id, map, x, y, z)
        if point[1] in npcById:
            outfile.write(str(point[1])+","+str(npcById[point[1]][1])+","+str(point[2])+","+str(point[3])+","+str(point[4])+",\n")
        else:
            print("No spawn for creature_movement_template with id "+str(point[1])+" point "+str(point[0]))
    outfile.close()

    return
