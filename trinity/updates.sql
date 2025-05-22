# According to the SkyFire DB the highest NPC ID is 80674 so we remove everything above that
DELETE FROM `creature` WHERE `id` > 80674;
DELETE FROM `creature_template` WHERE `entry` > 80674;
DELETE FROM `creature_queststarter` WHERE `id` > 80674;
DELETE FROM `creature_questender` WHERE `id` > 80674;