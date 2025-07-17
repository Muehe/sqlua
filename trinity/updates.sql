-- According to the SkyFire DB the highest NPC ID is 80674 so we remove everything above that
DELETE FROM `creature` WHERE `id` > 80674;
DELETE FROM `creature_template` WHERE `entry` > 80674;
DELETE FROM `creature_queststarter` WHERE `id` > 80674;
DELETE FROM `creature_questender` WHERE `id` > 80674;

-- Reduce race requirements to MoP races
UPDATE `quest_template` SET `AllowableRaces` = 33555378 WHERE `AllowableRaces` = 12261800583900083122; -- Horde
UPDATE `quest_template` SET `AllowableRaces` = 18875469 WHERE `AllowableRaces` = 6130900294268439629; -- Alliance
UPDATE `quest_template` SET `AllowableRaces` = 0 WHERE `AllowableRaces` = 18446744073709551615; -- Both
UPDATE `quest_template` SET `AllowableRaces` = 33554432 WHERE `AllowableRaces` = 31012; -- Pandaren Horde
UPDATE `quest_template` SET `AllowableRaces` = 16777216 WHERE `AllowableRaces` = 16777216; -- Pandaren Alliance
UPDATE `quest_template` SET `AllowableRaces` = 8388608 WHERE `AllowableRaces` = 58720256; -- Pandaren Neutral
UPDATE `quest_template` SET `AllowableRaces` = 8388608 WHERE `AllowableRaces` = 54043195541028864; -- Pandaren Neutral

-- quest 31694 has some debug text in the objectives text and details which we remove
UPDATE quest_template SET LogDescription = '', QuestDescription = '' WHERE ID = 31694;

-- some quests have a NextQuestId which is not in the database
UPDATE quest_template_addon SET NextQuestId = 26389 WHERE Id = 31145;
UPDATE quest_template_addon SET NextQuestId = 25064 WHERE Id = 31163;

-- some quests have questflags set to a really high value
-- for odd numbers we set them to 1 to keep the repeatable flag
-- for even numbers we set them to 0
UPDATE quest_template SET Flags = 1 WHERE Flags > 524296 AND MOD(Flags, 2) = 1; -- odd
UPDATE quest_template SET Flags = 0 WHERE Flags > 524296 AND MOD(Flags, 2) = 0; -- even

-- Stormwind
UPDATE creature SET zoneId = 1519, areaId = 1519 WHERE id IN (
    60931, 61809, 61837, 62106, 62419, 65048, 65066, 65068, 65051, 68868, 65069, 65072, 69334, 70296
);

-- Darnassus
UPDATE creature SET zoneId = 1657, areaId = 1657 WHERE id IN (
    62450
);

-- Silvermoon City
UPDATE creature SET zoneId = 3487, areaId = 3487 WHERE id IN (
    68085, 68086
);

-- Orgrimmar
UPDATE creature SET zoneId = 1637, areaId = 1637 WHERE id IN (
    62445, 65008, 65058, 65060, 65061, 65063, 65065, 65071, 65074, 65076, 65078, 66022, 68869, 69333, 70301
);

-- Northshire (Human starting area)
UPDATE creature SET zoneId = 6170, areaId = 6170 WHERE id IN (
    63258
);

-- Coldridge Valley (Dwarf starting area)
UPDATE creature SET zoneId = 6176, areaId = 6176 WHERE id IN (
    63285
);

-- New Tinkertown (Gnome starting area)
UPDATE creature SET zoneId = 6457, areaId = 6457 WHERE id IN (
    63238, 63239, 63241, 63242
);

-- Deathknell (Undead starting area)
UPDATE creature SET zoneId = 6454, areaId = 6454 WHERE id IN (
    63272
);

-- Sunstrider Isle (Blood Elf starting area)
UPDATE creature SET zoneId = 6455, areaId = 6455 WHERE id IN (
    63332
);

-- Eversong Woods
UPDATE creature SET zoneId = 3430, areaId = 3430 WHERE id IN (
    62020
);

-- Teldrassil
UPDATE creature SET zoneId = 141, areaId = 141 WHERE id IN (
    62242
);

-- Ashenvale
UPDATE creature SET zoneId = 331, areaId = 331 WHERE id IN (
    62177
);

-- Feralas
UPDATE creature SET zoneId = 357, areaId = 357 WHERE id IN (
    62395, 66352, 66361, 66363, 66364, 68805
);

-- Un'Goro
UPDATE creature SET zoneId = 490, areaId = 490 WHERE id IN (
    62127, 62370, 62375
);

-- Desolace
UPDATE creature SET zoneId = 405, areaId = 405 WHERE id IN (
    62184, 62185, 62186, 62187, 66372, 66375, 66376, 66377
);

-- Silithus
UPDATE creature SET zoneId = 1377, areaId = 1377 WHERE id IN (
    61441
);

-- Mount Hyjal
UPDATE creature SET zoneId = 616, areaId = 616 WHERE id IN (
    62178, 62373
);

-- Deepholm
UPDATE creature SET zoneId = 5042, areaId = 5042 WHERE id IN (
    62181, 62182
);

-- Uldum
UPDATE creature SET zoneId = 5034, areaId = 5034 WHERE id IN (
    62523
);

-- Twilight Highlands
UPDATE creature SET zoneId = 4922, areaId = 4922 WHERE id IN (
    62904
);

-- Invalid creature entries
DELETE FROM creature WHERE id IN (
    58701, 59304, 59316, 59375, 60908, 65379, 72676, 72973
);
