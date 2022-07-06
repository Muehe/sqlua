from db.CoordData import *

def printCoordFiles(cursor, version):
    # creatures
    cursor.execute("SELECT id, map, position_x, position_y, position_z, guid FROM creature")
    npc = {}
    ## sort by guid
    for a in cursor.fetchall():
        npc[a[5]] = a
    fileName = f"preExtract/{version}/creature_preExtract.csv"
    outfile = open(fileName, "w")
    for guid in npc: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(npc[guid][1])+","+str(npc[guid][2])+","+str(npc[guid][3])+","+str(npc[guid][4])+",\n")
    outfile.close()

    # creature_movement
    cursor.execute("SELECT point, id, PositionX, PositionY, PositionZ FROM creature_movement")
    npc_mov = {}
    ## sort by guid#point
    for a in cursor.fetchall():
        npc_mov[str(a[1])+"#"+str(a[0])] = a
    fileName = f"preExtract/{version}/creature_movement_preExtract.csv"
    outfile = open(fileName, "w")
    for guid in npc_mov: # (guid, map, x, y, z)
        if npc_mov[guid][1] in npc:
            outfile.write(guid+","+str(npc[npc_mov[guid][1]][1])+","+str(npc_mov[guid][2])+","+str(npc_mov[guid][3])+","+str(npc_mov[guid][4])+",\n")
        else:
            print("No spawn for creature_movement with guid "+str(guid)+". Skipped!")
    outfile.close()

    # creature_movement_template
    ## sort npcs by ID for map lookup
    npcById = {}
    for guid in npc:
        if npc[guid][0] not in npcById:
            npcById[npc[guid][0]] = npc[guid]
    ## TODO: figure out a way to get the map for every creature, there are about 10 who don't have one
    ## get template waypoints
    cursor.execute("SELECT point, entry, PositionX, PositionY, PositionZ, PathId FROM creature_movement_template")
    npc_mov_tpl = []
    for a in cursor.fetchall():
        npc_mov_tpl.append(a)
    fileName = f"preExtract/{version}/creature_movement_template_preExtract.csv"
    outfile = open(fileName, "w")
    for point in npc_mov_tpl: # (point#id, map, x, y, z)
        if point[1] in npcById:
            outfile.write(str(point[1])+"#"+str(point[0])+"#"+str(point[5])+","+str(npcById[point[1]][1])+","+str(point[2])+","+str(point[3])+","+str(point[4])+",\n")
        else:
            print("No spawn for creature_movement_template with id "+str(point[1])+" point "+str(point[0])+". Skipped!")
    outfile.close()

    # gameobjects
    cursor.execute("SELECT id, map, position_x, position_y, position_z, guid FROM gameobject")
    obj = {}
    ## sort by guid
    for a in cursor.fetchall():
        obj[a[5]] = a
    fileName = f"preExtract/{version}/gameobject_preExtract.csv"
    outfile = open(fileName, "w")
    for guid in obj: # (guid, map, x, y, z)
        outfile.write(str(guid)+","+str(obj[guid][1])+","+str(obj[guid][2])+","+str(obj[guid][3])+","+str(obj[guid][4])+",\n")
    outfile.close()

    # areaTriggers
    areaTriggers = getAreaTriggers(version)
    fileName = f"preExtract/{version}/areaTrigger_preExtract.csv"
    with open(fileName, 'w') as outfile:
        for trigger in areaTriggers:
            outfile.write(str(trigger[0])+','+str(trigger[1])+','+str(trigger[2])+','+str(trigger[3])+','+str(trigger[4])+",\n")
        outfile.close()
