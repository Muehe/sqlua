from sqlua.QuestList import *
from sqlua.NpcList import *
import pymysql
dbc = pymysql.connect('localhost', 'mangos', 'mangos', 'mangos') # host, user, pw, db name
cursor = dbc.cursor()

def doQuests(cursor):
	quests = QuestList(cursor)
	npcs = NpcList(cursor)
	print("Printing quest file...")
	quests.printShaguQuestFile(npcs)
	print("Done.")
	return quests, npcs
