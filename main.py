from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from ItemList import *
from preExtract.CoordPreExtract import printCoordFiles

import pymysql
import config

# Set up MySQL connection
connection = pymysql.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.database,
    charset='utf8'
)
cursor = connection.cursor()
dictCursor = connection.cursor(pymysql.cursors.DictCursor)

def getClassInstances(recache=False):
    """Get new instances of the list classes"""
    quests = QuestList(cursor, dictCursor, recache=recache)
    npcs = NpcList(cursor, dictCursor, recache=recache)
    obj = ObjList(cursor, dictCursor, recache=recache)
    items = ItemList(dictCursor, recache=recache)
    return quests, npcs, obj, items

def recache():
    _, _, _, _ = getClassInstances(True)

def main(recache):
    """Extracts and prints quest related data"""
    quests, npcs, objects, items = getClassInstances(recache)
    print("Printing files...")
    quests.printQuestFile()
    npcs.printNpcFile()
    objects.printObjFile()
    items.writeFile()
    print("Done.")
    return 0

if __name__ == "__main__":
    # execute only if run as a script
    main(True)
