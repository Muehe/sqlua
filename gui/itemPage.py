import flask

from db.CoordData import *
from db.UtilityData import *
from gui.utility import *

def itemPage(itemID, items, npcs, objects, quests):
    item = items.itemList[itemID]
    data = {}

    pinList = {}
    for npcID in item.npcs:
        npc = npcs.nList[npcID]
        for zone, pin in coordsToPins(npc.spawns, 'Dropped by: '+npc.name, imgSrc='slay', width=2):
            if zone not in pinList:
                pinList[zone] = []
            pinList[zone].append(pin)
    for objID in item.objects:
        obj = objects.objectList[objID]
        for zone, pin in coordsToPins(obj.spawns, 'Dropped by: '+obj.name, imgSrc='object', width=2):
            if zone not in pinList:
                pinList[zone] = []
            pinList[zone].append(pin)
    for npcID in item.vendors:
        npc = npcs.nList[npcID]
        for zone, pin in coordsToPins(npc.spawns, 'Sold by: '+npc.name, imgSrc='loot', width=2):
            if zone not in pinList:
                pinList[zone] = []
            pinList[zone].append(pin)
    if len(pinList) > 0:
        data['pinList'] = pinList

    data['activeFlags'] = []
    for flag in itemFlags:
        if flag > 0 and (item.flags & flag) == flag:
            data['activeFlags'].append((flag, itemFlags[flag]))
    if len(data['activeFlags']) == 0:
        data['activeFlags'].append((0, itemFlags[0]))

    data['item'] = item
    data['zoneNames'] = zoneNames
    data['ammoType'] = ammoType
    data['foodType'] = foodType
    data['itemClass'] = itemClass
    data['itemSubclass'] = itemSubclass
    return flask.render_template('item.html', data=data)
