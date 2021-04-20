from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from ItemList import *
from preExtract.CoordPreExtract import printCoordFiles

import sys
import pymysql
import config

version = config.version
debug = config.debug

if version not in ['classic', 'tbc']:
    print(f'Unknown version {version}')
    sys.exit(1)


def getClassInstances(recache=False):
    """Get new instances of the list classes"""
    quests = QuestList(cursor, dictCursor, version, recache=recache)
    npcs = NpcList(cursor, dictCursor, version, recache=recache, debug=debug)
    obj = ObjList(cursor, dictCursor, version, recache=recache)
    items = ItemList(dictCursor, version, recache=recache)
    return quests, npcs, obj, items

def recache():
    _, _, _, _ = getClassInstances(True)

def main(recache):
    """Extracts and prints quest related data"""
    quests, npcs, objects, items = getClassInstances(recache)
    print("Printing files...")
    quests.printQuestFile(f'output/{version}/questDB.lua')
    npcs.printNpcFile(f'output/{version}/spawnDB.lua')
    objects.printObjFile(f'output/{version}/objectDB.lua')
    items.writeFile(f'output/{version}/itemDB.lua')
    print("Done.")
    return 0

# DB connection needs to be set up first and globally, but after CLI 
# arguments are checked, in case the argument differs from the config
# file, so the main function being run is delayed by use of this variable
runMain = False

if __name__ == "__main__":
    """Executes only if run as a script"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['classic', 'tbc']:
            version = sys.argv[1]
        else:
            print(f'Unknown version {sys.argv[1]}')
            sys.exit(1)
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
else:
    print(f'Using version {version}')
