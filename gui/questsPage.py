import flask
import hashlib

def questsPage(questID, dbs):
    data = {
        'id': questID,
        'quests': {},
        'fields': [
            "id",
            "Title",
            "Details",
            "Objectives",
            "MinLevel",
            "QuestLevel",
            "ZoneOrSort",
            "Type",
            "QuestFlags",
            "SpecialFlags",
            "Method",
            "RequiredRaces",
            "RequiredClasses",
            "RequiredSkill",
            "RequiredSkillValue",
            "RequiredMinRepFaction",
            "RequiredMinRepValue",
            "RepObjectiveFaction",
            "RepObjectiveValue",
            "PrevQuestId",
            "NextQuestId",
            "NextQuestInChain",
            "ExclusiveGroup",
            "ExclusiveTo",
            "InGroupWith",
            "PreQuestGroup",
            "PreQuestSingle",
            "ParentQuest",
            "ChildQuests",
            "ObjectiveList",
            "ReqItemId",
            "ReqSourceId",
            "ReqCreatureId",
            "ReqGOId",
            "ReqSpellCast",
            "SrcItemId",
            "creatureStart",
            "goStart",
            "itemStart",
            "creatureEnd",
            "goEnd",
            "triggerEnd",
            "BreadcrumbForQuestId",
            "Breadcrumbs",
            "RepReward",
        ],
    }

    hasData = {}
    for field in data['fields']:
        hasData[field] = False

    def getQuestText(quest):
        qData = {}
        for field in data['fields']:
            if hasattr(quest, field):
                f = getattr(quest, field)
                #if f == None: # TODO filter on quest constructor
                #    delattr(quest, field)
                #    continue
                hasData[field] = True
                h = 0
                if type(f) == str:
                    h = hashlib.sha512(f.encode()).hexdigest()[:8]
                elif field in ['ObjectiveList', 'RepReward']:
                    f = str(f)
                    h = hashlib.sha512(f.encode()).hexdigest()[:8]
                qData[field] = (f, h)
        return qData

    for flavor in dbs:
        for version in dbs[flavor]:
            if questID in dbs[flavor][version]['quests'].qList:
                data['quests'][flavor+" "+version] = getQuestText(dbs[flavor][version]['quests'].qList[questID])
            else:
                data['quests'][flavor+" "+version] = "Missing"

    for field in hasData:
        if not hasData[field]:
            data['fields'].remove(field)

    return flask.render_template('quests.html', data=data)
