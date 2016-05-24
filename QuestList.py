from sqlua.Quest import *

class QuestList():
	"""Holds a list of Quest() objects. Requires a pymysql cursor to cmangos classicdb."""
	def __init__(self, cursor):
		self.qList = []
		tables = self.__getQuestTables(cursor)
		print("Adding Quests...")
		count = len(tables[0])
		for quest in tables[0]:
			self.__addQuest(quest, tables[1:])
			if ((count % 200) == 0):
				print(str(count)+"...", end="")
			count -= 1
		print("\nDone.")

	def unpackBitMask(self, bitMask):
		bits = []
		numBits=1
		while(pow(2, numBits) < bitMask):
			numBits += 1
		for x in range(-numBits, 1):
			potency = 1 << -x #pow(2, -x)
			if (bitMask >= potency):
				bitMask = bitMask - potency
				#s = "Flag on bit " + str(-x) + " is set (value " + str(potency) +")"
				#print (s)
				bits.insert(0, -x)
		return bits

	"""only used by constructor"""
	def __addQuest(self, quest, tables):
		self.qList.append(Quest(quest, tables))

	"""find one quest by keyword = value, ..."""
	def findQuest(self, **kwargs):
		return next(self.__iterQuest(**kwargs))

	"""find all quests by keyword = value, ..."""
	def allQuests(self, **kwargs):
		return list(self.__iterQuest(**kwargs))

	"""find all quests by keyword, ..."""
	def allQuestsWith(self, *args):
		return list(self.__iterQuestWith(*args))

	def __iterQuestWith(self, *args):
		return (quest for quest in self.qList if hasattr(quest, *args))

	def __iterQuest(self, **kwargs):
		return (quest for quest in self.qList if quest.match(**kwargs))

	"""only used by constructor"""
	def __getQuestTables(self, cursor):
		print("Selecting quest related MySQL tables...")
		# SrcItemId needed to check for spell_script_target (type and targetEntry) via item_template.spellId
		cursor.execute("SELECT entry, MinLevel, QuestLevel, Type, RequiredClasses, RequiredRaces, RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue, RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue, QuestFlags, PrevQuestId, NextQuestId, NextQuestInChain, ExclusiveGroup, Title, Objectives, ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqSourceId1, ReqSourceId2, ReqSourceId3, ReqSourceId4, ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4, ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4, PointMapId, PointX, PointY, StartScript, CompleteScript, SrcItemId, ZoneOrSort, Method, ObjectiveText1, ObjectiveText2, ObjectiveText3, ObjectiveText4 FROM quest_template")
		quest_template = []
		for a in cursor.fetchall():
			quest_template.append(a)
		cursor.execute("SELECT id, quest FROM creature_involvedrelation")
		creature_involvedrelation = []
		for a in cursor.fetchall():
			creature_involvedrelation.append(a)
		cursor.execute("SELECT id, quest FROM gameobject_involvedrelation")
		gameobject_involvedrelation = []
		for a in cursor.fetchall():
			gameobject_involvedrelation.append(a)
		cursor.execute("SELECT id, quest FROM creature_questrelation")
		creature_questrelation = []
		for a in cursor.fetchall():
			creature_questrelation.append(a)
		cursor.execute("SELECT id, quest FROM gameobject_questrelation")
		gameobject_questrelation = []
		for a in cursor.fetchall():
			gameobject_questrelation.append(a)
		cursor.execute("SELECT entry, startquest FROM item_template")
		item_questrelation = []
		for a in cursor.fetchall():
			item_questrelation.append(a)
		cursor.execute("SELECT id, quest FROM areatrigger_involvedrelation")
		areatrigger_involvedrelation = []
		for a in cursor.fetchall():
			areatrigger_involvedrelation.append(a)
		cursor.execute("SELECT entry, Title_loc3, Objectives_loc3, ObjectiveText1_loc3, ObjectiveText2_loc3, ObjectiveText3_loc3, ObjectiveText4_loc3 FROM locales_quest")
		loc_quest = []
		for a in cursor.fetchall():
			loc_quest.append(a)
		print("Done.")
		return (quest_template, creature_involvedrelation, gameobject_involvedrelation, creature_questrelation, gameobject_questrelation, item_questrelation, areatrigger_involvedrelation, loc_quest)

	def checkStartEnd(self):
		"""Find quests with missing start or end points.
		Returns a list of all objects in qList missing either.
		"""
		cs = self.allQuestsWith('creatureStart')
		gs = self.allQuestsWith('goStart')
		its = self.allQuestsWith('itemStart')
		xs = []
		for q in self.qList:
			if (q not in cs) and (q not in gs) and (q not in its):
				xs.append(q)
		ge = self.allQuestsWith('goEnd')
		ce = self.allQuestsWith('creatureEnd')
		xe = []
		for q in self.qList:
			if (q not in ce) and (q not in ge):
				xe.append(q)
		xx = []
		for q in xs:
			if (q in xe):
				xx.append(q)
		noS = []
		for q in xs:
			if (q not in xe):
				noS.append(q)
		noE = []
		for q in xe:
			if (q not in xs):
				noE.append(q)
		for q in noE:
			xx.append(q)
		for q in noS:
			xx.append(q)
		return xx

	def printQuestFile(self, file="sqlua/qData.lua"):
		outfile = open(file, "w")
		functionString = """DB_NAME, DB_NPC = 1, 1;
DB_STARTS, DB_OBJ = 2, 2;
DB_ENDS, DB_ITM = 3, 3;
DB_MINLEVEL, DB_ZONES = 4, 4;
DB_LEVEL = 5;
DB_REQRACE = 6;
DB_REQCLASS = 7;
DB_OBJECTIVES = 8;
DB_TRIGGER = 9;
function deleteFaction(str)
	local before = WHDB_GetTableLength(qData);
	for key, data in pairs(qData) do
		if (data[DB_REQRACE] == "AH") or (data[DB_REQRACE] ~= str) then
			data[DB_REQRACE] = nil;
		else
			qData[key] = nil;
		end
	end
	local after = WHDB_GetTableLength(qData);
	WHDB_Debug_Print(2, before-after.." opposite faction quests deleted");
end
function deleteClasses()
	if not WHDB_Settings.class then
		return;
	end
	local before = WHDB_GetTableLength(qData);
	local classes = {"Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Death Knight", "Shaman", "Mage", "Warlock", "Druid"};
	local playerClass = false;
	for key, name in pairs(classes) do
		if name == WHDB_Settings.class then
			playerClass = key - 1;
		end
	end
	if playerClass then
		for key, data in pairs(qData) do
			if data[DB_REQCLASS] then
				local found = false;
				for k, class in pairs(data[DB_REQCLASS]) do
					if class == playerClass then
						found = true;
					end
				end
				if not found then
					qData[key] = nil;
				end
			end
		end
	end
	local after = WHDB_GetTableLength(qData);
	WHDB_Debug_Print(2, before-after.." other class quests deleted");
end
qLookup = {};
function fillQuestLookup()
	local checkedNames = {};
	for key, data in pairs(qData) do
		local name = data[DB_NAME];
		local checked = checkedNames[name];
		if not checked then
			checkedNames[name] = true;
			qLookup[name] = {};
			for k, d in pairs(qData) do
				if (d[DB_NAME] == name) then
					if d[DB_OBJECTIVES] then
						qLookup[name][k] = d[DB_OBJECTIVES];
					else
						qLookup[name][k] = '';
					end
				end
			end
		end
	end
end
"""
		outfile.write(functionString)
		outfile.write("qData = {\n")
		excluded = self.checkStartEnd()
		for quest in self.qList:
			if quest in excluded:
				continue
			outfile.write("\t["+str(quest.id)+"] = {") #key
			outfile.write("\""+quest.Title+"\",") #name = 1
			outfile.write("{") #starts = 2
			if (hasattr(quest, "creatureStart")):
				outfile.write("{") #npc = starts1
				for npc in quest.creatureStart:
					outfile.write(str(npc)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if (hasattr(quest, "goStart")):
				outfile.write("{") #obj = starts2
				for obj in quest.goStart:
					outfile.write(str(obj)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if (hasattr(quest, "itemStart")):
				outfile.write("{") #itm = starts3
				for itm in quest.itemStart:
					outfile.write(str(itm)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			outfile.write("},")
			outfile.write("{") #ends = 3
			if (hasattr(quest, "creatureEnd")):
				outfile.write("{") #npc = ends1
				for npc in quest.creatureEnd:
					outfile.write(str(npc)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if (hasattr(quest, "goEnd")):
				outfile.write("{") #obj = ends2
				for obj in quest.goEnd:
					outfile.write(str(obj)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			outfile.write("},")
			outfile.write(str(quest.MinLevel)+",") #minLevel = 4
			outfile.write(str(quest.QuestLevel)+",") #level = 5
			outfile.write("\""+self.getFactionString(quest.RequiredRaces)+"\",") #RequiredRaces = 6
			if (hasattr(quest, "RequiredClasses")):
				outfile.write("{") #RequiredClasses = 7
				for n in self.unpackBitMask(quest.RequiredClasses):
					outfile.write(str(n)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			if (hasattr(quest, "Objectives")) and (len(self.allQuests(Title = quest.Title)) > 1):
				if quest.id == 4641:
					quest.Objectives = quest.Objectives[0:-5]
				outfile.write("\""+quest.Objectives+"\",") #objectives = 8
			else:
				outfile.write("nil,")
			if (hasattr(quest, "triggerEnd")):
				outfile.write("{") #trigger = 9
				for tri in quest.triggerEnd:
					outfile.write(str(tri)+",")
				outfile.write("},")
			else:
				outfile.write("nil,")
			outfile.write("},\n")
		outfile.write("};\n")
		outfile.close();

	def printShaguQuestFile(self, npcs, file="sqlua/questDB.lua"):
		outfile = open(file, "w")
		outfile.write("questDB = {\n")
		excluded = self.checkStartEnd()
		checked = []
		for quest in self.qList:
			if quest in excluded:
				continue
			if quest.Title not in checked:
				checked.append(quest.Title)
			else:
				continue
			start = []
			end = []
			for q in self.allQuests(Title = quest.Title):
				if not (q in excluded):
					if hasattr(q, "creatureStart"):
						for id in q.creatureStart:
							if not id in start:
								start.append(id)
					if hasattr(q, "creatureEnd"):
						for id in q.creatureEnd:
							if not id in end:
								end.append(id)
			outfile.write("\t[\""+quest.Title+"\"] = {\n")
			for q in end:
				if not q in start:
					start.append(q)
			for npc in start:
				found = npcs.findNpc(id = npc)
				outfile.write("\t\t[\""+found.name+"\"] = 'NPC',\n")
			outfile.write("\t},\n")
		outfile.write("};")
		outfile.close()

	def getFactionString(self, requiredRaces):
		if requiredRaces == 0:
			return "AH"
		faction = ""
		if requiredRaces & 77:
			faction += "A"
		if requiredRaces & 178:
			faction += "H"
		return faction
