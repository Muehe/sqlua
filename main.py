from QuestList import *
from NpcList import *
from ObjList import *
from CoordList import *
from ItemList import *
import pymysql

"""
Usage:
* Install pymysql package for python.
* Apply your MySQL information to the line below.
* Start python from sqlua's root folder and use "exec(open("main.py").read())".
* Use "quests, npcs, obj, items = doExtract(cur)"
* Go make a coffee, do you laundry, save the world, etc.
"""

host = 'localhost'
user = 'mangos'
password = 'mangos'
database = 'mangos'

connection = pymysql.connect(host, user, password, database)
cur1 = connection.cursor()
cur2 = connection.cursor(pymysql.cursors.DictCursor)

def doExtract(cursor=cur1, dictCursor=cur2):
    quests = QuestList(cursor)
    npcs = NpcList(cursor)
    obj = ObjList(cursor)
    items = ItemList(dictCursor)
    print("Printing quest file...")
    quests.printQuestFile()
    print("Done.")
    print("Printing NPC file...")
    npcs.printNpcFile()
    print("Done.")
    print("Printing object file...")
    obj.printObjFile()
    print("Done.")
    # items = doItems(cursor)
    # return quests, npcs, obj, items
    return "Extract successful!"
