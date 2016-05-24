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
		self.spawns = []
		self.waypoints = []
		for spawn in tables[0]:
			if (spawn[0] == self.id):
				self.spawns.append((spawn[1], spawn[2], spawn[3]))
				for waypoint in tables[3]:
					if (waypoint[1] == spawn[4]):
						self.waypoints.append((spawn[1], waypoint[2], waypoint[3]))
		wpError = False
		for waypoint in tables[4]:
			if (waypoint[1] == self.id):
				if (len(self.spawns) != 1):
					if (not wpError):
						wpError = True
				else:
					self.waypoints.append((self.spawns[0][0], waypoint[2], waypoint[3]))
		if (self.spawns == []):
			del self.spawns
			Npc.spawnErrors.append(self.id)
		if (self.waypoints == []) or wpError:
			del self.waypoints
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
