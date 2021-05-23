import flask

from db.CoordData import *
from db.UtilityData import *
from gui.utility import *

def npcPage(npcID, npcs, quests):
    if npcID not in npcs.nList:
        return 'Unknown NPC'
    data = {}
    npc = npcs.nList[npcID]
    data['hasSpawns'] = len(npc.spawns.cByZone) > 0
    data['spawns'] = npc.spawns.cByZone
    data['hasDifferentLevels'] = npc.minlevel != npc.maxlevel
    data['hasSubName'] = npc.subName != '' and npc.subName != None
    data['starts'] = []
    if hasattr(npc, 'start'):
        for questID in npc.start:
            data['starts'].append(quests.qList[questID])
    data['hasStart'] = len(data['starts']) > 0
    data['ends'] = []
    if hasattr(npc, 'end'):
        for questID in npc.end:
            data['ends'].append(quests.qList[questID])
    data['hasEnd'] = len(data['ends']) > 0
    npcFlags = {}
    if npc.version == 'classic':
        npcFlags = npcFlagsClassic
    else:
        npcFlags = npcFlagsTBC
    data['activeFlags'] = []
    for flag in npcFlags:
        if flag > 0 and (npc.npcFlags & flag) == flag:
            data['activeFlags'].append((flag, npcFlags[flag]))
    if len(data['activeFlags']) == 0:
        data['activeFlags'].append((0, npcFlags[0]))
    if data['hasSpawns']:
        pinList = {}
        for zone in npc.spawns.cByZone:
            if zone == 0:
                continue
            if zone not in pinList:
                pinList[zone] = []
            for coord in npc.spawns.cByZone[zone]:
                pinList[zone].append(createPinDict('Spawn: '+npc.name, coord[0], coord[1], color='blue', opacity=0.7, imgSrc='glow2', width=2))
        data['pinList'] = pinList

    data['zoneNames'] = zoneNames
    data['ranks'] = ranks

    return flask.render_template('npc.html', data=data, npc=npc)
