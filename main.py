from db.QuestList import QuestList
from db.cata.CataItemList import CataItemList
from db.cata.CataNpcList import CataNpcList
from db.cata.CataObjList import CataObjList
from db.cata.CataQuestList import CataQuestList
from db.NpcList import *
from db.ObjList import *
from db.ItemList import *
from preExtract.CoordPreExtract import printCoordFiles

import sys
import pymysql
import config

import time

version = config.version
db_flavor = config.db_flavor
debug = config.debug

if version not in ['classic', 'tbc', 'wotlk', 'cata']:
    print(f'Unknown version {version}')
    sys.exit(1)


def getClassInstances(recache=False):
    """Get new instances of the list classes"""
    print("Reading data from {0} database...".format(db_flavor))
    if version == 'cata':
        quests = CataQuestList(version)
        quests.run(cursor, dictCursor, db_flavor, recache)
        npcs = CataNpcList(version, debug)
        npcs.run(cursor, dictCursor, db_flavor, recache)
        obj = CataObjList(version)
        obj.run(cursor, db_flavor, recache=recache)
        items = CataItemList(version)
        items.run(dictCursor, recache=recache)
    else:
        quests = QuestList(version)
        quests.run(cursor, dictCursor, db_flavor, recache)
        npcs = NpcList(version, debug)
        npcs.run(cursor, dictCursor, db_flavor, recache)
        obj = ObjList(version)
        obj.run(cursor, db_flavor, recache=recache)
        items = ItemList(version)
        items.run(dictCursor, recache=recache)
    return quests, npcs, obj, items

def recache():
    _, _, _, _ = getClassInstances(True)

def main(recache):
    """Extracts and prints quest related data"""
    # TODO: Add args to extract and print only specific files
    quests, npcs, objects, items = getClassInstances(recache)
    print("Printing files...")
    quests.printQuestFile(f'output/{version}/{version}QuestDB.lua')
    npcs.printNpcFile(f'output/{version}/{version}NpcDB.lua')
    objects.printObjFile(f'output/{version}/{version}ObjectDB.lua')
    items.writeFile(f'output/{version}/{version}ItemDB.lua')
    print("Done.")
    return 0

def getCursors(v):
    connection = pymysql.connect(
        host=config.dbInfo['host'],
        user=config.dbInfo['user'],
        password=config.dbInfo['password'],
        database=config.dbInfo[v],
        port=config.dbInfo["port"],
        charset='utf8'
    )
    c = connection.cursor()
    dc = connection.cursor(pymysql.cursors.DictCursor)

    return c, dc

def preExtract(v):
    c, dc = getCursors(v)
    printCoordFiles(c, v)

# DB connection needs to be set up first and globally, but after CLI 
# arguments are checked, in case the argument differs from the config
# file, so the main function being run is delayed by use of this variable
runMain = False

reCache = False

if __name__ == "__main__":
    """Executes only if run as a script"""
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '-r':
                reCache = True
            elif arg in ['classic', 'tbc', 'wotlk', 'cata']:
                version = arg
            elif arg in ['mangos', 'trinity']:
                db_flavor = arg
            else:
                print(f'Unknown argument "{arg}"')
    print(f'Using version {version}')
    runMain = True

cursor, dictCursor = getCursors(version)

if runMain:
    start_time = time.time()
    main(reCache)
    print("--- %s seconds ---" % (time.time() - start_time))
else:
    print(f'Using version {version}')
