"""


######################################
Misc functions
######################################


"""

def escapeName(string):
    name = string.replace('"', '\\"')
    name2 = name.replace("'", "\\'")
    return name2

def doIt(cursor):
    npc_tpl, npc, npc_start, npc_end, npc_mov = getNPCTables(cursor)
    npcs = sortedNpcs(npc_tpl, npc, npc_start, npc_end, npc_mov)
    return npcs

"""


######################################
Data Definitions
######################################


"""

mapBorders = [('1', 'Dun Morogh', '0', '1802.08325195313', '-3122.91650390625', '-3877.08325195313', '-7160.41650390625'),
              ('3', 'Badlands', '0', '-2079.16650390625', '-4566.66650390625', '-5889.5830078125', '-7547.91650390625'),
              ('4', 'Blasted Lands', '0', '-1241.66662597656', '-4591.66650390625', '-10566.666015625', '-12800'),
              ('8', 'Swamp of Sorrows', '0', '-2222.91650390625', '-4516.66650390625', '-9620.8330078125', '-11150'),
              ('10', 'Duskwood', '0', '833.333312988281', '-1866.66662597656', '-9716.666015625', '-11516.666015625'),
              ('11', 'Wetlands', '0', '-389.583312988281', '-4525', '-2147.91650390625', '-4904.16650390625'),
              ('12', 'Elwynn Forest', '0', '1535.41662597656', '-1935.41662597656', '-7939.5830078125', '-10254.166015625'),
              ('28', 'Western Plaguelands', '0', '416.666656494141', '-3883.33325195313', '3366.66650390625', '499.999969482422'),
              ('33', 'Stranglethorn Vale', '0', '2220.83325195313', '-4160.41650390625', '-11168.75', '-15422.916015625'),
              ('36', 'Alterac Mountains', '0', '783.333312988281', '-2016.66662597656', '1500', '-366.666656494141'),
              ('38', 'Loch Modan', '0', '-1993.74987792969', '-4752.0830078125', '-4487.5', '-6327.0830078125'),
              ('40', 'Westfall', '0', '3016.66650390625', '-483.333312988281', '-9400', '-11733.3330078125'),
              ('41', 'Deadwind Pass', '0', '-833.333312988281', '-3333.33325195313', '-9866.666015625', '-11533.3330078125'),
              ('44', 'Redridge Mountains', '0', '-1570.83325195313', '-3741.66650390625', '-8575', '-10022.916015625'),
              ('45', 'Arathi Highlands', '0', '-866.666625976563', '-4466.66650390625', '-133.33332824707', '-2533.33325195313'),
              ('46', 'Burning Steppes', '0', '-266.666656494141', '-3195.83325195313', '-7031.24951171875', '-8983.3330078125'),
              ('47', 'The Hinterlands', '0', '-1575', '-5425', '1466.66662597656', '-1100'),
              ('51', 'Searing Gorge', '0', '-322.916656494141', '-2554.16650390625', '-6100', '-7587.49951171875'),
              ('85', 'Tirisfal Glades', '0', '3033.33325195313', '-1485.41662597656', '3837.49975585938', '824.999938964844'),
              ('130', 'Silverpine Forest', '0', '3449.99975585938', '-750', '1666.66662597656', '-1133.33325195313'),
              ('139', 'Eastern Plaguelands', '0', '-2185.41650390625', '-6056.25', '3799.99975585938', '1218.75'),
              ('267', 'Hillsbrad Foothills', '0', '1066.66662597656', '-2133.33325195313', '400', '-1733.33325195313'),
              ('1497', 'Undercity', '0', '873.192626953125', '-86.1824035644531', '1877.9453125', '1237.84118652344'),
              ('1519', 'Stormwind City', '0', '1380.97143554688', '36.7006301879883', '-8278.8505859375', '-9175.205078125'),
              ('1537', 'Ironforge', '0', '-713.591369628906', '-1504.21643066406', '-4569.2412109375', '-5096.845703125'),
              ('14', 'Durotar', '1', '-1962.49987792969', '-7249.99951171875', '1808.33325195313', '-1716.66662597656'),
              ('15', 'Dustwallow Marsh', '1', '-974.999938964844', '-6225', '-2033.33325195313', '-5533.3330078125'),
              ('16', 'Azshara', '1', '-3277.08325195313', '-8347.916015625', '5341.66650390625', '1960.41662597656'),
              ('17', 'The Barrens', '1', '2622.91650390625', '-7510.41650390625', '1612.49987792969', '-5143.75'),
              ('141', 'Teldrassil', '1', '3814.58325195313', '-1277.08325195313', '11831.25', '8437.5'),
              ('148', 'Darkshore', '1', '2941.66650390625', '-3608.33325195313', '8333.3330078125', '3966.66650390625'),
              ('215', 'Mulgore', '1', '2047.91662597656', '-3089.58325195313', '-272.916656494141', '-3697.91650390625'),
              ('331', 'Ashenvale', '1', '1699.99987792969', '-4066.66650390625', '4672.91650390625', '829.166625976563'),
              ('357', 'Feralas', '1', '5441.66650390625', '-1508.33325195313', '-2366.66650390625', '-6999.99951171875'),
              ('361', 'Felwood', '1', '1641.66662597656', '-4108.3330078125', '7133.3330078125', '3299.99975585938'),
              ('400', 'Thousand Needles', '1', '-433.333312988281', '-4833.3330078125', '-3966.66650390625', '-6899.99951171875'),
              ('405', 'Desolace', '1', '4233.3330078125', '-262.5', '452.083312988281', '-2545.83325195313'),
              ('406', 'Stonetalon Mountains', '1', '3245.83325195313', '-1637.49987792969', '2916.66650390625', '-339.583312988281'),
              ('440', 'Tanaris', '1', '-218.749984741211', '-7118.74951171875', '-5875', '-10475'),
              ('490', "Un'Goro Crater", '1', '533.333312988281', '-3166.66650390625', '-5966.66650390625', '-8433.3330078125'),
              ('493', 'Moonglade', '1', '-1381.25', '-3689.58325195313', '8491.666015625', '6952.0830078125'),
              ('618', 'Winterspring', '1', '-316.666656494141', '-7416.66650390625', '8533.3330078125', '3799.99975585938'),
              ('1377', 'Silithus', '1', '2537.5', '-945.833984375', '-5958.333984375', '-8281.25'),
              ('1637', 'Orgrimmar', '1', '-3680.60107421875', '-5083.20556640625', '2273.87719726563', '1338.46057128906'),
              ('1638', 'Thunder Bluff', '1', '516.666625976563', '-527.083312988281', '-849.999938964844', '-1545.83325195313'),
              ('1657', 'Darnassus', '1', '2938.36279296875', '1880.02954101563', '10238.31640625', '9532.5869140625')]
instanceIds = [('209', 'Shadowfang Keep', '33'),
               ('491', 'Razorfen Kraul', '47'),
               ('717', 'Stormwind Stockade', '34'),
               ('718', 'Wailing Caverns', '43'),
               ('719', 'Blackfathom Deeps', '48'),
               ('721', 'Gnomeregan', '90'),
               ('722', 'Razorfen Downs', '129'),
               ('796', 'Scarlet Monastery', '189'),
               ('1176', "Zul'Farrak", '209'),
               ('1337', 'Uldaman', '70'),
               ('1477', 'Sunken Temple', '109'),
               ('1581', 'The Deadmines', '36'),
               ('1583', 'Blackrock Spire', '229'),
               ('1585', 'Blackrock Depths', '230'),
               ('1977', "Zul'Gurub", '309'),
               ('2017', 'Stratholme', '329'),
               ('2057', 'Scholomance', '289'),
               ('2100', 'Maraudon', '349'),
               ('2159', "Onyxia's Lair", '249'),
               ('2257', 'Deeprun Tram', '369'),
               ('2437', 'Ragefire Chasm', '389'),
               ('2557', 'Dire Maul', '429'),
               ('2677', 'Blackwing Lair', '469'),
               ('2717', 'Molten Core', '409'),
               ('3428', "Ahn'Qiraj", '531'),
               ('3429', "Ruins of Ahn'Qiraj", '509'),
               ('3456', 'Naxxramas', '533'),
               ('2917', 'Horde PVP Barracks', '450'),
               ('2918', 'Alliance PVP Barracks', '449'),
               ('2597', 'Alterac Valley', '30'),
               ('3277', 'Warsong Gulch', '489'),
               ('3358', 'Arathi Basin', '529')
               #('209', 'Shadowfang Keep', '33', '4500', '300', '1133.333', '-1666.667'),
               #('491', 'Razorfen Kraul', '47', '2766.667', '966.6666', '2733.333', '1533.333'),
               #('722', 'Razorfen Downs', '129', '2766.667', '-633.3333', '3266.667', '999.9999'),
               #('796', 'Scarlet Monastery', '189', '1508.333', '-800', '1918.75', '379.166'),
               #('1176', "Zul'Farrak", '209', '1625', '241.6667', '2052.083', '1129.167'),
               #('1581', 'The Deadmines', '36', '1966.667', '-3033.333', '1133.333', '-2200'),
               #('1977', "Zul'Gurub", '309', '-693.75', '-2570.833', '-11308.33', '-12560.42'),
               #('2017', 'Stratholme', '329', '-1766.667', '-5166.667', '4333.333', '2066.667'),
               #('2057', 'Scholomance', '289', '633.3333', '-1166.667', '600', '-600'),
               #('2597', 'Alterac Valley', '30', '1781.24987792969', '-2456.25', '1085.41662597656', '-1739.58325195313'),
               #('2677', 'Blackwing Lair', '469', '633.3333', '-2766.667', '-6333.333', '-8600'),
               #('3277', 'Warsong Gulch', '489', '2041.66662597656', '895.833312988281', '1627.08325195313', '862.499938964844'),
               #('3358', 'Arathi Basin', '529', '1858.33325195313', '102.08332824707', '1508.33325195313', '337.5'),
               #('3428', "Ahn'Qiraj", '531', '3033.333', '1233.333', '-7933.333', '-9133.333'),
               #('3429', "Ruins of Ahn'Qiraj", '509', '3035.417', '522.9166', '-8233.333', '-9908.333')
               ]
continentBorders = [('5', 'Eastern Kingdoms', '0', '16000', '-19199.900390625', '7466.60009765625', '-16000'),
                    ('6', 'Kalimdor', '1', '17066.599609375', '-19733.2109375', '12799.900390625', '-11733.2998046875')]

validZoneList = [1, 3, 4, 8, 10, 11, 12, 14, 15, 16, 17, 28, 33, 36, 38, 40, 41, 44, 45, 46, 47, 51, 85, 130, 139, 141, 148, 215, 267, 331, 357, 361, 400, 405, 406, 440, 490, 493, 618, 1377, 1497, 1519, 1537, 1637, 1638, 1657]
zoneLevelList = [(1, 1, 10),
                 (3, 35, 45),
                 (4, 45, 55),
                 (8, 35, 45),
                 (10, 18, 30),
                 (11, 20, 30),
                 (12, 1, 10),
                 (14, 1, 10),
                 (15, 35, 45),
                 (16, 45, 55),
                 (17, 10, 25),
                 (28, 51, 58),
                 (33, 30, 45),
                 (36, 30, 40),
                 (38, 10, 20),
                 (40, 10, 20),
                 (41, 55, 60),
                 (44, 15, 25),
                 (45, 30, 40),
                 (46, 50, 58),
                 (47, 40, 50),
                 (51, 45, 50),
                 (85, 1, 10),
                 (130, 10, 20),
                 (139, 53, 60),
                 (141, 1, 10),
                 (148, 10, 20),
                 (215, 1, 10),
                 (267, 20, 30),
                 (331, 18, 30),
                 (357, 40, 50),
                 (361, 48, 55),
                 (400, 25, 35),
                 (405, 30, 40),
                 (406, 15, 27),
                 (440, 40, 50),
                 (490, 48, 55),
                 (493, 55, 60),
                 (618, 53, 60),
                 (1377, 55, 60),
                 (1497, 1, 60),
                 (1519, 1, 60),
                 (1537, 1, 60),
                 (1637, 1, 60),
                 (1638, 1, 60),
                 (1657, 1, 60)]

"""


######################################
NPC functions
######################################


"""

def calculateCoords(mapId, x, y):
    zones=[]
    for mapSet in mapBorders:
        zone = int(mapSet[0])
        mId = int(mapSet[2])
        x1 = float(mapSet[5])
        x2 = float(mapSet[6])
        y1 = float(mapSet[3])
        y2 = float(mapSet[4])
        if (mapId == mId) and (x < x1) and (x > x2) and (y < y1) and (y > y2):
            xCoord = round(abs((x-x1)/(x2-x1)*100), 2)
            yCoord = round(abs((y-y1)/(y2-y1)*100), 2)
            z = [zone, yCoord, xCoord]
            zones.append(z)

    for instance in instanceIds:
        zoneId = int(instance[0])
        mapID = int(instance[2])
        if (mapId == mapID):
            z = [zoneId, -1, -1]
            zones.append(z)
    """
    for continent in continentBorders:
        cId = int(continent[2])
        if (mapId == cId):
            zone = int(continent[0])
            x1 = float(continent[5])
            x2 = float(continent[6])
            y1 = float(continent[3])
            y2 = float(continent[4])
            xCoord = round(abs((x-x1)/(x2-x1)*100), 2)
            yCoord = round(abs((y-y1)/(y2-y1)*100), 2)
            z = [zone, yCoord, xCoord]
            zones.append(z)
    """
    if zones != []:
        return zones
    else:
        return False

def getNPCTables(cursor):
    print("Selecting MySQL tables...")
    cursor.execute("SELECT entry, name, minlevel, maxlevel, minlevelhealth, maxlevelhealth, rank FROM creature_template")
    npc_tpl = []
    for a in cursor.fetchall():
        npc_tpl.append(a)
    cursor.execute("SELECT id, map, position_x, position_y, guid FROM creature")
    npc = []
    for a in cursor.fetchall():
        npc.append(a)
    cursor.execute("SELECT * FROM creature_questrelation")
    npc_start = []
    for a in cursor.fetchall():
        npc_start.append(a)
    cursor.execute("SELECT * FROM creature_involvedrelation")
    npc_end = []
    for a in cursor.fetchall():
        npc_end.append(a)
    cursor.execute("SELECT point, id, position_x, position_y FROM creature_movement")
    npc_mov = []
    for a in cursor.fetchall():
        npc_mov.append(a)
    """
    cursor.execute("SELECT point, entry, position_x, position_y FROM creature_movement_template")
    npc_mov_tpl = []
    for a in cursor.fetchall():
        npc_mov_tpl.append(a)
    """

    return npc_tpl, npc, npc_start, npc_end, npc_mov

def sortedNpcs(npc_tpl, npc, npc_start, npc_end, npc_mov):
    alle = []
    for entries in npc_tpl:
        """
        if entries[0] > 715:
            break
        elif entries[0] < 234:
            continue
        """
        temp = []
        temp.extend(entries)
        ends = []
        starts = []
        zones = []
        waypoints = []
        for npcId, quest in npc_end:
            if temp[0] == npcId:
                ends.append(quest)
        for npcID, quest in npc_start:
            if temp[0] == npcID:
                starts.append(quest)
        q = [starts, ends]
        temp.append(q)
        for npcid, mapID, position_x, position_y, guid in npc:
            if temp[0] == npcid:
                zonexy = calculateCoords(mapID, position_x, position_y)
                if (zonexy == False):
                    print("Error with", npcid, mapID, position_x, position_y, guid,  "_______________________________________")
                    continue
                for coordsSet in zonexy:
                    if (coordsSet[1] == -1):
                        done = False
                        for a in zones:
                            if (a[0] == coordsSet[0]):
                                done = True
                        if (not done):
                            z = [coordsSet[0], [[coordsSet[1], coordsSet[2]]]]
                            zones.append(z)
                            print("Instance for", npcid, " added. XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        continue
                    else:
                        done = False
                        for a in zones:
                            if (a[0] == coordsSet[0]):
                                z = [coordsSet[1], coordsSet[2]]
                                a[1].append(z)
                                done = True
                                print("Coordinates for", npcid, "added.")
                                break
                        if (done):
                            continue
                        else:
                            z = [coordsSet[0], [[coordsSet[1], coordsSet[2]]]]
                            zones.append(z)
                            print("Zone for", npcid, "added. <<<<<<<<<<<<<<<<<<<<<")
                            continue
                for point, guid2, position_x2, position_y2 in npc_mov:
                    if (guid2 == guid):
                        zonexy2 = calculateCoords(mapID, position_x2, position_y2)
                        if (zonexy2 == False):
                            print("Error with", npcid, mapID, point, position_x2, position_y3, guid,  "_________________________Waypoints")
                            continue
                        for coordsSet in zonexy2:
                            if (coordsSet[1] == -1):
                                continue
                            else:
                                done = False
                                for a in waypoints:
                                    if (a[0] == coordsSet[0]):
                                        z = [coordsSet[1], coordsSet[2]]
                                        a[1].append(z)
                                        done = True
                                        print("Waypoint for", npcid, "added.")
                                        break
                                if (done):
                                    continue
                                else:
                                    z = [coordsSet[0], [[coordsSet[1], coordsSet[2]]]]
                                    waypoints.append(z)
                                    print("Zone for", npcid, "added. <<<<<<<<<<<<<<<<<Waypoints")
                                    continue
        temp.append(waypoints)
        temp.append(zones)
        alle.append(temp)
        print(temp[0], "done! <------------------------------------------")
    return alle

"""


######################################
NPC printing functions
######################################


"""

def getOldNPCData(file="npcDataOld.lua"):
    print("Getting old zone data...")
    infile = open(file, 'r')
    npcDataOld = infile.read()
    infile.close()
    import re
    npcDataTemp = re.findall(r"\n\t\['(.*?)'.*?\['zone'] = (\d+),.*?rds'\] =\n\t\t\{(.*?),\n\t\t\},", npcDataOld, re.S)
    npcDataSorted = []
    for n in npcDataTemp:
        name = n[0]
        zone = n[1]
        xy = re.findall(r"\[\d+\] = '(.*?),(.*?)',", n[2], re.S)
        alle = [name, zone, xy]
        npcDataSorted.append(alle)
    print("Getting old zone data suceeded.")
    return npcDataSorted

def checkZone(zoneListNew, npcDataNew, longest):
    validZones = []
    for zoneEntry in zoneListNew:
        for levelSet in zoneLevelList:
            if (zoneEntry[0] == levelSet[0]) and (npcDataNew[2] >= levelSet[1]) and (npcDataNew[3] <= levelSet[2]):
                validZones.append(zoneEntry[0])
                break

    if (len(validZones) == 1):
        zone = validZones[0]
    # no idea how to determine the right one here:
    elif (len(validZones) > 1):
        zone = validZones[0]
    else:
        zone = zoneListNew[longest][0]
    return zone

def findZoneCheckCoords(npcDataOld, npcDataNew):
    name = escapeName(str(npcDataNew[1]))
    zoneListOld = False
    for nameInSet, zoneInSet, xy in npcDataOld:
        if (nameInSet == name):
            if (int(zoneInSet) in validZoneList):
                zoneListOld = [[int(zoneInSet), xy]]
                zoneOld = zoneListOld[0][0]
            else:
                print("Non-Classic zone detected")
            break

    
    match = False
    if (npcDataNew[-1] == []):
        zoneListNew = False
    else:
        zoneListNew = npcDataNew[-1]
        longest = 0
        if (len(zoneListNew) > 1):
            lengthSet = []
            for zoneSet in zoneListNew:
                z = [zoneSet[0], len(zoneSet[1])]
                lengthSet.append(z)
            
            x = 0
            lengthLongest = 0
            for zoneId, length in lengthSet:
                if (lengthLongest < length):
                    lengthLongest = length
                    longest = x
                    x = x + 1
                if (zoneListOld):
                    if (zoneId == zoneOld):
                        match = True

    if (zoneListNew == False) and (zoneListOld == False):
        print(name, npcDataNew[0], "Nothing to add.")
        return False, False
    elif (zoneListNew == False) and (zoneListOld):
        print("Using Old Data: ", end="")
        return zoneListOld[0][0], zoneListOld
    elif (zoneListNew) and (zoneListOld == False):
        print("Using New Data: ", end="")
        return checkZone(zoneListNew, npcDataNew, longest), zoneListNew
    else:
        print("Using Merge Data: ", end="")
        if (match):
            zone = zoneOld
        else:
            if (len(zoneListNew) > 2):
                zone = checkZone(zoneListNew, npcDataNew, longest)
            else:
                zone = zoneListNew[longest][0]
        return zone, zoneListNew

def writeNpcFile(npcs, file="npcData.lua"):
    outfile = open(file, "w")
    outfile.write("npcData =\n{\n")
    
    npcDataOld = getOldNPCData()
    
    for npc in npcs:
        # this check is kind of useless, but better safe than sorry
        if (len(npc) == 10):
            if (npc[-1] == []):
                zoneList = False
            else:
                zoneList = npc[-1]
            if (npc[-2] == []):
                waypoints = False
            else:
                waypoints = npc[-2]
            quests = npc[-3]
        else:
            waypoints = npc[-1]
            quests = npc[-2]
            zoneList = False

        zone, zoneList = findZoneCheckCoords(npcDataOld, npc)
        if (zoneList):
            npcid = str(npc[0])
            print("Adding", npcid, end='... ')
            name = escapeName(str(npc[1]))
            minlvl = str(npc[2])
            maxlvl = str(npc[3])
            minlvlhp = str(npc[4])
            maxlvlhp = str(npc[5])

            if minlvl == maxlvl:
                level = minlvl
                if level == 63:
                    level = '??'
            else:
                level = minlvl + " - " + maxlvl
        
            if npc[6] == 1:
                level = level + " Elite"
            elif npc[6] == 2:
                level = level + " Rare Elite"
            elif npc[6] == 3:
                level = level + " World Boss"
            elif npc[6] == 4:
                level = level + " Rare"
        
            if minlvlhp == maxlvlhp:
                hp = minlvlhp
            else:
                hp = minlvlhp + " - " + maxlvlhp

            outfile.write("\t[" + npcid + "] =\n\t{\n")
            outfile.write("\t\t['name'] = '" + name + "',\n")
            outfile.write("\t\t['level'] = '" + level +  "',\n")
            outfile.write("\t\t['hp'] = '" + hp + "',\n")
        
            if quests[0] != []:
                outfile.write("\t\t['starts'] = {")
                for questId in quests[0]:
                    q = str(questId) + ","
                    outfile.write(q)
                outfile.write("},\n")
        
            if quests[1] != []:
                outfile.write("\t\t['ends'] = {")
                for questId in quests[1]:
                    q = str(questId) + ","
                    outfile.write(q)
                outfile.write("},\n")

            outfile.write("\t\t['zone'] = " + str(zone) +  ",\n")
            
            outfile.write("\t\t['zones'] =\n\t\t{\n")
            for zoneS in zoneList:
                zoneId = "\t\t\t[" + str(zoneS[0]) + "] = {"
                outfile.write(zoneId)
                for coords in zoneS[1]:
                    coord = "{" + str(coords[0]) + ", " + str(coords[1]) + "},"
                    outfile.write(coord)
                outfile.write("},\n")
            outfile.write("\t\t},\n")
            
            if (waypoints):
                outfile.write("\t\t['waypoints'] =\n\t\t{\n")
                for zoneS in waypoints:
                    zoneId = "\t\t\t[" + str(zoneS[0]) + "] = {"
                    outfile.write(zoneId)
                    for coords in zoneS[1]:
                        coord = "{" + str(coords[0]) + ", " + str(coords[1]) + "},"
                        outfile.write(coord)
                    outfile.write("},\n")
                outfile.write("\t\t},\n")
            
            outfile.write("\t},\n")
            
            print("Done.")
    outfile.write("}\n")
    print("Finished. Data added to", file)

"""


######################################
Quest functions
######################################


"""

def getQuestTables(cursor):
    print("Selecting MySQL tables...")
    cursor.execute("SELECT entry, Title, Objectives, RequiredRaces FROM quest_template")
    quest_tpl = []
    for a in cursor.fetchall():
        quest_tpl.append(a)
    print("Done.")
    return quest_tpl

def objectivesText(objectives):
    split = objectives.split('$B')
    temp = '\\n'.join(split)
    split1 = temp.split('$b')
    temp = '\\n'.join(split1)
    split2 = temp.split('$c')
    temp = '$C'.join(split2)
    split3 = temp.split('$r')
    temp = '$R'.join(split3)
    split4 = temp.split('$n')
    temp = '$N'.join(split4)
    return escapeName(temp)

def checkSide(racemask):
    if (racemask == 0):
        return 3
    
    alliance = False
    horde = False
    racem = racemask
    if (racem >= 128):
        racem = racem - 128
        horde = True
    if (racem >= 64):
        racem = racem - 64
        alliance = True
    if (racem >= 32):
        racem = racem - 32
        horde = True
    if (racem >= 16):
        racem = racem - 16
        horde = True
    if (racem >= 8):
        racem = racem - 8
        alliance = True
    if (racem >= 4):
        racem = racem - 4
        alliance = True
    if (racem >= 2):
        racem = racem - 2
        horde = True
    if (racem >= 1):
        racem = racem - 1
        alliance = True

    if (alliance and horde):
        return 3
    elif (horde):
        return 2
    elif (alliance):
        return 1
    else:
        print("Error:", racemask)
        return 0

def sortedQuests(quest_tpl):
    print("Checking objectives...")
    questsSorted = []
    for qID, title, objectives, racemask in quest_tpl:
        temp = title.split("'")
        name = "\\'".join(temp)
        text = objectivesText(objectives)
        side = checkSide(racemask)
        a = [qID, name, text, side]
        questsSorted.append(a)
    questsA, questsH, questsB = [], [], []
    for qID, name, text, side in questsSorted:
        quest = [qID, name, text]
        if (side == 1):
            questsA.append(quest)
        elif (side == 2):
            questsH.append(quest)
        elif (side == 3):
            questsB.append(quest)
    print("Done.")
    return questsA, questsH, questsB

"""


######################################
Quest printing functions
######################################


"""
years = [0, 2006, 2008, 2010]
months = [0, 12, 10, 10]
days = [0, 4, 13, 11]
vNames = ['0', 'Classic', 'TBC', 'WOTLK']

def checkVersion(y, m, d, version):
    if (int(y) < years[version]):
        return vNames[version]
    elif ((int(y) == years[version]) and (int(m) <= months[version])):# and (int(d) <= days[2])):
        return vNames[version]
    else:
        return False

def formatDate(date):
    import re
    try:
        y, m, d = re.findall(r"(\d+)", date)
    except:
        print(date)
        return False
    c = checkVersion(y, m, d, 1)
    t = checkVersion(y, m, d, 2)
    w = checkVersion(y, m, d, 3)
    if (c):
        return c
    elif (t):
        return t
    elif (w):
        return w
    else:
        return False

def formatComment(comment):
    unslashed = []
    for body, date in comment:
        step1 = body.replace("\\n", "[LINEFEED]")
        step2 = step1.replace("\\", "")
        newDate = formatDate(date)
        if (not newDate):
            continue
        unslashed.append([step2.replace("[LINEFEED]", "\\n"), newDate])
    unurled = []
    for body, date in unslashed:
        unurled.append(date + ":\\n" + body.replace("http://www.wowhead.com/?", ""))
    unbolded = []
    for body in unurled:
        step = body.replace("[b]", "")
        unbolded.append(step.replace("[/b]", ""))
    ununderlined = []
    for body in unbolded:
        step = body.replace("[u]", "")
        ununderlined.append(step.replace("[/u]", ""))
    unitaliced = []
    for body in ununderlined:
        step = body.replace("[i]", "")
        unitaliced.append(step.replace("[/i]", ""))
    ready = []
    for body in unitaliced:
        ready.append(body.replace("'", "\\'"))
    return ready

def getAllWHComments(faction):
    x = len(faction)
    y = 0
    z = 0
    new = []
    print("Get comments for", x, "questnames...")
    #debug: breaker = 0
    for name, qIDs in faction:
        """debug:
        if (breaker > 20):
            break
        breaker = breaker + 1
        """
        z = z + 1
        print(name, "(", z, "/", x, "):", sep="")
        newQIDs = []
        for qID, obj in qIDs:
            #if ((qID < 1) or (qID > 21)):
                #continue
            y = y + 1
            print(qID, end=": ")
            uncomment = getWHComments(qID)
            comment = formatComment(uncomment)
            if (comment == []):
                print("None")
            else:
                print(len(comment))
            newQIDs.append([qID, obj, comment])
        new.append([name, newQIDs])
    print("Finished with", y, "quest IDs for this faction. <--------------------")
    return new

def getWHComments(qid):
    from urllib import request
    url = "http://wowhead.com/quest=" + str(qid)
    r = request.urlopen(url)
    bytecode = r.read()
    stringC = bytecode.decode('utf-8', 'replace')
    import re
    pairs = re.findall(r"comment.*?body['\":]*(.*?)['\"]+,.*?date['\":]+(\d.*?) ", stringC, re.S)
    return pairs

def unpackOldData(qData):
    import re
    quests = re.findall(r"\t\['(.*?)'\] = \n(.*?)\t\t\},\n.*?\t\},\n", qData, re.S)
    sort = []
    for quest, commentBlock in quests:
        comments = re.findall(r"\[\d+\] = '(.*?)',\n", commentBlock, re.S)
        sort.append([quest, comments])
    return sort

def getOldQuestData(file="qDataOld.lua"):
    print("Getting old quest data...")
    infile = open(file, mode='r', encoding="ISO-8859-1")
    qDataOld = infile.read()
    infile.close()
    import re
    qDataA = re.findall(r"\t\['Alliance'\] =(.*?\n\t\},\n)\t\},", qDataOld, re.S)
    qDataH = re.findall(r"\t\['Horde'\] =(.*?\n\t\},\n)\t\},", qDataOld, re.S)
    qDataB = re.findall(r"\t\['Common'\] =(.*?\n\t\},\n)\t\},", qDataOld, re.S)
    print("Done.")
    return unpackOldData(qDataA[0]), unpackOldData(qDataH[0]), unpackOldData(qDataB[0])

def questsMerge(questsNew, questsOld):
    print("Merging...")
    questMerge = []
    done = []
    for qID, name, objectives in questsNew:
        if (not (qID in done)):
            done.append(qID)
            qIDs = [[qID, objectives]]
            for qID2, name2, objectives2 in questsNew:
                if ((name2 == name) and not (qID2 in done)):
                    done.append(qID2)
                    qIDs.append([qID2, objectives2])
            com = []
            for nameOld, comments in questsOld:
                if (nameOld == name):
                    for comment in comments:
                        if (comment in com):
                            continue
                        else:
                            com.append(comment)
            q = [name, qIDs, com]
            questMerge.append(q)
    print("Done.")
    return questMerge

def questSort(questsNew):
    print("Sorting...")
    questMerge = []
    done = []
    for qID, name, objectives in questsNew:
        if (not (qID in done)):
            done.append(qID)
            qIDs = [[qID, objectives]]
            for qID2, name2, objectives2 in questsNew:
                if ((name2 == name) and not (qID2 in done)):
                    done.append(qID2)
                    qIDs.append([qID2, objectives2])
            questMerge.append([name, qIDs])
    print("Done.")
    return questMerge

def writeFaction(faction, outfile):
    for name, qIDs in faction:
        outfile.write("\t\t['" + name + "'] =\n\t\t{\n")
        outfile.write("\t\t\t['IDs'] =\n\t\t\t{\n")
        if (len(qIDs) > 1):
            for qID, objectives, comments in qIDs:
                outfile.write("\t\t\t\t[" + str(qID) + "] = {'" + objectives + "',")
                outfile.write("{")
                for comment in comments:
                    outfile.write("'" + comment + "',")
                outfile.write("},},\n")
        else:
            for qID, objectives, comments in qIDs:
                outfile.write("\t\t\t\t[" + str(qID) + "] = {'',")
                outfile.write("{")
                for comment in comments:
                    outfile.write("'" + comment + "',")
                outfile.write("},},\n")
        outfile.write("\t\t\t},\n")
        outfile.write("\t\t},\n")
    outfile.write("\t},\n")

def writeSavedQuestFile(file="qData.lua"):
    import pickle
    outfile = open(file, "w", encoding="utf-8", errors="replace")

    print("Writing file...")
    outfile.write("qData = \n{\n")
    
    outfile.write("\t['Alliance'] =\n\t{\n")
    a = pickle.load(open("savea.p", "rb"))
    writeFaction(a, outfile)

    outfile.write("\t['Horde'] =\n\t{\n")
    h = pickle.load(open("saveh.p", "rb"))
    writeFaction(h, outfile)

    outfile.write("\t['Common'] =\n\t{\n")
    b = pickle.load(open("saveb.p", "rb"))
    writeFaction(b, outfile)
    
    outfile.write("}\n")
    outfile.close()
    print("Finished!")

def writeQuestFile(questsANew, questsHNew, questsBNew, file="qData.lua"):
    #questsAOld, questsHOld, questsBOld = getOldQuestData()
    #questsA, questsH, questsB = questsMerge(questsANew, questsAOld), questsMerge(questsHNew, questsHOld), questsMerge(questsBNew, questsBOld)
    questsA, questsH, questsB = questSort(questsANew), questSort(questsHNew), questSort(questsBNew)

    import pickle
    outfile = open(file, "w", encoding="utf-8", errors="replace")

    print("Writing file...")
    outfile.write("qData = \n{\n")
    
    outfile.write("\t['Alliance'] =\n\t{\n")
    a = getAllWHComments(questsA)
    pickle.dump(a, open("savea.p", "wb"))
    #a = pickle.load(open("savea.p", "rb"))
    writeFaction(a, outfile)

    outfile.write("\t['Horde'] =\n\t{\n")
    h = getAllWHComments(questsH)
    pickle.dump(h, open("saveh.p", "wb"))
    writeFaction(h, outfile)

    outfile.write("\t['Common'] =\n\t{\n")
    b = getAllWHComments(questsB)
    pickle.dump(b, open("saveb.p", "wb"))
    writeFaction(b, outfile)
    
    outfile.write("}\n")
    outfile.close()
    print("Finished!")

"""


######################################
Object functions
######################################


"""

def getObjectTables(cursor):
    print("Selecting MySQL tables...")
    cursor.execute("SELECT entry, type, name FROM gameobject_template")
    obj_tpl = []
    for a in cursor.fetchall():
        obj_tpl.append(a)
    cursor.execute("SELECT id, map, position_x, position_y FROM gameobject")
    obj = []
    for a in cursor.fetchall():
        obj.append(a)
    cursor.execute("SELECT id, quest FROM gameobject_questrelation")
    obj_starts = []
    for a in cursor.fetchall():
        obj_starts.append(a)
        cursor.execute("SELECT id, quest FROM gameobject_involvedrelation")
    obj_ends = []
    for a in cursor.fetchall():
        obj_ends.append(a)
    print("Done.")
    return [obj_tpl, obj, obj_starts, obj_ends]

def sortedObjects(obj_tbl):
    types = [2,3,5,10]
    objects = []
    for obj in obj_tbl[0]:
        if not (obj[1] in types):
            continue
        objID = obj[0]
        name = obj[2]
        starts = []
        ends = []
        zones = []
        for oid, mapID, x, y in obj_tbl[1]:
            if (oid != objID):
                continue
            zonexy = calculateCoords(mapID, x, y)
            if (zonexy == False):
                print("Error with", objID, mapID, x, y, oid,  "_______________________________________")
                continue
            for coordsSet in zonexy:
                if (coordsSet[1] == -1):
                    done = False
                    for a in zones:
                        if (a[0] == coordsSet[0]):
                            done = True
                    if (not done):
                        z = [coordsSet[0], [[coordsSet[1], coordsSet[2]]]]
                        zones.append(z)
                        print("Instance for", oid, " added. XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    continue
                else:
                    done = False
                    for a in zones:
                        if (a[0] == coordsSet[0]):
                            z = [coordsSet[1], coordsSet[2]]
                            a[1].append(z)
                            done = True
                            print("Coordinates for", oid, "added.")
                            break
                    if (done):
                        continue
                    else:
                        z = [coordsSet[0], [[coordsSet[1], coordsSet[2]]]]
                        zones.append(z)
                        print("Zone for", oid, "added. <<<<<<<<<<<<<<<<<<<<<")
                        continue
        for oid, quest in obj_tbl[2]:
            if (oid == objID):
                starts.append(quest)
        for oid, quest in obj_tbl[3]:
            if (oid == objID):
                ends.append(quest)
        if zones == []:
            print("Error with", objID, name, ": no location OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        objects.append([objID, name, zones, starts, ends])
    return objects

def writeObjFile(objs, file="objData.lua"):
    outfile = open(file, "w")
    outfile.write("objData =\n{\n")
    
    for obj in objs:
        objid = str(obj[0])
        if obj[2] == []:
            print("Left out (no location):", objid)
            if obj[3] != [] or obj[4] != []:
                print("Error: has quests <------------------------")
            continue
        
        print("Adding", objid, end='... ')
        name = escapeName(str(obj[1]))

        outfile.write("\t[" + objid + "] =\n\t{\n")
        outfile.write("\t\t['name'] = '" + name + "',\n")
        
        if obj[3] != []:
            outfile.write("\t\t['starts'] = {")
            for questId in obj[3]:
                q = str(questId) + ","
                outfile.write(q)
            outfile.write("},\n")
        
        if obj[4] != []:
            outfile.write("\t\t['ends'] = {")
            for questId in obj[4]:
                q = str(questId) + ","
                outfile.write(q)
            outfile.write("},\n")
            
        outfile.write("\t\t['zones'] =\n\t\t{\n")
        for zones in obj[2]:
            zoneId = "\t\t\t[" + str(zones[0]) + "] = {"
            outfile.write(zoneId)
            for coords in zones[1]:
                coord = "{" + str(coords[0]) + ", " + str(coords[1]) + "},"
                outfile.write(coord)
            outfile.write("},\n")
        outfile.write("\t\t},\n")
            
        outfile.write("\t},\n")
            
        print("Done.")
    outfile.write("}\n")
    print("Finished. Data added to", file)
