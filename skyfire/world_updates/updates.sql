# These updates are required after installing the database:

# quest 25136 has a NextQuestId which is not in the database
UPDATE quest_template SET NextQuestId = 25127 WHERE Id = 25136;

# There are gameobjects that have item=1, but mincountOrRef is set to a negative itemId. We set item to the absolute value of mincountOrRef
UPDATE gameobject_loot_template SET item = ABS(mincountOrRef) WHERE item = 1 AND mincountOrRef < 0;

# quest 31694 has some debug text in the objectives text and details which we remove
UPDATE quest_template SET Objectives = '', Details = '' WHERE Id = 31694;

# NPC 62943 has npcflag of -2147483648, which we don't care about
UPDATE creature_template SET npcflag = 0 WHERE entry = 62943;

# some quests have questflags set to 16777216 - we override them with the Cata value 128
UPDATE quest_template SET Flags = 128 WHERE Flags = 16777216;

# some quests have questflags set to a really high value
# for odd numbers we set them to 1 to keep the repeatable flag
# for even numbers we set them to 0
UPDATE quest_template SET Flags = 1 WHERE Flags > 524296 AND MOD(Flags, 2) = 1; # odd
UPDATE quest_template SET Flags = 0 WHERE Flags > 524296 AND MOD(Flags, 2) = 0; # even

# the requiredRaces field is mixed in pre-cata values and cata values, we streamline them to the cata values
UPDATE quest_template SET RequiredRaces = 2098253 WHERE RequiredRaces = 77; # All Alliance Classic -> Cata
UPDATE quest_template SET RequiredRaces = 946 WHERE RequiredRaces = 178; # All Horde Classic -> Cata
UPDATE quest_template SET RequiredRaces = 2098253 WHERE RequiredRaces = 1101; # All Alliance TBC -> Cata
UPDATE quest_template SET RequiredRaces = 946 WHERE RequiredRaces = 690; # All Horde TBC -> Cata

ALTER TABLE quest_template MODIFY COLUMN RequiredRaces INT UNSIGNED;
UPDATE quest_template SET RequiredRaces = 18875469 WHERE RequiredRaces = 2098253; # All Alliance Cata -> MoP
UPDATE quest_template SET RequiredRaces = 33555378 WHERE RequiredRaces = 946; # All Horde Cata -> MoP

# some quests have a MinLevel of -1, which does not make sense, we set them to 0
UPDATE quest_template SET MinLevel = 0 WHERE MinLevel = -1;

# Remove NPC 69533 as quest starter for now, as it is missing in the database
# This NPC is correct though and should be added to the database at some point
DELETE FROM creature_queststarter WHERE id = 69533;
