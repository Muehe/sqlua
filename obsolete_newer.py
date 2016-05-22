"""
import pymysql
dbc = pymysql.connect('localhost', 'mangos', 'mangos', 'mangos')
cursor = dbc.cursor()
"""

def main(cursor):
	writeItemFile(sortItemTables(getItemTables(cursor)), "WHDB/itemData.lua")
"""
	quests = getQuestTable(cursor)
	coZones = getZonesFromLog()
	npcs = getNPCTables(cursor)
	npcss = sortNPCTables(npcs, coZones)
"""

"""


######################################
Data Definitions
######################################


"""

mapBorders = [(1, 'Dun Morogh', 0, 1802.08325195313, -3122.91650390625, -3877.08325195313, -7160.41650390625),
			  (3, 'Badlands', 0, -2079.16650390625, -4566.66650390625, -5889.5830078125, -7547.91650390625),
			  (4, 'Blasted Lands', 0, -1241.66662597656, -4591.66650390625, -10566.666015625, -12800),
			  (8, 'Swamp of Sorrows', 0, -2222.91650390625, -4516.66650390625, -9620.8330078125, -11150),
			  (10, 'Duskwood', 0, 833.333312988281, -1866.66662597656, -9716.666015625, -11516.666015625),
			  (11, 'Wetlands', 0, -389.583312988281, -4525, -2147.91650390625, -4904.16650390625),
			  (12, 'Elwynn Forest', 0, 1535.41662597656, -1935.41662597656, -7939.5830078125, -10254.166015625),
			  (28, 'Western Plaguelands', 0, 416.666656494141, -3883.33325195313, 3366.66650390625, 499.999969482422),
			  (33, 'Stranglethorn Vale', 0, 2220.83325195313, -4160.41650390625, -11168.75, -15422.916015625),
			  (36, 'Alterac Mountains', 0, 783.333312988281, -2016.66662597656, 1500, -366.666656494141),
			  (38, 'Loch Modan', 0, -1993.74987792969, -4752.0830078125, -4487.5, -6327.0830078125),
			  (40, 'Westfall', 0, 3016.66650390625, -483.333312988281, -9400, -11733.3330078125),
			  (41, 'Deadwind Pass', 0, -833.333312988281, -3333.33325195313, -9866.666015625, -11533.3330078125),
			  (44, 'Redridge Mountains', 0, -1570.83325195313, -3741.66650390625, -8575, -10022.916015625),
			  (45, 'Arathi Highlands', 0, -866.666625976563, -4466.66650390625, -133.33332824707, -2533.33325195313),
			  (46, 'Burning Steppes', 0, -266.666656494141, -3195.83325195313, -7031.24951171875, -8983.3330078125),
			  (47, 'The Hinterlands', 0, -1575, -5425, 1466.66662597656, -1100),
			  (51, 'Searing Gorge', 0, -322.916656494141, -2554.16650390625, -6100, -7587.49951171875),
			  (85, 'Tirisfal Glades', 0, 3033.33325195313, -1485.41662597656, 3837.49975585938, 824.999938964844),
			  (130, 'Silverpine Forest', 0, 3449.99975585938, -750, 1666.66662597656, -1133.33325195313),
			  (139, 'Eastern Plaguelands', 0, -2185.41650390625, -6056.25, 3799.99975585938, 1218.75),
			  (267, 'Hillsbrad Foothills', 0, 1066.66662597656, -2133.33325195313, 400, -1733.33325195313),
			  (1497, 'Undercity', 0, 873.192626953125, -86.1824035644531, 1877.9453125, 1237.84118652344),
			  (1519, 'Stormwind City', 0, 1380.97143554688, 36.7006301879883, -8278.8505859375, -9175.205078125),
			  (1537, 'Ironforge', 0, -713.591369628906, -1504.21643066406, -4569.2412109375, -5096.845703125),
			  (14, 'Durotar', 1, -1962.49987792969, -7249.99951171875, 1808.33325195313, -1716.66662597656),
			  (15, 'Dustwallow Marsh', 1, -974.999938964844, -6225, -2033.33325195313, -5533.3330078125),
			  (16, 'Azshara', 1, -3277.08325195313, -8347.916015625, 5341.66650390625, 1960.41662597656),
			  (17, 'The Barrens', 1, 2622.91650390625, -7510.41650390625, 1612.49987792969, -5143.75),
			  (141, 'Teldrassil', 1, 3814.58325195313, -1277.08325195313, 11831.25, 8437.5),
			  (148, 'Darkshore', 1, 2941.66650390625, -3608.33325195313, 8333.3330078125, 3966.66650390625),
			  (215, 'Mulgore', 1, 2047.91662597656, -3089.58325195313, -272.916656494141, -3697.91650390625),
			  (331, 'Ashenvale', 1, 1699.99987792969, -4066.66650390625, 4672.91650390625, 829.166625976563),
			  (357, 'Feralas', 1, 5441.66650390625, -1508.33325195313, -2366.66650390625, -6999.99951171875),
			  (361, 'Felwood', 1, 1641.66662597656, -4108.3330078125, 7133.3330078125, 3299.99975585938),
			  (400, 'Thousand Needles', 1, -433.333312988281, -4833.3330078125, -3966.66650390625, -6899.99951171875),
			  (405, 'Desolace', 1, 4233.3330078125, -262.5, 452.083312988281, -2545.83325195313),
			  (406, 'Stonetalon Mountains', 1, 3245.83325195313, -1637.49987792969, 2916.66650390625, -339.583312988281),
			  (440, 'Tanaris', 1, -218.749984741211, -7118.74951171875, -5875, -10475),
			  (490, "Un'Goro Crater", 1, 533.333312988281, -3166.66650390625, -5966.66650390625, -8433.3330078125),
			  (493, 'Moonglade', 1, -1381.25, -3689.58325195313, 8491.666015625, 6952.0830078125),
			  (618, 'Winterspring', 1, -316.666656494141, -7416.66650390625, 8533.3330078125, 3799.99975585938),
			  (1377, 'Silithus', 1, 2537.5, -945.833984375, -5958.333984375, -8281.25),
			  (1637, 'Orgrimmar', 1, -3680.60107421875, -5083.20556640625, 2273.87719726563, 1338.46057128906),
			  (1638, 'Thunder Bluff', 1, 516.666625976563, -527.083312988281, -849.999938964844, -1545.83325195313),
			  (1657, 'Darnassus', 1, 2938.36279296875, 1880.02954101563, 10238.31640625, 9532.5869140625)]
instanceIds = [(209, 'Shadowfang Keep', 33),
			   (491, 'Razorfen Kraul', 47),
			   (717, 'Stormwind Stockade', 34),
			   (718, 'Wailing Caverns', 43),
			   (719, 'Blackfathom Deeps', 48),
			   (721, 'Gnomeregan', 90),
			   (722, 'Razorfen Downs', 129),
			   (796, 'Scarlet Monastery', 189),
			   (1176, "Zul'Farrak", 209),
			   (1337, 'Uldaman', 70),
			   (1477, 'Sunken Temple', 109),
			   (1581, 'The Deadmines', 36),
			   (1583, 'Blackrock Spire', 229),
			   (1585, 'Blackrock Depths', 230),
			   (1977, "Zul'Gurub", 309),
			   (2017, 'Stratholme', 329),
			   (2057, 'Scholomance', 289),
			   (2100, 'Maraudon', 349),
			   (2159, "Onyxia's Lair", 249),
			   (2257, 'Deeprun Tram', 369),
			   (2437, 'Ragefire Chasm', 389),
			   (2557, 'Dire Maul', 429),
			   (2677, 'Blackwing Lair', 469),
			   (2717, 'Molten Core', 409),
			   (3428, "Ahn'Qiraj", 531),
			   (3429, "Ruins of Ahn'Qiraj", 509),
			   (3456, 'Naxxramas', 533),
			   (2917, 'Horde PVP Barracks', 450),
			   (2918, 'Alliance PVP Barracks', 449),
			   (2597, 'Alterac Valley', 30),
			   (3277, 'Warsong Gulch', 489),
			   (3358, 'Arathi Basin', 529)
			   #(209, 'Shadowfang Keep', '33', '4500', '300', '1133.333', '-1666.667'),
			   #(491, 'Razorfen Kraul', '47', '2766.667', '966.6666', '2733.333', '1533.333'),
			   #(722, 'Razorfen Downs', '129', '2766.667', '-633.3333', '3266.667', '999.9999'),
			   #(796, 'Scarlet Monastery', '189', '1508.333', '-800', '1918.75', '379.166'),
			   #(1176, "Zul'Farrak", '209', '1625', '241.6667', '2052.083', '1129.167'),
			   #(1581, 'The Deadmines', '36', '1966.667', '-3033.333', '1133.333', '-2200'),
			   #(1977, "Zul'Gurub", '309', '-693.75', '-2570.833', '-11308.33', '-12560.42'),
			   #(2017, 'Stratholme', '329', '-1766.667', '-5166.667', '4333.333', '2066.667'),
			   #(2057, 'Scholomance', '289', '633.3333', '-1166.667', '600', '-600'),
			   #(2597, 'Alterac Valley', '30', '1781.24987792969', '-2456.25', '1085.41662597656', '-1739.58325195313'),
			   #(2677, 'Blackwing Lair', '469', '633.3333', '-2766.667', '-6333.333', '-8600'),
			   #(3277, 'Warsong Gulch', '489', '2041.66662597656', '895.833312988281', '1627.08325195313', '862.499938964844'),
			   #(3358, 'Arathi Basin', '529', '1858.33325195313', '102.08332824707', '1508.33325195313', '337.5'),
			   #(3428, "Ahn'Qiraj", '531', '3033.333', '1233.333', '-7933.333', '-9133.333'),
			   #(3429, "Ruins of Ahn'Qiraj", '509', '3035.417', '522.9166', '-8233.333', '-9908.333')
			   ]
continentBorders = [(5, 'Eastern Kingdoms', 0, 16000, -19199.900390625, 7466.60009765625, -16000),
					(6, 'Kalimdor', 1, 17066.599609375, -19733.2109375, 12799.900390625, -11733.2998046875)]

validZoneList = [1, 3, 4, 8, 10, 11, 12, 14, 15, 16, 17, 28, 33, 36, 38, 40, 41, 44, 45, 46, 47, 51, 85, 130, 139, 141, 148, 215, 267, 331, 357, 361, 400, 405, 406, 440, 490, 493, 618, 1377, 1497, 1519, 1537, 1637, 1638, 1657]

"""


######################################
Misc Functions
######################################


"""

# the file used here is a server log from a modified cmangos
# to aquire:
# get cmangos source
# search ObjectMgr.cpp for "zoneId, areaId" (without quotes)
# uncomment the three lines
# copy and adjust them to the creature function in the same file
# compile, run, close, check Server.log
def getZonesFromLog(file="Zeug/Save_Server.log"):
	print("Getting Zone Data...")
	infile = open(file, mode='r', encoding="utf-8")
	fileData = infile.read()
	infile.close()
	import re
	creatureZones = re.findall(r"creature SET zone_id=(\d+), area_id=\d+ WHERE guid=(\d+)", fileData, re.S)
	objectZones = re.findall(r"gameobject SET zone_id=(\d+), area_id=\d+ WHERE guid=(\d+)", fileData, re.S)
	print("Converting...")
	cr = []
	for x in creatureZones:
		cr.append([int(x[0]), int(x[1])])
	ob = []
	for x in objectZones:
		cr.append([int(x[0]), int(x[1])])
	print("Done.")
	return [cr, ob]

def escapeName(string):
	name = string.replace('"', '\\"')
	name2 = name.replace("'", "\\'")
	return name2

def unpackBitMask(bitMask):
	bits = []
	numBits=1
	while(pow(2, numBits) < bitMask):
		numBits += 1
	for x in range(-numBits, 1):
		potency = 1 << -x #pow(2, -x)
		if (bitMask >= potency):
			bitMask = bitMask - potency
			#s = "Flag on bit " + str(-x) + " is set (value " + str(potency) +")"
			#print (s)
			bits.insert(0, -x)
	return bits

def checkBit(bit, bitMask):
	set = unpackBitMask(bitMask)
	if bit in set:
		return True
	else:
		return False

"""


######################################
Quest Functions
######################################


"""
def getQuestTable(cursor):
	print("Selecting quest related MySQL tables...")
	# SrcItemId needed to check for spell_script_target (type and targetEntry) via item_template.spellId
	cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort FROM quest_template")
	quest_template = []
	for a in cursor.fetchall():
		quest_template.append(a)
		
	cursor.execute("SELECT id, quest FROM creature_involvedrelation")
	creature_involvedrelation = []
	for a in cursor.fetchall():
		creature_involvedrelation.append(a)
	
	cursor.execute("SELECT id, quest FROM gameobject_involvedrelation")
	gameobject_involvedrelation = []
	for a in cursor.fetchall():
		gameobject_involvedrelation.append(a)
		
	cursor.execute("SELECT id, quest FROM creature_questrelation")
	creature_questrelation = []
	for a in cursor.fetchall():
		creature_questrelation.append(a)
	
	cursor.execute("SELECT id, quest FROM gameobject_questrelation")
	gameobject_questrelation = []
	for a in cursor.fetchall():
		gameobject_questrelation.append(a)
	
	cursor.execute("SELECT entry, startquest FROM item_template")
	item_questrelation = []
	for a in cursor.fetchall():
		item_questrelation.append(a)
	
	cursor.execute("SELECT id, quest FROM areatrigger_involvedrelation")
	areatrigger_involvedrelation = []
	for a in cursor.fetchall():
		areatrigger_involvedrelation.append(a)
	
	print("Done.")
	
	print("Sorting quest related tables.")
	quest_sort = sortQuestTable(quest_template, creature_involvedrelation, gameobject_involvedrelation, creature_questrelation, gameobject_questrelation, item_questrelation, areatrigger_involvedrelation)
	print("Done.")
	
	return quest_sort

def sortQuestTable(quest_template, creature_involvedrelation, gameobject_involvedrelation, creature_questrelation, gameobject_questrelation, item_questrelation, areatrigger_involvedrelation):
	newQuests = []
	for quest in quest_template:
		entry = quest[0]
		MinLevel = quest[1]
		QuestLevel = quest[2]
		Type = quest[3]
		RequiredClasses = quest[4]
		RequiredRaces = quest[5]
		RequiredSkill = quest[6]
		RequiredSkillValue = quest[7]
		RepObjectiveFaction = quest[8]
		RepObjectiveValue = quest[9]
		RequiredMinRepFaction = quest[10]
		RequiredMinRepValue = quest[11]
		RequiredMaxRepFaction = quest[12]
		RequiredMaxRepValue = quest[13]
		QuestFlags = quest[14]
		PrevQuestId = quest[15]
		NextQuestId = quest[16]
		NextQuestInChain = quest[17]
		ExclusiveGroup = quest[18]
		Title = quest[19]
		Objectives = quest[20]
		ReqItemId1 = quest[21]
		ReqItemId2 = quest[22]
		ReqItemId3 = quest[23]
		ReqItemId4 = quest[24]
		ReqSourceId1 = quest[25]
		ReqSourceId2 = quest[26]
		ReqSourceId3 = quest[27]
		ReqSourceId4 = quest[28]
		ReqCreatureOrGOId1 = quest[29]
		ReqCreatureOrGOId2 = quest[30]
		ReqCreatureOrGOId3 = quest[31]
		ReqCreatureOrGOId4 = quest[32]
		ReqSpellCast1 = quest[33]
		ReqSpellCast2 = quest[34]
		ReqSpellCast3 = quest[35]
		ReqSpellCast4 = quest[36]
		PointMapId = quest[37]
		PointX = quest[38]
		PointY = quest[39]
		StartScript = quest[40]
		CompleteScript = quest[41]
		SrcItemId = quest[42]
		ZoneOrSort = quest[43]
		
		# RequiredSkills
		if (RequiredSkill != 0):
			RequiredSkills = [RequiredSkill, RequiredSkillValue]
		else:
			RequiredSkills = []
		
		# RequiredRep
		if (RequiredMinRepFaction != 0) or (RequiredMaxRepFaction != 0):
			RequiredRep = [RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue]
		else:
			RequiredRep = []
		
		# ReqItemIds
		if (ReqItemId1 != 0) and (ReqItemId1 != SrcItemId):
			ReqItemIds = [ReqItemId1]
		else:
			ReqItemIds = []
		if (ReqItemId2 != 0) and (ReqItemId2 != SrcItemId):
			ReqItemIds.append(ReqItemId2)
		if (ReqItemId3 != 0) and (ReqItemId3 != SrcItemId):
			ReqItemIds.append(ReqItemId3)
		if (ReqItemId4 != 0) and (ReqItemId4 != SrcItemId):
			ReqItemIds.append(ReqItemId4)
		
		# ReqSourceIds
		if (ReqSourceId1 != 0):
			ReqSourceIds = [ReqSourceId1]
		else:
			ReqSourceIds = []
		if (ReqSourceId2 != 0):
			ReqSourceIds.append(ReqSourceId2)
		if (ReqSourceId3 != 0):
			ReqSourceIds.append(ReqSourceId3)
		if (ReqSourceId4 != 0):
			ReqSourceIds.append(ReqSourceId4)
		
		# ReqCreatureOrGOIds
		if (ReqCreatureOrGOId1 != 0):
			if (ReqCreatureOrGOId1 > 0):
				ReqCreatureOrGOIds = [[ReqCreatureOrGOId1],[]]
			elif (ReqCreatureOrGOId1 < 0):
				ReqCreatureOrGOIds = [[],[-ReqCreatureOrGOId1]]
		else:
			ReqCreatureOrGOIds = [[], []]
		if (ReqCreatureOrGOId2 > 0):
			ReqCreatureOrGOIds[0].append(ReqCreatureOrGOId2)
		elif (ReqCreatureOrGOId2 < 0):
			ReqCreatureOrGOIds[1].append(-ReqCreatureOrGOId2)
		if (ReqCreatureOrGOId3 > 0):
			ReqCreatureOrGOIds[0].append(ReqCreatureOrGOId3)
		elif (ReqCreatureOrGOId3 < 0):
			ReqCreatureOrGOIds[1].append(-ReqCreatureOrGOId3)
		if (ReqCreatureOrGOId4 > 0):
			ReqCreatureOrGOIds[0].append(ReqCreatureOrGOId4)
		elif (ReqCreatureOrGOId4 < 0):
			ReqCreatureOrGOIds[1].append(-ReqCreatureOrGOId4)
		
		# ReqSpellCasts
		if (ReqSpellCast1 != 0):
			ReqSpellCasts = [ReqSpellCast1]
		else:
			ReqSpellCasts = []
		if (ReqSpellCast2 != 0):
			ReqSpellCasts.append(ReqSpellCast2)
		if (ReqSpellCast3 != 0):
			ReqSpellCasts.append(ReqSpellCast3)
		if (ReqSpellCast4 != 0):
			ReqSpellCasts.append(ReqSpellCast4)
		
		# find quest start points
		CreatureOrGOOrItemQuestStart = [[], [], []]
		for x in creature_questrelation:
			if x[1] == entry:
				CreatureOrGOOrItemQuestStart[0].append(x[0])
		for x in gameobject_questrelation:
			if x[1] == entry:
				CreatureOrGOOrItemQuestStart[1].append(x[0])
		for x in item_questrelation:
			if x[1] == entry:
				CreatureOrGOOrItemQuestStart[2].append(x[0])
		
		# find quest end points
		CreatureOrGOQuestEnd = [[], []]
		for x in creature_involvedrelation:
			if x[1] == entry:
				CreatureOrGOQuestEnd[0].append(x[0])
		for x in gameobject_involvedrelation:
			if x[1] == entry:
				CreatureOrGOQuestEnd[1].append(x[0])
		
		areatrigger = 0
		for x in areatrigger_involvedrelation:
			if x[1] == entry:
				areatrigger = x[0]
		
		newQuest = [
						entry,							# 0
						Title,							# 1
						Objectives,						# 2
						MinLevel,						# 3
						QuestLevel,						# 4
						Type,							# 5
						QuestFlags,						# 6
						StartScript,					# 7
						CompleteScript,					# 8
						[								# 9
							RequiredClasses,			# 9.0
							RequiredRaces,				# 9.1
							RequiredSkills,				# 9.2[0:1]
							RequiredRep					# 9.3[0:3]
						],
						[								# 10
							RepObjectiveFaction,		# 10.0
							RepObjectiveValue,			# 10.1
							ReqItemIds,					# 10.2[0:3]
							ReqSourceIds,				# 10.3[0:3]
							ReqCreatureOrGOIds,			# 10.4[[0:3], [0:3]]
							ReqSpellCasts,				# 10.5[0:3]
							[							# 10.6 POI
								PointMapId,				# 10.6.0
								PointX,					# 10.6.1
								PointY					# 10.6.2
							]
						],
						[								# 11
							PrevQuestId,				# 11.0
							NextQuestId,				# 11.1
							NextQuestInChain,			# 11.2
							ExclusiveGroup				# 11.3
						],
						CreatureOrGOOrItemQuestStart,	# 12 [[Creatures], [Gameobjects], [Items]]
						CreatureOrGOQuestEnd,			# 13 [[Creatures], [Gameobjects]]
						areatrigger,					# 14
						SrcItemId,						# 15
						ZoneOrSort						# 16
					]
		newQuests.append(newQuest)
	return newQuests

def printQuest(quest):
	print("0: ID = "+str(quest[0]))
	print("1: Title = "+quest[1])
	if (quest[2] != ""):
		print("2: Objectives = "+quest[2])
	if (quest[3] != 0):
		print("3: MinLevel = "+str(quest[3]))
	if (quest[4] != 0):
		print("4: QuestLevel = "+str(quest[4]))
	if (quest[5] != 0):
		print("5: Type = "+str(quest[5]))
	if (quest[6] != 0):
		print("6: QuestFlags = "+str(quest[6]))
	if (quest[7] != 0):
		print("7: StartScript = "+str(quest[7]))
	if (quest[8] != 0):
		print("8: CompleteScript = "+str(quest[8]))
	if (quest[9][0] != 0):
		print("	9.0: RequiredClasses = "+str(quest[9][0]))
	if (quest[9][1] != 0):
		print("	9.1 RequiredRaces = "+str(quest[9][1]))
	if (quest[9][2] != []):
		print("	9.2 RequiredSkill/Value = "+str(quest[9][2][0])+str(quest[9][2][1]))
	if (quest[9][3] != []):
		print("	9.3.0 RequiredMinRepFaction = "+str(quest[9][3][0]))
		print("	9.3.1 RequiredMinRepValue = "+str(quest[9][3][1]))
		print("	9.3.2 RequiredMaxRepFaction = "+str(quest[9][3][2]))
		print("	9.3.3 RequiredMaxRepValue = "+str(quest[9][3][3]))
	if (quest[10][0] != 0):
		print("	10.0: RepObjectiveFaction = "+str(quest[10][0]))
	if (quest[10][1] != 0):
		print("	10.1: RepObjectiveValue = "+str(quest[10][1]))
	if (quest[10][2] != []):
		print("	10.2: ReqItemIds:")
		for x in quest[10][2]:
			print("		"+str(x))
	if (quest[10][3] != []):
		print("	10.3: ReqSourceIds:")
		for x in quest[10][3]:
			print("		"+str(x))
	if (quest[10][4][0] != []):
		print("	10.4.0: ReqCreatures:")
		for x in quest[10][4][0]:
			print("		"+str(x))
	if (quest[10][4][1] != []):
		print("	10.4.1: ReqGameobjects:")
		for x in quest[10][4][1]:
			print("		"+str(x))
	if (quest[10][5] != []):
		print("	10.5: ReqSpellCasts:")
		for x in quest[10][5]:
			print("		"+str(x))
	if (quest[10][6][0] != 0):
		print("		10.6.0: PointMapId = "+str([10][6][0]))
	if (quest[10][6][1] != 0):
		print("		10.6.1: PointX = "+str(quest[10][6][1]))
	if (quest[10][6][2] != 0):
		print("		10.6.2: PointY = "+str(quest[10][6][2]))
	if (quest[11][0] != 0):
		print("	11.0: PrevQuestId = "+str(quest[11][0]))
	if (quest[11][1] != 0):
		print("	11.1: NextQuestId = "+str(quest[11][1]))
	if (quest[11][2] != 0):
		print("	11.2: NextQuestInChain = "+str(quest[11][2]))
	if (quest[11][3] != 0):
		print("	11.3: ExclusiveGroup = "+str(quest[11][3]))
	if (quest[12][0] != []):
		print("	12.0: Start by Creatures:")
		for x in quest[12][0]:
			print("		"+str(x))
	if (quest[12][1] != []):
		print("	12.1: Start by Gameobject:")
		for x in quest[12][1]:
			print("		"+str(x))
	if (quest[12][2] != []):
		print("	12.2: Start by Item:")
		for x in quest[12][2]:
			print("		"+str(x))
	if (quest[13][0] != []):
		print("	13.0: End by Creatures:")
		for x in quest[13][0]:
			print("		"+str(x))
	if (quest[13][1] != []):
		print("	13.1: End by Gameobject:")
		for x in quest[13][1]:
			print("		"+str(x))
	if (quest[14] != 0):
		print("	14: Areatrigger ID = "+str(quest[14]))
	if (quest[15] != 0):
		print("	15: SrcItemId = "+str(quest[15]))
	if (quest[16] != 0):
		print("	16: ZoneOrSort = "+str(quest[16]))

def printQuestByID(questID, questList):
	for quests in questList:
		if quests[0] == questID:
			printQuest(quests)
			break

"""			newQuest = [
						entry,							# 0
						Title,							# 1
						Objectives,						# 2
						MinLevel,						# 3
						QuestLevel,						# 4
						Type,							# 5
						QuestFlags,						# 6
						StartScript,					# 7
						CompleteScript,					# 8
						[								# 9
							RequiredClasses,			# 9.0
							RequiredRaces,				# 9.1
							RequiredSkills,				# 9.2[0:1]
							RequiredRep					# 9.3[0:3]
						],
						[								# 10
							RepObjectiveFaction,		# 10.0
							RepObjectiveValue,			# 10.1
							ReqItemIds,					# 10.2[0:3]
							ReqSourceIds,				# 10.3[0:3]
							ReqCreatureOrGOIds,			# 10.4[[0:3], [0:3]]
							ReqSpellCasts,				# 10.5[0:3]
							[							# 10.6 POI
								PointMapId,				# 10.6.0
								PointX,					# 10.6.1
								PointY					# 10.6.2
							]
						],
						[								# 11
							PrevQuestId,				# 11.0
							NextQuestId,				# 11.1
							NextQuestInChain,			# 11.2
							ExclusiveGroup				# 11.3
						],
						CreatureOrGOOrItemQuestStart,	# 12 [[Creatures], [Gameobjects], [Items]]
						CreatureOrGOQuestEnd,			# 13 [[Creatures], [Gameobjects]]
						areatrigger,					# 14
						SrcItemId						# 15
					]
"""

def formQuestsLookup(questList):
	list = []
	checked = []
	for x in questList:
		if x[1] not in checked:
			checked.append(x[1])
			list.append([x[1], [(x[0], x[2], x[11], x[9][1])]])
		else:
			for y in list:
				if y[0] == x[1]:
					y[1].append((x[0], x[2], x[11], x[9][1]))
	return list

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

def getFaction(bitfield):
	if bitfield == 0:
		return "AH"
	races = unpackBitMask(bitfield)
	alliance = [0, 2, 3, 6, 10]
	horde = [1, 4, 5, 7, 9]
	a = False
	h = False
	for r in alliance:
		if r in races:
			a = True
			break
	for r in horde:
		if r in races:
			h = True
			break
	factions = ""
	if a:
		factions += "A"
	if h:
		factions += "H"
	return factions

def writeQuestLookupFile(quests, file="Zeug/questLookup.lua"):
	outfile = open(file, "w")
	outfile.write("questLookup = {\n")

	for quest in quests:
		outfile.write("\t[\""+escapeName(quest[0])+"\"] = ")
		if len(quest[1]) > 1:
			outfile.write("{\n")
			for id in quest[1]:
				outfile.write("\t\t["+str(id[0])+"] = {\""+objectivesText(id[1])+"\", "+str(id[2][0])+", "+str(id[2][1])+", "+str(id[2][2])+", "+str(id[2][3])+", \""+getFaction(id[3])+"\"},\n")
			outfile.write("\t},\n")
		else:
			outfile.write("{\n")
			for id in quest[1]:
				outfile.write("\t\t["+str(id[0])+"] = {\"\", "+str(id[2][0])+", "+str(id[2][1])+", "+str(id[2][2])+", "+str(id[2][3])+", \""+getFaction(id[3])+"\"},\n")
			outfile.write("\t},\n")
	outfile.write("}\n")

# research function, not in use now
def findWeirdQuests(questList):
	questIds = []
	for quest in questList:
		if ((quest[2] != "") and (quest[6] != 2) and (quest[7] == 0) and (quest[8] == 0) and (quest[9][3] == []) and (quest[10][0] == 0) and (quest[10][2] == []) and (quest[10][2] == []) and (quest[10][3] == []) and (quest[10][4] == [[], []]) and (quest[14] == 0)):
			if ("Speak" in quest[2]) or ("speak" in quest[2])or ("Report" in quest[2]) or ("report" in quest[2]) or ("Talk" in quest[2]) or ("talk" in quest[2]):
				continue
			questIds.append(quest[0])
	return questIds

def findMultiQuestPoint(quests):
	ids = []
	for quest in quests: #12.3,13.2
		#if (len(quest[12][0])+len(quest[12][1])+len(quest[12][2])) > 1:
			#ids.append(quest[0])
			#continue
		if (len(quest[13][0])+len(quest[13][1])) > 1:
			ids.append(quest[0])
	return ids

def findDoubleQuests(questList):
	list = []
	checked = []
	for x in questList:
		if x[1] not in checked:
			checked.append(x[1])
		else:
			done = False
			for y in list:
				if y[0] == x[1]:
					y[1].append(x[0])
					done = True
			if not done:
				first = 0
				for z in questList:
					if z[1] == x[1]:
						first = z[0]
						break
				list.append([x[1], [first, x[0]]])
	return list

def checkIdentity(doubleQuests, questList):
	uncertain = []
	for questPack in doubleQuests:
		newPack = []
		uPack = []
		for quest in questList:
			if quest[0] in questPack[1]:
				newPack.append(quest)
		for quest in newPack:
			for quest2 in newPack:
				if (quest[0] != quest2[0]) and (quest[2] == quest2[2]) and (quest[11][3] != quest2[11][3]) and (quest[13] == quest2[13]) and (quest[0] not in uPack):
					uPack.append(quest[0])
		if uPack != []:
			uncertain.append(uPack)
	return uncertain

def checkIdentitx(doubleQuests, questList):
	uncertain = []
	for questPack in doubleQuests:
		newPack = []
		uPack = []
		for quest in questList:
			if quest[0] in questPack[1]:
				newPack.append(quest)
		for quest in newPack:
			for quest2 in newPack:
				if (quest[0] != quest2[0]) and (quest[9][1] == quest2[9][1]) and (quest[2] == quest2[2]) and (quest[0] not in uPack):
					uPack.append(quest[0])
		if uPack != []:
			uncertain.append(uPack)
	return uncertain

"""

######################################
NPC functions
######################################

"""
instanceKey = [	(1581, 40),
				(796, 85),
				(2557, 357),
				(1977, 33),
				(717, 1519),
				(209, 130),
				(722, 17),
				(2057, 28),
				(1583, 46),
				(1585, 46),
				(1337, 3),
				(718, 17),
				(2100, 405),
				(3456, 139),
				(491, 17),
				(719, 331),
				(2257, 1537),
				(1477, 8),
				(1176, 440),
				(721, 1),
				(2677, 46),
				(2159, 15),
				(2017, 139),
				(2437, 1637),
				(2717, 46),
				(2918, 1519),
				(2917, 1637),
				(3429, 1377),
				(3428, 1377),
				(25, 46)]

def calculateWorldInstanceCoords(zoneId, x, y):
	for mapSet in mapBorders:
		zone = int(mapSet[0])
		mId = int(mapSet[2])
		x1 = float(mapSet[5])
		x2 = float(mapSet[6])
		y1 = float(mapSet[3])
		y2 = float(mapSet[4])
		for instance in instanceKey:
			if instance[0] == zoneId:
				zoneX = instance[1]
				for mapSet2 in mapBorders:
					if (mapSet2[0] == zoneX)and (x < x1) and (x > x2) and (y < y1) and (y > y2):
						xCoord = round(abs((x-x1)/(x2-x1)*100), 2)
						yCoord = round(abs((y-y1)/(y2-y1)*100), 2)
						return (zoneX, yCoord, xCoord)

	return False

def calculateCoords(point): # 0: id, 1: guid, 2: map, 3: x, 4: y, 5: zone
	for mapSet in mapBorders:
		zone = mapSet[0]
		mapId = mapSet[2]
		x1 = mapSet[5]
		x2 = mapSet[6]
		y1 = mapSet[3]
		y2 = mapSet[4]
		if (mapId == point[2]) and (point[3] < x1) and (point[3] > x2) and (point[4] < y1) and (point[4] > y2) and (zone == point[5]):
			xCoord = round(abs((point[3]-x1)/(x2-x1)*100), 2)
			yCoord = round(abs((point[4]-y1)/(y2-y1)*100), 2)
			z = (zone, yCoord, xCoord)
			return z

	for instance in instanceIds:
		zoneId = int(instance[0])
		mapId = int(instance[2])
		# test for zoneId here instead?
		if (mapId == point[2]):
			z = [zoneId, -1, -1]
			return z
		elif (zoneId == point[5]) and ((point[2] == 0) or (point[2] == 1)):
			z = calculateWorldInstanceCoords(point[5], point[3], point[4])
			if z:
				return z
			else:
				print("Instance error for", end=": ")
				print(point)
				return False
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
	print("Error with coordinates for", end=":")
	print(point)
	return False

def sortNPCTables(npc_table, npc_zones):
	#npc_tpl = npc_table[0]
	#npc = npc_table[1]
	#npc_start = npc_table[2]
	#npc_end = npc_table[3]
	#npc_mov = npc_table[4]
	#npc_mov_tpl = npc_table[5]
	
	print("Sort zone and spawn tables together...")
	npcNew = [] # 0: id, 1: guid, 2: map, 3: x, 4: y, 5: zone
	countdown = len(npc_table[1])
	for x in npc_table[1]:
		for y in npc_zones[0]:
			if x[4] == y[1]:
				npcNew.append([x[0], x[4], x[1], x[2], x[3], y[0]])
				break
		if (countdown%500 == 0):
			print(str(countdown), end=",")
		countdown -= 1
	print("Done.")
	
	print("Merge everything else...")
	npcs = []
	countdown = len(npc_table[0])
	for x in npc_table[0]:
		entry = x[0]
		name = x[1]
		minlevel = x[2]
		maxlevel = x[3]
		minlevelhealth = x[4]
		maxlevelhealth = x[5]
		rank = x[6]
		
		# get spawns for this npc
		spawns = []
		for y in npcNew:
			# 0: id, 1: guid, 3: x, 4: y, 5: zone
			if y[0] == entry:
				spawns.append(calculateCoords(y))
		
		
		spawnsSorted = []
		zones = []
		for y in spawns:
			if y == False:
				continue
			elif y[0] in zones:
				for z in spawnsSorted:
					if z[0] == y[0]:
						z[1].append([y[1], y[2]])
						break
			else:
				spawnsSorted.append([y[0], [[y[1], y[2]]]])
				zones.append(y[0])
		zone = 0
		longest = 0
		if len(zones) == 0:
			#print("Error with NPC "+name+"("+str(entry)+"): No zones!")
			continue
		elif len(zones) == 1:
			zone = zones[0]
		else:
			for z in spawnsSorted:
				if len(z[1]) > longest:
					longest = len(z[1])
					zone = z[0]
		if (countdown%200 == 0):
			print(str(countdown))
		countdown -= 1
		npcs.append([entry, name, minlevel, maxlevel, minlevelhealth, maxlevelhealth, rank, spawnsSorted, zone])
	print("Done.")
	return npcs

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
	cursor.execute("SELECT point, entry, position_x, position_y FROM creature_movement_template")
	npc_mov_tpl = []
	for a in cursor.fetchall():
		npc_mov_tpl.append(a)
	print("Done.")

	return [npc_tpl, npc, npc_start, npc_end, npc_mov, npc_mov_tpl]
"""


######################################
Item functions
######################################



"""
def getItemTables(cursor):
	print("Selecting MySQL tables...")

	cursor.execute("SELECT entry, item, ChanceOrQuestChance, groupid, mincountOrRef FROM creature_loot_template")
	npc_loot_tpl = []
	for a in cursor.fetchall():
		npc_loot_tpl.append(a)

	cursor.execute("SELECT entry, item, ChanceOrQuestChance, groupid, mincountOrRef FROM gameobject_loot_template")
	obj_loot_tpl = []
	for a in cursor.fetchall():
		obj_loot_tpl.append(a)

	cursor.execute("SELECT entry, item, ChanceOrQuestChance, groupid, mincountOrRef FROM item_loot_template")
	item_loot_tpl = []
	for a in cursor.fetchall():
		item_loot_tpl.append(a)

	cursor.execute("SELECT entry, item, ChanceOrQuestChance, groupid, mincountOrRef FROM reference_loot_template")
	ref_loot_tpl = []
	for a in cursor.fetchall():
		ref_loot_tpl.append(a)

	cursor.execute("SELECT entry, name, Flags FROM item_template")
	item_tpl = []
	for a in cursor.fetchall():
		item_tpl.append(a)

	cursor.execute("SELECT entry, data1 FROM gameobject_template WHERE type = 3")
	obj_tpl = []
	for a in cursor.fetchall():
		obj_tpl.append(a)

	cursor.execute("SELECT entry, LootId FROM creature_template") # PickpocketLootId and SkinningLootId might be good...
	npc_tpl = []
	for a in cursor.fetchall():
		npc_tpl.append(a)

	print("Done.")

	return [item_tpl, npc_loot_tpl, obj_loot_tpl, item_loot_tpl, ref_loot_tpl, npc_tpl, obj_tpl]

# entry, item, ChanceOrQuestChance, groupid, mincountOrRef
def getRefGroup(refLootTable, entry, chance):
	newTable = [] # (item, ChanceOrQuestChance)
	groupProcessed = [] # groupId
	for x in refLootTable:
		if x[0] == entry:
			if x[3] == 0:# not grouped
				# currently there are no other cases to cover here
				newTable.append((x[1], abs(x[2]*(chance/100))))
			else:# grouped
				if x[3] in groupProcessed:
					continue
				else:
					groupProcessed.append(x[3])
					for y in getLootGroup(refLootTable, refLootTable, entry, x[3]):
						newTable.append((y[0], abs(y[1]*(chance/100))))
	return newTable

def getLootGroup(lootTable, refLootTable, entry, groupId):
	newTable = []
	chance = 100
	for x in lootTable:
		if x[0] == entry and x[3] == groupId:
			if x[4] < 0:# reference
				for y in getRefGroup(refLootTable, abs(x[4]), abs(x[2])):
					newTable.append(y)
			else:
				chance -= abs(x[2])
				newTable.append((x[1], abs(x[2])))
	newerTable = []
	numZeroChance = 0
	for x in newTable:
		if x[1] == 0:
			numZeroChance += 1
	if chance < 0:
		print("\nChance "+str(chance)+" for entry:"+str(entry)+", group: "+str(groupId)+", numZeroChance: "+str(numZeroChance))
	if numZeroChance > 0:
		newChance = chance/numZeroChance
	for x in newTable:
		if x[1] == 0:
			newerTable.append((x[0], newChance))
		else:
			newerTable.append(x)
	return newerTable

def getLootEntry(lootTable, refLootTable, entry):
	newTable = []
	groupProcessed = []
	for x in lootTable:
		if x[0] == entry:
			if x[3] == 0:# not grouped
				if x[4] > 0:# no reference
					newTable.append((x[1], abs(x[2])))
				else: # reference
					for y in getRefGroup(refLootTable, abs(x[4]), abs(x[2])):
						newTable.append(y)
			else: # grouped
				if x[3] in groupProcessed:
					continue
				else:
					groupProcessed.append(x[3])
					for y in getLootGroup(lootTable, refLootTable, entry, x[3]):
						newTable.append(y)
	return newTable

def sortLootTable(lootTable, refLootTable):
	newTable = []
	processed = []
	count = len(lootTable)
	for x in lootTable:
		count -= 1
		if count % 1000 == 0:
			print(count, end="... ")
		if x[0] in processed:
			continue
		else:
			newTable.append([x[0], getLootEntry(lootTable, refLootTable, x[0]), []])
			processed.append(x[0])
	return newTable

def checkForItem(newLootTable, item):
	for x in newLootTable:
		if x[0] == item:
			return x[1]
	return False

def sortItemTables(itemTables):
	print("Sorting NPC loot tables...")
	npcs = sortLootTable(itemTables[1], itemTables[4])
	print("\nAdding NPC ID's...")
	for x in npcs:
		for y in itemTables[5]:
			if y[1] == x[0]:
				x[2].append(y[0])
	print("Done.")

	print("Sorting Object loot tables...")
	objs = sortLootTable(itemTables[2], itemTables[4])
	print("\nAdding Object ID's...")
	for x in objs:
		for y in itemTables[6]:
			if y[1] == x[0]:
				x[2].append(y[0])
	print("Done.")

	print("Sorting Item loot tables...")
	items = sortLootTable(itemTables[3], itemTables[4])
	print("\nDone.")

	print("Sorting tables per item...")
	drops = []
	count = len(itemTables[0])
	for item in itemTables[0]:
		foundDrop = False
		newItem = [item[0], item[1], [], [], []]
		for npc in npcs:
			foundChance = checkForItem(npc[1], item[0])
			if foundChance:
				foundDrop = True
				for id in npc[2]:
					newItem[2].append((id, foundChance))
		for obj in objs:
			foundChance = checkForItem(obj[1], item[0])
			if foundChance:
				foundDrop = True
				for id in obj[2]:
					newItem[3].append((id, foundChance))
		for itm in items:
			for x in itm[1]:
				if x[0] == item[0]:
					newItem[4].append((itm[0], x[1]))
					foundDrop = True
		if foundDrop:
			drops.append(newItem)
		count -= 1
		if count % 100 == 0:
			print(count, end="... ")
	print("\nDone.")

	return drops

def writeItemFile(items, file="Zeug/itemData.lua"):
	outfile = open(file, "w")

	outfile.write("itemLookup = {\n")
	for item in items:
		id = item[0]
		name = escapeName(item[1])
		outfile.write("\t['"+name+"'] = "+str(id)+",\n")
	outfile.write("}\n")

	outfile.write("itemData = {\n")
	for item in items:
		id = item[0]
		name = escapeName(item[1])
		outfile.write("\t["+str(id)+"] = {\n")

		if item[2] != []:
			outfile.write("\t\t['npcs'] = {")
			for npc in item[2]:
				outfile.write("{"+str(npc[0])+","+str(round(abs(npc[1]), 2))+"},")
			outfile.write("},\n")

		if item[3] != []:
			outfile.write("\t\t['objects'] = {")
			for object in item[3]:
				outfile.write("{"+str(object[0])+","+str(round(abs(object[1]), 2))+"},")
			outfile.write("},\n")

		if item[4] != []:
			outfile.write("\t\t['items'] = {")
			for itm in item[4]:
				outfile.write("{"+str(itm[0])+","+str(round(abs(itm[1]), 2))+"},")
			outfile.write("},\n")

		outfile.write("\t},\n")
	outfile.write("}")
