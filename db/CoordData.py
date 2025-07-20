import json
import re
import csv

"""

DBC functions

"""

# TODO: Use proper CSV reader
def getAreaTriggers(version):
    file_path = f'data/{version}/AreaTrigger.dbc.CSV'
    with open(file_path, 'r') as infile:
        file_content = infile.read()
    rows = re.findall("(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),?\n", file_content)
    areaTrigger = []
    for row in rows:
        if row[0] == 'ID':
            continue
        areaTrigger.append((int(row[0]), int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])))
    print(f'Found {len(areaTrigger)} area triggers in {file_path}')
    return areaTrigger

def getMapBorders(version):
    reader = csv.reader(open(f'data/{version}/WorldMapArea.dbc.CSV', 'r'))
    wma = []
    """(zoneId, zoneName, mapId, minX, maxX, minY, maxY)"""
    for row in reader:
        wma.append((int(row[2]), row[3], int(row[1]), float(row[4]), float(row[5]), float(row[6]), float(row[7])))
    return wma

def get_retail_like_map_borders(version):
    area_table = {}
    with open(f'data/{version}/AreaTable.dbc.CSV', 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            area_table[row['ID']] = row

    ui_map = {}
    with open(f'data/{version}/UiMap.dbc.CSV', 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            ui_map[row['ID']] = row

    ui_map_assignments = []
    with open(f'data/{version}/UiMapAssignment.dbc.CSV', 'r') as infile:
        """(UiMin_0,UiMin_1,UiMax_0,UiMax_1,Region_0,Region_1,Region_2,Region_3,Region_4,Region_5,ID,UiMapID,OrderIndex,MapID,AreaID,WMODoodadPlacementID,WMOGroupID)"""
        reader = csv.DictReader(infile)
        """Region_0=maxY, Region_1=maxX, Region_3=minY, Region_4=minX"""
        for row in reader:
            if row['OrderIndex'] != '0':
                continue
            area_id = int(row['AreaID'])
            ui_map_id = row['UiMapID']
            if area_id == 0:
                # Some entries in UiMapAssignment have AreaID 0, even though there is an areaId in AreaTable.
                # So we search for it by the zone name.
                if ui_map_id not in ui_map:
                    print(f'Warning: UiMapID {ui_map_id} not found in UiMap table for AreaID 0.')
                    continue
                name_lang = ui_map[ui_map_id]['Name_lang']
                for mop_area_id, area in area_table.items():
                    if area['AreaName_lang'] == name_lang:
                        area_id = int(mop_area_id)
                        # no break to get the last value if there are multiple matches

            """(zoneId, zoneName, mapId, minX, maxX, minY, maxY)"""
            ui_map_assignments.append((area_id, "None", int(row['MapID']), float(row['Region_4']), float(row['Region_1']), float(row['Region_3']), float(row['Region_0'])))
    return ui_map_assignments

"""

These IDs are used to determine if a coordinate is on an instance map (that doesn't have an ingame map)

"""


# Values are taken from AreaTable.dbc - (ID, ZoneName; ContinentID)
"""(zoneId, name, mapId)"""
instanceIds = [ (206, 'UtgardeKeep', 574),
                (209, 'ShadowfangKeep', 33),
                (491, 'RazorfenKraul', 47),
                (717, 'TheStockade', 34),
                (718, 'WailingCaverns', 43),
                (719, 'BlackfathomDeeps', 48),
                (721, 'Gnomeregan', 90),
                (722, 'RazorfenDowns', 129),
                (796, 'ScarletMonastery', 189),
                (1176, 'ZulFarrak', 209),
                (1196, 'UtgardePinnacle', 575),
                (1337, 'Uldaman', 70),
                (1477, 'TheTempleOfAtalHakkar', 109),
                (1581, 'TheDeadmines', 36),
                (1583, 'BlackrockSpire', 229),
                (1584, 'BlackrockDepths', 230),
                (1977, 'ZulGurub', 309),
                (1977, 'ZulGurub', 859),
                (2017, 'Stratholme', 329),
                (2057, 'Scholomance', 289),
                (2100, 'Maraudon', 349),
                (2159, 'OnyxiasLair', 249),
                (2366, 'CoTTheBlackMorass', 269),
                (2367, 'CoTHillsbradFoothills', 560),
                (2437, 'Ragefire', 389),
                (2557, 'DireMaul', 429),
                #(2597, 'AlteracValley', 30),
                (2677, 'BlackwingLair', 469),
                (2717, 'MoltenCore', 409),
                #(3277, 'WarsongGulch', 489),
                #(3358, 'ArathiBasin', 529),
                (3428, 'AhnQiraj', 531),
                (3429, 'RuinsofAhnQiraj', 509),
                (3456, 'Naxxramas', 533),
                (3457, 'Karazhan', 532),
                (3562, 'HellfireRamparts', 543),
                (3606, 'CoTMountHyjal', 534),
                (3607, 'CoilfangReservoir', 548),
                (3713, 'TheBloodFurnace', 542),
                (3714, 'TheShatteredHalls', 540),
                (3715, 'TheSteamvault', 545),
                (3716, 'TheUnderbog', 546),
                (3717, 'TheSlavePens', 547),
                (3789, 'ShadowLabyrinth', 555),
                (3790, 'AuchenaiCrypts', 558),
                (3791, 'SethekkHalls', 556),
                (3792, 'ManaTombs', 557),
                (3805, 'ZulAman', 568),
                #(3820, 'NetherstormArena', 566),
                (3836, 'MagtheridonsLair', 544),
                (3845, 'TempestKeep', 550),
                (3847, 'TheBotanica', 553),
                (3848, 'TheArcatraz', 552),
                (3849, 'TheMechanar', 554),
                (3923, 'GruulsLair', 565),
                (3959, 'BlackTemple', 564),
                (4075, 'SunwellPlateau', 580),
                (4100, 'CoTStratholme', 595),
                (4131, 'MagistersTerrace', 585),
                (4196, 'DrakTharonKeep', 600),
                (4228, 'Nexus80', 578),
                (4264, 'Ulduar77', 599),
                (4265, 'TheNexus', 576),
                (4265, 'TheNexusLegendary', 951),
                (4272, 'HallsofLightning', 602),
                (4273, 'Ulduar', 603),
                (4277, 'AzjolNerub', 601),
                # (4298, 'ScarletEnclave', 609),
                #(4384, 'StrandoftheAncients', 607),
                (4415, 'VioletHold', 608),
                (4416, 'Gundrak', 604),
                (4493, 'TheObsidianSanctum', 615),
                (4494, 'Ahnkahet', 619),
                (4500, 'TheEyeofEternity', 616),
                (4603, 'VaultofArchavon', 624),
                #(4710, 'IsleofConquest', 628),
                # (4714, 'Gilneas', 654),
                # (4714, 'GilneasX', 638),
                # (4714, 'Gilneas_terrain1', 654),
                # (4714, 'Gilneas_terrain2', 654),
                # (4720, 'TheLostIsles', 648),
                # (4720, 'TheLostIsles_terrain1', 648),
                # (4720, 'TheLostIsles_terrain2', 648),
                (4722, 'TheArgentColiseum', 649),
                (4723, 'TheArgentColiseum', 650),
                # (4737, 'Kezan', 648),
                # (4755, 'GilneasCity', 654),
                (4809, 'TheForgeofSouls', 632),
                (4812, 'IcecrownCitadel', 631),
                (4813, 'PitofSaron', 658),
                (4820, 'HallsofReflection', 668),
                (4926, 'BlackrockCaverns', 645),
                (4945, 'HallsofOrigination', 644),
                (4950, 'GrimBatol', 670),
                (4987, 'TheRubySanctum', 724),
                (5004, 'ThroneofTides', 643),
                #(5031, 'TwinPeaks', 726),
                (5035, 'Skywall', 657),
                # (5042, 'Deepholm', 646),
                (5088, 'TheStonecore', 725),
                (5094, 'BlackwingDescent', 669),
                (5095, 'TolBarad', 732),
                #(5108, 'BattleforGilneas', 728),
                (5334, 'TheBastionofTwilight', 671),
                # (5389, 'TolBaradDailyArea', 732),
                (5396, 'LostCityofTolvir', 755),
                (5416, 'TheMaelstrom', 730),
                #(5449, 'GilneasBattleground2', 761),
                (5600, 'BaradinHold', 757),
                (5630, 'TheMaelstromContinent', -1),
                (5638, 'ThroneoftheFourWinds', 754),
                (5723, 'Firelands', 720),
                # (5733, 'MoltenFront', 861),
                (5788, 'WellofEternity', 939),
                (5789, 'EndTime', 938),
                #(5799, 'NetherstormArena', 968),
                (5844, 'HourofTwilight', 940),
                # (5861, 'DarkmoonFaireIsland', 974),
                (5892, 'DragonSoul', 967),
                (5975, 'TempleoftheJadeSerpent', 960),
                (6001, 'StormstoutBrewery', -1),
                (6052, 'ScarletHalls', 1001),
                (6066, 'Scholomance', 1007),
                (6125, 'MogushanVaults', 1008),
                (6173, 'ShadoPanMonastery', -1),
                (6182, 'MogushanPalace', 994),
                (6214, 'SiegeofNiuzaoTemple', 1011),
                (6396, 'GateoftheSettingSunGV', -1),
                (6435, 'HeartofFear', -1),
                (6515, 'TerraceofEndlessSpring', 996),
                (6622, 'ThunderKingRaid', 1098),
                (6738, 'OrgrimmarRaid', 1136),
              ]

"""

Map borders

"""

mapBordersClassic = getMapBorders('classic')

mapBordersTBC = getMapBorders('tbc')

mapBordersWotLK = getMapBorders('wotlk')

mapBordersCata = getMapBorders('cata')

mapBordersMoP = get_retail_like_map_borders('mop')

mapBordersTWW = getMapBorders('tww')

# Read npc_zone_id_data.json into a map. The format of each entry in the map is (npcId, zoneId)
# This file is generated by the npc_zone_id_spider in Questie
npcZoneIdMap = {}
with open('data/cata/npc_zone_id_data.json', 'r') as f:
    data = json.load(f)
    for d in data:
        npcZoneIdMap[int(d['npcId'])] = int(d['zoneId'])

objectZoneIdMap = {}
with open('data/cata/object_zone_id_data.json', 'r') as f:
    data = json.load(f)
    for d in data:
        objectZoneIdMap[int(d['objectId'])] = int(d['zoneId'])

zoneNames = {}
for m in mapBordersCata:
    zoneNames[m[0]] = m[1]

"""

These zoneIds are subzones on the world (continent) maps.

Used to prevent the print function from printing a long list of {-1, -1} for instance spawns

"""

# Classic
#validZoneList = [1, 3, 4, 8, 10, 11, 12, 14, 15, 16, 17, 28, 33, 36, 38, 40, 41, 44, 45, 46, 47, 51,             85, 130, 139, 141, 148,           215, 267, 331, 357, 361,      400, 405, 406, 440, 490, 493,           618,       1377, 1497, 1519, 1537, 1637, 1638, 1657, 2597,       3277, 3358]
#validZoneList = [1, 3, 4, 8, 10, 11, 12, 14, 15, 16, 17, 28, 33, 36, 38, 40, 41, 44, 45, 46, 47, 51, 65, 66, 67, 85, 130, 139, 141, 148, 206, 210, 215, 267, 331, 357, 361, 394, 400, 405, 406, 440, 490, 493, 495,      618, 1196, 1377, 1497, 1519, 1537, 1637, 1638, 1657, 2597, 2817, 3277, 3358, 3430, 3433, 3456, 3483, 3487, 3518, 3519, 3520, 3521, 3522, 3523, 3524, 3525, 3537, 3557, 3703, 3711, 3820, 4080, 4100, 4196, 4197, 4228, 4264, 4265, 4272, 4273, 4277, 4298, 4384, 4395, 4415, 4416, 4493, 4494, 4500, 4603,             4710,             4722, 4723,       4742,       4809, 4812, 4813,       4820,       4987]
#validZoneList =  [1, 3, 4, 8, 10, 11, 12, 14, 15, 16, 17, 28, 33, 36, 38, 40, 41, 44, 45, 46, 47, 51, 65, 66, 67, 85, 130, 139, 141, 148, 206, 210, 215, 267, 331, 357, 361, 394, 400, 405, 406, 440, 490, 493, 495, 616, 618, 1196, 1377, 1497, 1519, 1537, 1637, 1638, 1657, 2597, 2817, 3277, 3358, 3430, 3433, 3456, 3483, 3487, 3518, 3519, 3520, 3521, 3522, 3523, 3524, 3525, 3537, 3557, 3703, 3711, 3820, 4080, 4100, 4196, 4197, 4228, 4264, 4265, 4272, 4273, 4277, 4298, 4384, 4395, 4415, 4416, 4493, 4494, 4500, 4603, 4706, 4709, 4710, 4714, 4720, 4722, 4723, 4737, 4742, 4755, 4809, 4812, 4813, 4815, 4820, 4922, 4987, 5034, 5042, 5144, 5145, 5146, 5287, 5339, 5351, 5389, 5695, 5733, 5861]

validZoneList = [k for k in range(1, 9999)]
"""

Unused data

"""

"""(zoneId, zoneName, mapId, minX, maxX, minY, maxY)"""
m1 = [
    (1, 'Dun Morogh', 0, 1802.08325195313, -3122.91650390625, -3877.08325195313, -7160.41650390625),
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
    (1657, 'Darnassus', 1, 2938.36279296875, 1880.02954101563, 10238.31640625, 9532.5869140625),
    (2597, 'Alterac Valley', 30, 1781.24987792969, -2456.25, 1085.41662597656, -1739.58325195313),
    (3277, 'Warsong Gulch', 489, 2041.66662597656, 895.833312988281, 1627.08325195313, 862.499938964844),
    (3358, 'Arathi Basin', 529, 1858.33325195313, 102.08332824707, 1508.33325195313, 337.5),
]

"""TBC (?,mapID,zoneID,zoneName,?,?,?,?,?)"""
mb2 = [(4,1,14,'Durotar',-1962.4999,-7249.9995,1808.3333,-1716.6666,-1),
(9,1,215,'Mulgore',2047.9166,-3089.5833,-272.91666,-3697.9165,-1),
(11,1,17,'Barrens',2622.9165,-7510.4165,1612.4999,-5143.75,-1),
(15,0,36,'Alterac',783.3333,-2016.6666,1500,-366.66666,-1),
(16,0,45,'Arathi',-866.6666,-4466.6665,-133.33333,-2533.3333,-1),
(17,0,3,'Badlands',-2079.1665,-4566.6665,-5889.583,-7547.9165,-1),
(19,0,4,'BlastedLands',-1241.6666,-4591.6665,-10566.666,-12800,-1),
(20,0,85,'Tirisfal',3033.3333,-1485.4166,3837.4998,824.99994,-1),
(21,0,130,'Silverpine',3449.9998,-750,1666.6666,-1133.3333,-1),
(22,0,28,'WesternPlaguelands',416.66666,-3883.3333,3366.6665,499.99997,-1),
(23,0,139,'EasternPlaguelands',-2185.4165,-6056.25,3799.9998,1218.75,-1),
(24,0,267,'Hilsbrad',1066.6666,-2133.3333,400,-1733.3333,-1),
(26,0,47,'Hinterlands',-1575,-5425,1466.6666,-1100,-1),
(27,0,1,'DunMorogh',1802.0833,-3122.9165,-3877.0833,-7160.4165,-1),
(28,0,51,'SearingGorge',-322.91666,-2554.1665,-6100,-7587.4995,-1),
(29,0,46,'BurningSteppes',-266.66666,-3195.8333,-7031.2495,-8983.333,-1),
(30,0,12,'Elwynn',1535.4166,-1935.4166,-7939.583,-10254.166,-1),
(32,0,41,'DeadwindPass',-833.3333,-3333.3333,-9866.666,-11533.333,-1),
(34,0,10,'Duskwood',833.3333,-1866.6666,-9716.666,-11516.666,-1),
(35,0,38,'LochModan',-1993.7499,-4752.083,-4487.5,-6327.083,-1),
(36,0,44,'Redridge',-1570.8333,-3741.6665,-8575,-10022.916,-1),
(37,0,33,'Stranglethorn',2220.8333,-4160.4165,-11168.75,-15422.916,-1),
(38,0,8,'SwampOfSorrows',-2222.9165,-4516.6665,-9620.833,-11150,-1),
(39,0,40,'Westfall',3016.6665,-483.3333,-9400,-11733.333,-1),
(40,0,11,'Wetlands',-389.5833,-4525,-2147.9165,-4904.1665,-1),
(41,1,141,'Teldrassil',3814.5833,-1277.0833,11831.25,8437.5,-1),
(42,1,148,'Darkshore',2941.6665,-3608.3333,8333.333,3966.6665,-1),
(43,1,331,'Ashenvale',1699.9999,-4066.6665,4672.9165,829.1666,-1),
(61,1,400,'ThousandNeedles',-433.3333,-4833.333,-3966.6665,-6899.9995,-1),
(81,1,406,'StonetalonMountains',3245.8333,-1637.4999,2916.6665,-339.5833,-1),
(101,1,405,'Desolace',4233.333,-262.5,452.0833,-2545.8333,-1),
(121,1,357,'Feralas',5441.6665,-1508.3333,-2366.6665,-6999.9995,-1),
(141,1,15,'Dustwallow',-974.99994,-6225,-2033.3333,-5533.333,-1),
(161,1,440,'Tanaris',-218.74998,-7118.7495,-5875,-10475,-1),
(181,1,16,'Aszhara',-3277.0833,-8347.916,5341.6665,1960.4166,-1),
(182,1,361,'Felwood',1641.6666,-4108.333,7133.333,3299.9998,-1),
(201,1,490,'UngoroCrater',533.3333,-3166.6665,-5966.6665,-8433.333,-1),
(241,1,493,'Moonglade',-1381.25,-3689.5833,8491.666,6952.083,-1),
(261,1,1377,'Silithus',2537.5,-945.834,-5958.334,-8281.25,-1),
(281,1,618,'Winterspring',-316.66666,-7416.6665,8533.333,3799.9998,-1),
(301,0,1519,'Stormwind',1380.9714,36.70063,-8278.851,-9175.205,-1),
(321,1,1637,'Ogrimmar',-3680.601,-5083.2056,2273.8772,1338.4606,-1),
(341,0,1537,'Ironforge',-713.5914,-1504.2164,-4569.241,-5096.8457,-1),
(362,1,1638,'ThunderBluff',516.6666,-527.0833,-849.99994,-1545.8333,-1),
(381,1,1657,'Darnassis',2938.3628,1880.0295,10238.316,9532.587,-1),
(382,0,1497,'Undercity',873.1926,-86.1824,1877.9453,1237.8412,-1),
(401,30,2597,'AlteracValley',1781.2499,-2456.25,1085.4166,-1739.5833,-1),
(443,489,3277,'WarsongGulch',2041.6666,895.8333,1627.0833,862.49994,-1),
(461,529,3358,'ArathiBasin',1858.3333,102.08333,1508.3333,337.5,-1),
(462,530,3430,'EversongWoods',-4487.5,-9412.5,11041.666,7758.333,0),
(463,530,3433,'Ghostlands',-5283.333,-8583.333,8266.666,6066.6665,0),
(464,530,3524,'AzuremystIsle',-10500,-14570.833,-2793.75,-5508.333,1),
(465,530,3483,'Hellfire',5539.583,375,1481.25,-1962.4999,-1),
(467,530,3521,'Zangarmarsh',9475,4447.9165,1935.4166,-1416.6666,-1),
(471,530,3557,'TheExodar',-11066.367,-12123.138,-3609.6833,-4314.371,1),
(473,530,3520,'ShadowmoonValley',4225,-1275,-1947.9166,-5614.583,-1),
(475,530,3522,'BladesEdgeMountains',8845.833,3420.8333,4408.333,791.6666,-1),
(476,530,3525,'BloodmystIsle',-10075,-13337.499,-758.3333,-2933.3333,1),
(477,530,3518,'Nagrand',10295.833,4770.833,41.666664,-3641.6665,-1),
(478,530,3519,'TerokkarForest',7083.333,1683.3333,-999.99994,-4600,-1),
(479,530,3523,'Netherstorm',5483.333,-91.666664,5456.25,1739.5833,-1),
(480,530,3487,'SilvermoonCity',-6400.75,-7612.2085,10153.709,9346.938,0),
(481,530,3703,'ShattrathCity',6135.259,4829.009,-1473.9545,-2344.7878,-1),
(482,566,3820,'NetherstormArena',2660.4165,389.5833,2918.75,1404.1666,-1),
(499,530,4080,'Sunwell',-5302.083,-8629.166,13568.749,11350,0),]

continentBorders = [(5, 'Eastern Kingdoms', 0, 16000, -19199.900390625, 7466.60009765625, -16000),
                    (6, 'Kalimdor', 1, 17066.599609375, -19733.2109375, 12799.900390625, -11733.2998046875),
                    (2597, 'Alterac Valley', 30, 1781.24987792969, -2456.25, 1085.41662597656, -1739.58325195313),
                    (3277, 'Warsong Gulch', 489, 2041.66662597656, 895.833312988281, 1627.08325195313, 862.499938964844),
                    (3358, 'Arathi Basin', 529, 1858.33325195313, 102.08332824707, 1508.33325195313, 337.5),]


"""
(13,1,0,'Kalimdor',17066.6,-19733.21,12799.9,-11733.3,-1),
(14,0,0,'Azeroth',18171.97,-22569.21,11176.344,-15973.344,-1),
(466,530,0,'Expansion01',12996.039,-4468.039,5821.3594,-5821.3594,-1),
(485,571,0,'Northrend',9217.152,-8534.246,10593.375,-1240.89,-1,0,0),
"""

"""Key for zoneIds that are subzones of an instance."""
instanceKey = [ (1581, 40),
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

"""(zoneId, minLevel, maxLevel)"""
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
