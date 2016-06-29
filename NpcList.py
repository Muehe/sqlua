from sqlua.Npc import *

class NpcList():
	"""Holds a list of Npc() objects. Requires a pymysql cursor to cmangos classicdb."""
	def __init__(self, cursor):
		self.nList = {}
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
		newNpc = Npc(npc, tables)
		self.nList[newNpc.id] = newNpc

	def findNpc(self, **kwargs):
		return next(self.__iterNpc(**kwargs))

	def allNpcs(self, **kwargs):
		return list(self.__iterNpc(**kwargs))

	def allNpcsWith(self, *args):
		return list(self.__iterNpcWith(*args))

	def __iterNpcWith(self, *args):
		return (self.nList[npc] for npc in self.nList if hasattr(self.nList[npc], *args))

	def __iterNpc(self, **kwargs):
		return (self.nList[npc] for npc in self.nList if self.nList[npc].match(**kwargs))

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

	def printNpcFile(self, file="sqlua/npcData.lua"):
		outfile = open(file, "w")
		outfile.write("npcData = {\n")
		for npcId in sorted(self.nList):
			npc = self.nList[npcId]
			if (not hasattr(npc, "spawns")) and (not hasattr(npc, "waypoints")):
				continue
			zoneId = 0
			lenSpawns = 0
			outfile.write("["+str(npc.id)+"] = {'"+npc.name+"',"+str(npc.minlevelhealth)+","+str(npc.maxlevelhealth)+","+str(npc.minlevel)+","+str(npc.maxlevel)+","+str(npc.rank)+",")
			if hasattr(npc, "spawns"):
				outfile.write("{")
				for zone in npc.spawns.cByZone:
					if not zone in validZoneList:
						if zoneId == 0:
							zoneId = zone
						outfile.write("["+str(zone)+"]={{-1, -1}},")
						continue
					if len(npc.spawns.cByZone[zone]) > lenSpawns:
						lenSpawns = len(npc.spawns.cByZone[zone])
						zoneId = zone
					outfile.write("["+str(zone)+"]={")
					for coords in npc.spawns.cByZone[zone]:
						outfile.write("{"+str(coords[0])+","+str(coords[1])+"},")
					outfile.write("},")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if hasattr(npc, "waypoints"):
				outfile.write("{")
				for zone in npc.waypoints.cByZone:
					if not zone in validZoneList:
						if zoneId == 0:
							zoneId = zone
						outfile.write("["+str(zone)+"]={{-1, -1}},")
						continue
					outfile.write("["+str(zone)+"]={")
					for coords in npc.waypoints.cByZone[zone]:
						outfile.write("{"+str(coords[0])+","+str(coords[1])+"},")
					outfile.write("},")
				outfile.write("},")
			else:
				outfile.write("nil,")
			outfile.write(str(zoneId)+",")
			if hasattr(npc, "start"):
				outfile.write("{")
				for quest in npc.start:
					outfile.write(str(quest)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if hasattr(npc, "end"):
				outfile.write("{")
				for quest in npc.end:
					outfile.write(str(quest)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			outfile.write("},\n")
		outfile.write("}\n")
