from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from ItemList import *
from preExtract.CoordPreExtract import printCoordFiles

import sys
import pymysql
import config

def getClassInstances(recache=False):
    """Get new instances of the list classes"""
    quests = QuestList(cursor, dictCursor, version, recache=recache)
    npcs = NpcList(cursor, dictCursor, version, recache=recache)
    obj = ObjList(cursor, dictCursor, version, recache=recache)
    items = ItemList(dictCursor, version, recache=recache)
    return quests, npcs, obj, items

def recache():
    _, _, _, _ = getClassInstances(True)

def main(recache):
    """Extracts and prints quest related data"""
    quests, npcs, objects, items = getClassInstances(recache)
    print("Printing files...")
    quests.printQuestFile(f'output/{self.version}/questDB.lua')
    npcs.printNpcFile(f'output/{self.version}/spawnDB.lua')
    objects.printObjFile(f'output/{self.version}/objectDB.lua')
    items.writeFile(f'output/{self.version}/itemDB.lua')
    print("Done.")
    return 0

version = config.version # accepts 'classic' or 'tbc'
runMain = False

if __name__ == "__main__":
    """Executes only if run as a script"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['classic', 'tbc']:
            version = sys.argv[1]
    print(f'Using version {version}')
    runMain = True

# Set up MySQL connection
connection = pymysql.connect(
    host=config.dbInfo['host'],
    user=config.dbInfo['user'],
    password=config.dbInfo['password'],
    database=config.dbInfo[version],
    charset='utf8'
)
cursor = connection.cursor()
dictCursor = connection.cursor(pymysql.cursors.DictCursor)

if runMain:
    main(True)
