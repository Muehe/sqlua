from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from Items import *
import pymysql

"""
Usage:
* Install pymysql package for python.
* Apply your MySQL information to the line below.
* Start python from sqlua's root folder and use "exec(open("main.py").read())".
* Use "quests, npcs, obj, items = doExtract(cur)"
* Go make a coffee, do you laundry, save the world, etc.
"""
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
    items = doItems(cursor)
    return quests, npcs, obj, items
