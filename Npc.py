from sqlua.CoordList import *
import re

def getCreatureZones(file="sqlua/creatureZones.txt"):
	infile = open(file, "r")
	content = infile.read()
	infile.close()
	zoneList = re.findall("(\d+),(\d+)", content)
	zoneDict = {}
	for pair in zoneList:
		zoneDict[int(pair[1])] = int(pair[0])
	return zoneDict

zones = getCreatureZones()

class Npc():
	spawnErrors = [] # Holds IDs of NPCs without spawns
	waypointErrors = []
	def __init__(self, npc, tables):
		self.id = npc[0]
		self.name = self.escapeName(npc[1])
		self.minlevel = npc[2]
		self.maxlevel = npc[3]
		self.minlevelhealth = npc[4]
		self.maxlevelhealth = npc[5]
		self.rank = npc[6]
		spawns = []
		waypoints = []
		for spawn in tables[0]:
			if (spawn[0] == self.id):
				if spawn[4] in zones:
					spawns.append((spawn[1], spawn[2], spawn[3], zones[spawn[4]]))
				else:
					spawns.append((spawn[1], spawn[2], spawn[3]))
				for waypoint in tables[3]:
					if (waypoint[1] == spawn[4]):
						waypoints.append((spawn[1], waypoint[2], waypoint[3]))
		wpError = False
		for waypoint in tables[4]:
			if (waypoint[1] == self.id):
				if (spawns == []):
					if (not wpError):
						wpError = True
				else:
					waypoints.append((spawns[0][0], waypoint[2], waypoint[3]))
		if (spawns == []):
			Npc.spawnErrors.append(self.id)
		else:
			self.spawns = CoordList(spawns)
		if (waypoints != []):
			self.waypoints = CoordList(waypoints)
		if(wpError):
			Npc.waypointErrors.append(self.id)

	def __repr__(self):
		return str(self.id)

	def escapeName(self, string):
		name = string.replace('"', '\\"')
		name2 = name.replace("'", "\\'")
		return name2

	def match(self, **kwargs):
		for (key, val) in kwargs.items():
			if not (hasattr(self, key)):
				return False
		return all(getattr(self,key) == val for (key, val) in kwargs.items())
