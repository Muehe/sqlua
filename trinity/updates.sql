# According to the SkyFire DB the highest NPC ID is 80674 so we remove everything above that
DELETE FROM `creature` WHERE `id` > 80674;
DELETE FROM `creature_template` WHERE `entry` > 80674;
DELETE FROM `creature_queststarter` WHERE `id` > 80674;
DELETE FROM `creature_questender` WHERE `id` > 80674;

# quest 31694 has some debug text in the objectives text and details which we remove
UPDATE quest_template SET LogDescription = '', QuestDescription = '' WHERE ID = 31694;

# some quests have questflags set to a really high value
# for odd numbers we set them to 1 to keep the repeatable flag
# for even numbers we set them to 0
UPDATE quest_template SET Flags = 1 WHERE Flags > 524296 AND MOD(Flags, 2) = 1; # odd
UPDATE quest_template SET Flags = 0 WHERE Flags > 524296 AND MOD(Flags, 2) = 0; # even
