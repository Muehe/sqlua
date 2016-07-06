# sqlua
Unpacks data from a cmangos DB for addon developers. In Alpha.

# Requirements
 1. A cmangos DB or one with the same field names.
  * Optionally a version of GMDB.
 2. Python3 (2 should be fine, but not tested).
 3. pymysql. Under linux you can :
  * ```sudo apt-get install pip3```
  * ```sudo pip3 install PyMySQL```

# Usage

There might be a smarter way here, but this works for me (Windows):
  1. Place the sqlua folder in the python directory.
  2. Configure your mysql data in the main.py file.
  3. Start IDLE interpreter.
  4. Use ```exec(open("sqlua/main.py").read())```

Now you are ready to use the functions and classes. E.g. use:

 * ```q = QuestList(cursor)``` to generate a list holding all quests in the DB.
 * ```q = QuestList(cursor, "deDE")``` to generate a list using german locale tables.
 * ```vars(q.allQuests(Title = "The Defias Brotherhood"))``` to see the properties of all quests with this name.
 * ```defiasChain = q.allQuests(Title = "The Defias Brotherhood")``` to get a list of Quest() objects with this name.
 * ```q.printQuestFile("sqlua/spawnDB.lua")``` to generate a DB file.
