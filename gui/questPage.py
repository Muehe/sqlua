import flask

from db.CoordData import *
from gui.utility import *

def questPage(questID, quests, npcs, objects, items):
    if questID not in quests.qList:
        return 'Unknown quest'
    data = {}
    quest = quests.qList[questID]
    ""
    pinList = {}
    for objective in quest.ObjectiveList:
        if objective == False:
            continue
        if 'type' in objective and objective['type'] == 'areaTrigger':
            for zone, pin in coordsToPins(objective['coords'], 'Exploration: '+objective['text'], imgSrc='event', width=2):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
        if 'type' in objective and objective['type'] == 'monster':
            npc = npcs.nList[objective['id']]
            for zone, pin in coordsToPins(npc.spawns, 'Creature Objective: '+npc.name, imgSrc='slay', width=1.75):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
        if 'type' in objective and objective['type'] == 'object':
            obj = objects.objectList[objective['id']]
            for zone, pin in coordsToPins(obj.spawns, 'Object Objective: '+obj.name, imgSrc='object', width=1.75):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
        if 'type' in objective and objective['type'] == 'item':
            item = items.itemList[objective['id']]
            for npcId in item.npcs:
                npc = npcs.nList[npcId]
                for zone, pin in coordsToPins(npc.spawns, item.name+' dropped by: '+npc.name, imgSrc='loot', width=2):
                    if zone not in pinList:
                        pinList[zone] = []
                    pinList[zone].append(pin)
            for objId in item.objects:
                obj = objects.objectList[npcId]
                for zone, pin in coordsToPins(obj.spawns, item.name+' dropped by: '+obj.name, imgSrc='loot', width=2):
                    if zone not in pinList:
                        pinList[zone] = []
                    pinList[zone].append(pin)
    if hasattr(quest, 'creatureStart'):
        for npcId in quest.creatureStart:
            npc = npcs.nList[npcId]
            for zone, pin in coordsToPins(npc.spawns, 'Started by: '+npc.name, imgSrc='available', width=2):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
    if hasattr(quest, 'goStart'):
        for goId in quest.goStart:
            obj = objects.objectList[goId]
            for zone, pin in coordsToPins(obj.spawns, 'Started by: '+obj.name, imgSrc='available', width=2):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
    if hasattr(quest, 'creatureEnd'):
        for npcId in quest.creatureEnd:
            npc = npcs.nList[npcId]
            for zone, pin in coordsToPins(npc.spawns, 'Finished by: '+npc.name, imgSrc='complete', width=2):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
    if hasattr(quest, 'goEnd'):
        for goId in quest.goEnd:
            obj = objects.objectList[goId]
            for zone, pin in coordsToPins(obj.spawns, 'Finished by: '+obj.name, imgSrc='complete', width=2):
                if zone not in pinList:
                    pinList[zone] = []
                pinList[zone].append(pin)
    if len(pinList) > 0:
        data['pinList'] = pinList
    ""
    data['quest'] = quest
    data['zoneNames'] = zoneNames
    data['quests'] = quests
    data['npcs'] = npcs
    data['objects'] = objects
    data['itms'] = items
    return flask.render_template('quest.html', data=data)
