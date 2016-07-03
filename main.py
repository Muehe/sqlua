from sqlua.QuestList import *
from sqlua.NpcList import *
from sqlua.ObjList import *
from sqlua.CoordList import *
from sqlua.Items import *
import pymysql

dbc = pymysql.connect('localhost', 'mangos', 'mangos', 'mangos') # host, user, pw, db name
cur = dbc.cursor()

def doExtract(cursor=cur):
    quests = QuestList(cursor)
    npcs = NpcList(cursor)
    obj = ObjList(cursor)
    print("Printing quest file...")
    quests.printQuestFile()
    print("Done.")
    print("Printing NPC file...")
    npcs.printNpcFile()
    print("Done.")
    print("Printing object file...")
    obj.printObjFile()
    print("Done.")
    doItems(cursor)
    return quests, npcs, obj
