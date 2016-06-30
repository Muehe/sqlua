from sqlua.Obj import *

class ObjList():
	"""Holds a list of Obj() objects. Requires a pymysql cursor to cmangos classicdb."""
	def __init__(self, cursor):
		self.objectList = {}
		tables = self.__getObjTables(cursor)
		print("Adding Objs...")
		count = len(tables[0])
		for obj in tables[0]:
			self.addObj(obj, tables[1:])
			if ((count % 200) == 0):
				print(str(count)+"...", end="")
			count -= 1
		print("\nDone.")

	def addObj(self, obj, tables):
		newObj = Obj(obj, tables)
		self.objectList[newObj.id] = newObj

	def findObj(self, **kwargs):
		return next(self.__iterObj(**kwargs))

	def allObjs(self, **kwargs):
		return list(self.__iterObj(**kwargs))

	def allObjsWith(self, *args):
		return list(self.__iterObjWith(*args))

	def __iterObjWith(self, *args):
		return (self.objectList[obj] for obj in self.objectList if hasattr(self.objectList[obj], *args))

	def __iterObj(self, **kwargs):
		return (self.objectList[obj] for obj in self.objectList if self.objectList[obj].match(**kwargs))

	def __getObjTables(self, cursor):
		print("Selecting object related MySQL tables...")
		cursor.execute("SELECT entry, name, type, faction, data1 FROM gameobject_template")
		obj_tpl = []
		for a in cursor.fetchall():
			obj_tpl.append(a)
		cursor.execute("SELECT id, map, position_x, position_y, guid FROM gameobject")
		obj = []
		for a in cursor.fetchall():
			obj.append(a)
		cursor.execute("SELECT * FROM gameobject_questrelation")
		obj_start = []
		for a in cursor.fetchall():
			obj_start.append(a)
		cursor.execute("SELECT * FROM gameobject_involvedrelation")
		obj_end = []
		for a in cursor.fetchall():
			obj_end.append(a)
		print("Done.")

		return [obj_tpl, obj, obj_start, obj_end]

	def printObjFile(self, file="sqlua/objData.lua"):
		outfile = open(file, "w")
		outfile.write("objData = {\n")
		for objId in sorted(self.objectList):
			obj = self.objectList[objId]
			if (not hasattr(obj, "spawns")) or (obj.type not in [2, 3, 5, 8, 10]):
				continue
			zoneId = 0
			lenSpawns = 0
			outfile.write("["+str(obj.id)+"] = {'"+obj.name+"',")
			if hasattr(obj, "start"):
				outfile.write("{")
				for quest in obj.start:
					outfile.write(str(quest)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if hasattr(obj, "end"):
				outfile.write("{")
				for quest in obj.end:
					outfile.write(str(quest)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if hasattr(obj, "spawns"):
				outfile.write("{")
				for zone in obj.spawns.cByZone:
					if not zone in validZoneList:
						if zoneId == 0:
							zoneId = zone
						outfile.write("["+str(zone)+"]={{-1, -1}},")
						continue
					if len(obj.spawns.cByZone[zone]) > lenSpawns:
						lenSpawns = len(obj.spawns.cByZone[zone])
						zoneId = zone
					outfile.write("["+str(zone)+"]={")
					for coords in obj.spawns.cByZone[zone]:
						outfile.write("{"+str(coords[0])+","+str(coords[1])+"},")
					outfile.write("},")
				outfile.write("},")
			else:
				outfile.write("nil,")
			outfile.write(str(zoneId)+",")
			outfile.write("},\n")
		outfile.write("}\n")
