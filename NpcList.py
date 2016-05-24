from sqlua.Npc import *

class NpcList():
	"""Holds a list of Npc() objects. Requires a pymysql cursor to cmangos classicdb."""
	def __init__(self, cursor):
		self.nList = []
		tables = self.__getNpcTables(cursor)
		print("Adding Npcs...")
		count = len(tables[0])
		for npc in tables[0]:
			self.addNpc(npc, tables[1:])
			if ((count % 200) == 0):
				print(str(count)+"...", end="")
			count -= 1
		print("\nDone.")

	def addNpc(self, npc, tables):
		self.nList.append(Npc(npc, tables))

	def findNpc(self, **kwargs):
		return next(self.__iterNpc(**kwargs))

	def allNpcs(self, **kwargs):
		return list(self.__iterNpc(**kwargs))

	def allNpcsWith(self, *args):
		return list(self.__iterNpcWith(*args))

	def __iterNpcWith(self, *args):
		return (npc for npc in self.nList if hasattr(npc, *args))

	def __iterNpc(self, **kwargs):
		return (npc for npc in self.nList if npc.match(**kwargs))

	def __getNpcTables(self, cursor):
		print("Selecting NPC related MySQL tables...")
		cursor.execute("SELECT entry, name, minlevel, maxlevel, minlevelhealth, maxlevelhealth, rank FROM creature_template")
		npc_tpl = []
		for a in cursor.fetchall():
			npc_tpl.append(a)
		cursor.execute("SELECT id, map, position_x, position_y, guid FROM creature")
		npc = []
		for a in cursor.fetchall():
			npc.append(a)
		cursor.execute("SELECT * FROM creature_questrelation")
		npc_start = []
		for a in cursor.fetchall():
			npc_start.append(a)
		cursor.execute("SELECT * FROM creature_involvedrelation")
		npc_end = []
		for a in cursor.fetchall():
			npc_end.append(a)
		cursor.execute("SELECT point, id, position_x, position_y FROM creature_movement")
		npc_mov = []
		for a in cursor.fetchall():
			npc_mov.append(a)
		cursor.execute("SELECT point, entry, position_x, position_y FROM creature_movement_template")
		npc_mov_tpl = []
		for a in cursor.fetchall():
			npc_mov_tpl.append(a)
		print("Done.")

		return [npc_tpl, npc, npc_start, npc_end, npc_mov, npc_mov_tpl]
