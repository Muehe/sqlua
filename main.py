from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from ItemList import *
from Items import *
from preExtract.CoordPreExtract import printCoordFiles

import pymysql
import config

# Set up MySQL connection
connection = pymysql.connect(config.host, config.user, config.password, config.database, charset='utf8')
cursor = connection.cursor()
dictCursor = connection.cursor(pymysql.cursors.DictCursor)

# Create new List classes
def getClassInstances():
    """Get new instances of the list classes"""
    quests = QuestList(cursor, dictCursor)
    npcs = NpcList(cursor, dictCursor)
    obj = ObjList(cursor, dictCursor)
    items = [] # will be changed to: ItemList(dictCursor)
    return quests, npcs, obj, items

def questiePrint():
    """Partial extraction and print for QuestieClassic branch (no items)"""
    print("Printing quest file...")
    quests = QuestList(cursor, dictCursor)
    quests.printQuestFile("questDB.lua")
    print("Done printing quests.")
    print("Printing NPC file...")
    npcs = NpcList(cursor, dictCursor)
    npcs.printNpcFile("spawnDB.lua")
    print("Done printing NPCs.")
    print("Printing object file...")
    obj = ObjList(cursor, dictCursor)
    obj.printObjFile("objectDB.lua")
    print("Done printing objects.")

def main():
    """Extracts and prints quest related data"""
    quests, npcs, objects, items = getClassInstances()
    print("Printing quest file...")
    quests.printQuestFile()
    print("Done.")
    print("Printing NPC file...")
    npcs.printNpcFile()
    print("Done.")
    print("Printing object file...")
    objects.printObjFile()
    print("Done.")
    items = doItems(cursor)
    return "Extract successful!"

if __name__ == "__main__":
    # execute only if run as a script
    main()