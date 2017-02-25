# sqlua
Unpacks data from a cmangos DB for addon developers. In Alpha.

# Requirements
 1. A cmangos DB or one with the same field names.
  * Optionally a German localization.
 2. Python3.
 3. pymysql. Under linux you can :
    ```
    sudo apt-get install pip3
    sudo pip3 install PyMySQL
    ```

# Usage

  1. Configure your mysql data in the main.py file.
  2. Start the interpreter from the sqlua directory.
   * When starting idle3 from the start menu or a shortcut, you can use these commands to change your working directory:
     ```
     import os
     os.chdir('C:\\Path\\to\\sqlua\\')
     ```
  4. Use ```exec(open("main.py").read())``` to import all the definitions and set up a pymysql cursor to your database.

Now you are ready to use the functions and classes. Examples:

 * `q = QuestList(cur)` to generate a list holding all quests in the DB.
 * `q = QuestList(cur, "deDE")` to generate a list using german locale tables.
 * `vars(q.allQuests(Title = "The Defias Brotherhood"))` to see the properties of all quests with this name.
 * `defiasChain = q.allQuests(Title = "The Defias Brotherhood")` to get a list of Quest() objects with this name.
 * `q.printQuestFile("spawnDB.lua")` to generate a DB file.
