from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from Items import *
from ItemList import *
from preExtract.CoordPreExtract import printCoordFiles
import pymysql

# MySQL information
host = 'localhost'
user = 'mangos'
password = 'mangos'
database = 'classicmangos'

# Set up MySQL connection
connection = pymysql.connect(host, user, password, database, charset='utf8')
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
