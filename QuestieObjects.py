
with open("sqlua/newObjectsCoords.lua", "w") as outfile:
    outfile.write("QuestieNewObjects = {\n")
    for objectId in a:
        outfile.write(" ["+objectId+"] = {\n")
        outfile.write("  name = \""+obj.objectList[int(objectId)].name+"\",\n  locations = {\n")
        for zone in obj.objectList[int(objectId)].spawns.cByZone:
            outfile.write("   ["+str(zone)+"] = {")
            for point in obj.objectList[int(objectId)].spawns.cByZone[zone]:
                outfile.write("{"+str(round(point[0]/100, 4))+","+str(round(point[1]/100, 4))+"},")
            outfile.write("},\n")
        outfile.write("  },\n")
        outfile.write(" },\n")
    outfile.write("}\n")

with open("sqlua/newObjectsCoords2.lua", "w") as outfile:
    outfile.write("QuestieNewObjects = {\n")
    for objectId in a:
        outfile.write(" ["+objectId+"] = {\n")
        outfile.write("  name = \""+obj.objectList[int(objectId)].name+"\",\n  locations = {\n")
        for zone in obj.objectList[int(objectId)].spawns.cByZone:
            for point in obj.objectList[int(objectId)].spawns.cByZone[zone]:
                outfile.write("   {"+str(zone)+","+str(round(point[0]/100, 4))+","+str(round(point[1]/100, 4))+"},\n")
            outfile.write("  },\n")
        outfile.write(" },\n")
    outfile.write("}\n")

with open("sqlua/newObjectsCoords3.lua", "w") as outfile:
    outfile.write("QuestieNewObjects = {\n")
    for objectId in a:
        outfile.write(" ["+objectId+"] = {\n")
        outfile.write("  name = \""+obj.objectList[int(objectId)].name+"\",\n  locations = {\n")
        for zone in obj.objectList[int(objectId)].spawns.cByZone:
            c, z = 0, 0
            for set in zoneMask:
                if set[0] == zone:
                    c = set[2]
                    z = set[3]
            for point in obj.objectList[int(objectId)].spawns.cByZone[zone]:
                outfile.write("   {"+str(c)+","+str(z)+","+str(round(point[0]/100, 4))+","+str(round(point[1]/100, 4))+"},\n")
            outfile.write("  },\n")
        outfile.write(" },\n")
    outfile.write("}\n")

zoneMask = [(1, 'Dun Morogh', 2, 7),
            (3, 'Badlands', 2, 3),
            (4, 'Blasted Lands', 2, 4),
            (8, 'Swamp of Sorrows', 2, 19),
            (10, 'Duskwood', 2, 8),
            (11, 'Wetlands', 2, 25),
            (12, 'Elwynn Forest', 2, 10),
            (28, 'Western Plaguelands', 2, 23),
            (33, 'Stranglethorn Vale', 2, 18),
            (36, 'Alterac Mountains', 2, 1),
            (38, 'Loch Modan', 2, 13),
            (40, 'Westfall', 2, 24),
            (41, 'Deadwind Pass', 2, 6),
            (44, 'Redridge Mountains', 2, 14),
            (45, 'Arathi Highlands', 2, 2),
            (46, 'Burning Steppes', 2, 5),
            (47, 'The Hinterlands', 2, 20),
            (51, 'Searing Gorge', 2, 15),
            (85, 'Tirisfal Glades', 2, 21),
            (130, 'Silverpine Forest', 2, 16),
            (139, 'Eastern Plaguelands', 2, 9),
            (267, 'Hillsbrad Foothills', 2, 11),
            (1497, 'Undercity', 2, 22),
            (1519, 'Stormwind City', 2, 17),
            (1537, 'Ironforge', 2, 12),
            (14, 'Durotar', 1, 6),
            (15, 'Dustwallow Marsh', 1, 7),
            (16, 'Azshara', 1, 2),
            (17, 'The Barrens', 1, 17),
            (141, 'Teldrassil', 1, 16),
            (148, 'Darkshore', 1, 3),
            (215, 'Mulgore', 1, 11),
            (331, 'Ashenvale', 1, 1),
            (357, 'Feralas', 1, 9),
            (361, 'Felwood', 1, 8),
            (400, 'Thousand Needles', 1, 18),
            (405, 'Desolace', 1, 5),
            (406, 'Stonetalon Mountains', 1, 14),
            (440, 'Tanaris', 1, 15),
            (490, "Un'Goro Crater", 1, 20),
            (493, 'Moonglade', 1, 10),
            (618, 'Winterspring', 1, 21),
            (1377, 'Silithus', 1, 13),
            (1637, 'Orgrimmar', 1, 12),
            (1638, 'Thunder Bluff', 1, 19),
            (1657, 'Darnassus', 1, 4)]
