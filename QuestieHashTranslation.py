import re

class HashTranslation():
    def __init__(self, quests, file="sqlua/addendum.lua", file2="sqlua/QuestieHashes.csv"):
        content = ""
        with open(file, "r") as infile:
            content = infile.read()
        questieLevLookup = re.search("QuestieLevLookup = \{\\n(.*?)\\n}", content, re.DOTALL)
        questNames = re.findall("\\n \[\"(.*?)\"]=\{\\n(.*?) },", questieLevLookup.group(0), re.DOTALL)
        self.questsByName = {} # [name] = [(Objectives, RequiredRaces, questieHash), ...]
        for name, objectivesString in questNames:
            self.questsByName[name] = re.findall("  \[\"(.*?)\"]=\{(.*?),(.*?)},\\n", objectivesString, re.DOTALL)
        self.questsByHash = {} # [questieHash] = (name, Objectives, RequiredRaces)
        for name in self.questsByName:
            for quest in self.questsByName[name]:
                self.questsByHash[int(quest[2])] = (name, quest[0], int(quest[1]))
        content = ""
        with open(file2, "r") as infile:
            content = infile.read()
        hashes = re.findall("(.*?),(.*?),(.*?)\\n", content, re.DOTALL)
        self.newHashes = {}
        for x in hashes[1:]:
            self.newHashes[int(x[1])] = int(x[0])
        self.alternateNewHashes = {}
        for x in hashes[1:]:
            self.alternateNewHashes[int(x[2])] = int(x[0])
        self.hashToId = {}
        for name in self.questsByName:
            for quest in self.questsByName[name]:
                questieHash = int(quest[2])
                if questieHash in self.newHashes:
                    self.hashToId[questieHash] = [self.newHashes[questieHash]]
                elif questieHash in self.alternateNewHashes:
                    self.hashToId[questieHash] = [self.alternateNewHashes[questieHash]]
                else:
                    self.hashToId[questieHash] = quests.allQuests(Title = self.escapeName(name))
                    if len(self.hashToId[questieHash]) == 0: # this captures 5 quests whose title includes quotes
                        self.hashToId[questieHash] = quests.allQuests(Title = name)
                    if len(self.hashToId[questieHash]) == 0 and " (Elite)" in name: # yes, I'm really doing this for one quest
                        self.hashToId[questieHash] = quests.allQuests(Title = name[0:-8])
                    if len(self.hashToId[questieHash]) == 0: # this too
                        self.hashToId[questieHash] = quests.allQuests(Title = name.replace("'", "\\'"))
        self.objectiveFix = {}
        for questieHash in self.hashToId:
            if len(self.hashToId[questieHash]) > 1:
                possibleIds = []
                for quest in self.hashToId[questieHash]:
                    possibleIds.append(quest)
                for quest in self.hashToId[questieHash]:
                    if hasattr(quest, "Objectives") and (self.questsByHash[questieHash][1] != quest.Objectives):
                        possibleIds.remove(quest)
                if len(possibleIds) == 1:
                    self.objectiveFix[questieHash] = possibleIds[0]
                elif len(possibleIds) > len(self.hashToId[questieHash]):
                    self.hashToId[questieHash] = possibleIds
        for questieHash in self.objectiveFix:
            self.hashToId[questieHash] = [self.objectiveFix[questieHash]]
        nameDone = []
        self.addendum = []
        self.debug = []
        self.debug2 = []
        for questieHash in self.hashToId:
            if len(self.hashToId[questieHash]) > 1:
                name = self.questsByHash[questieHash][0]
                if name in nameDone:
                    continue
                objectives = self.questsByHash[questieHash][1]
                requiredRaces = self.questsByHash[questieHash][2]
                allEqual = True
                hashes = []
                qIds = []
                for x in self.hashToId[questieHash]:
                    qIds.append(x)
                for quest in self.questsByName[name]:
                    self.debug2.append((int(quest[2]), self.hashToId[int(quest[2])]))
                    if len(self.hashToId[int(quest[2])]) == 1 and self.hashToId[int(quest[2])][0] in qIds:
                        if questieHash not in self.debug:
                            self.debug.append(questieHash)
                        qIds.remove(self.hashToId[int(quest[2])][0])
                    else:
                        hashes.append(int(quest[2]))
                        if quest[0] != objectives or int(quest[1]) != requiredRaces:
                            allEqual = False
                if (allEqual) and (len(hashes) == len(self.hashToId[questieHash])):
                    for i in range(0, len(hashes)):
                        self.addendum.append((hashes[i], qIds[i]))
                nameDone.append(name)
        # check for unknown quests.
        self.noQuestId = []
        for questieHash in self.hashToId:
            if len(self.hashToId[questieHash]) == 0:
                self.noQuestId.append(questieHash)
        # check for non-unique hash-to-ID matching
        self.moreThanOneQuestId = []
        for questieHash in self.hashToId:
            if len(self.hashToId[questieHash]) > 1:
                self.moreThanOneQuestId.append(questieHash)

    def printTranslation(self, file="sqlua/translateHashToId.lua"):
        with open(file, "w") as outfile:
            outfile.write("QuestieHashToId = {\n")
            for questieHash in sorted(self.hashToId):
                if len(self.hashToId[questieHash]) == 1:
                    outfile.write(" ["+str(questieHash)+"] = "+str(self.hashToId[questieHash][0])+",\n")
                else:
                    outfile.write(" ["+str(questieHash)+"] = 0, --FIXME: "+str(self.hashToId[questieHash])+",\n")
            outfile.write("}\n")
    def escapeName(self, string):
        name = string.replace('"', '\\"')
        name2 = name.replace("'", "\\'")
        return name2
