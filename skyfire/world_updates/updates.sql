# quest 25136 has a NextQuestId which is not in the database
UPDATE quest_template SET NextQuestId = 25127 WHERE Id = 25136;

# There are gameobjects that have item=1, but mincountOrRef is set to a negative itemId. We set item to the absolute value of mincountOrRef
UPDATE gameobject_loot_template SET item = ABS(mincountOrRef) WHERE item = 1 AND mincountOrRef < 0;

# quest 31694 has some debug text in the objectives text and details which we remove
UPDATE quest_template SET Objectives = '', Details = '' WHERE Id = 31694;
