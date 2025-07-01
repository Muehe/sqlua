from db.QuestList import QuestList
from db.NpcList import *
from db.ObjList import *
from db.ItemList import *
from preExtract.CoordPreExtract import printCoordFiles

import sys
import pymysql
import config

import time

version = config.version
versions = ['classic', 'tbc', 'wotlk', 'cata', 'mop']
if version not in versions:
    print(f'Unknown version {version}')
    sys.exit(1)

flavor = config.flavor
flavors = ['cmangos', 'mangos', 'trinity', 'skyfire']
if flavor not in flavors:
    print(f'Unknown flavor {flavor}')
    sys.exit(1)

debug = config.debug

def getClassInstances(recache=False):
    """Get new instances of the list classes"""
    print("Reading data from {0} database...".format(flavor))
    quests = QuestList(version, flavor, cursor, dictCursor, recache=recache)
    npcs = NpcList(version, flavor, cursor, dictCursor, recache=recache, extractSpawns=True, debug=debug)
    obj = ObjList(version, flavor, cursor, extractSpawns=True, recache=recache)
    items = ItemList(version, flavor, dictCursor, locale='enUS', recache=recache)
    return quests, npcs, obj, items

def recache():
    _, _, _, _ = getClassInstances(True)

def main(recache):
    """Extracts and prints quest related data"""
    if not individualUpdates:
        quests, npcs, objects, items = getClassInstances(recache)
        print("Printing files...")
        quests.printQuestFile(f'output/{version}/{flavor}/{version}QuestDB.lua')
        npcs.printNpcFile(f'output/{version}/{flavor}/{version}NpcDB.lua')
        objects.printObjFile(f'output/{version}/{flavor}/{version}ObjectDB.lua')
        items.writeFile(f'output/{version}/{flavor}/{version}ItemDB.lua')
        print("Done.")
        return 0
    else:
        if 'items' in sys.argv:
            items = ItemList(version, flavor, dictCursor, locale='enUS', recache=recache)
            items.writeFile(f'output/{version}/{flavor}/{version}ItemDB.lua')
        if 'npcs' in sys.argv:
            npcs = NpcList(version, flavor, cursor, dictCursor, recache=recache, extractSpawns=True, debug=debug)
            npcs.printNpcFile(f'output/{version}/{flavor}/{version}NpcDB.lua')
        if 'objects' in sys.argv:
            objects = ObjList(version, flavor, cursor, extractSpawns=True, recache=recache)
            objects.printObjFile(f'output/{version}/{flavor}/{version}ObjectDB.lua')
        if 'quests' in sys.argv:
            quests = QuestList(version, flavor, cursor, dictCursor, recache=recache)
            quests.printQuestFile(f'output/{version}/{flavor}/{version}QuestDB.lua')
        return 0

def getCursors(v=version, f=flavor):
    conversions = pymysql.converters.conversions
    conversions[pymysql.FIELD_TYPE.DECIMAL] = lambda x: float(x)
    conversions[pymysql.FIELD_TYPE.NEWDECIMAL] = lambda x: float(x)
    connection = pymysql.connect(
        host=config.dbInfo['host'],
        user=config.dbInfo['user'],
        password=config.dbInfo['password'],
        database=config.dbInfo[f][v],
        port=config.dbInfo["port"],
        charset='utf8',
        conv=conversions
    )
    c = connection.cursor()
    dc = connection.cursor(pymysql.cursors.DictCursor)

    return c, dc

def preExtract(v=version, f=flavor):
    c, dc = getCursors(v, f)
    printCoordFiles(c, v)

# DB connection needs to be set up first and globally, but after CLI 
# arguments are checked, in case the argument differs from the config
# file, so the main function being run is delayed by use of this variable
runMain = False
individualUpdates = False
reCache = False

if __name__ == "__main__":
    """Executes only if run as a script"""
    print(len(sys.argv))
    print(sys.argv)
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '-r':
                reCache = True
            elif arg in versions:
                version = arg
            elif arg in flavors:
                flavor = arg
            elif arg in ['items', 'npcs', 'objects', 'quests']:
                individualUpdates = True
            else:
                print(f'Unknown argument "{arg}"')
    print(f'Using version {version}')
    print(f'Using DB flavour {flavor}')
    runMain = True

cursor, dictCursor = getCursors(version, flavor)

if runMain:
    start_time = time.time()
    main(reCache)
    print("--- %s seconds ---" % (time.time() - start_time))
else:
    print(f'Using version {version}')
    print(f'Using DB flavour {flavor}')
