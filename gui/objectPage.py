import flask

from db.CoordData import *
from gui.utility import *

def objectPage(objectID, objects, quests):
    if objectID not in objects.objectList:
        return 'Unknown Object'
    data = {}
    obj = objects.objectList[objectID]

    data['starts'] = []
    if hasattr(obj, 'start'):
        for questID in obj.start:
            data['starts'].append(quests.qList[questID])
    data['hasStart'] = len(data['starts']) > 0
    data['ends'] = []
    if hasattr(obj, 'end'):
        for questID in obj.end:
            data['ends'].append(quests.qList[questID])
    data['hasEnd'] = len(data['ends']) > 0

    data['hasSpawns'] = len(obj.spawns.cByZone) > 0
    if data['hasSpawns']:
        pinList = {}
        for zone in obj.spawns.cByZone:
            if zone == 0:
                continue
            if zone not in pinList:
                pinList[zone] = []
            for coord in obj.spawns.cByZone[zone]:
                pinList[zone].append(createPinDict('Spawn: '+obj.name, coord[0], coord[1], color='yellow', opacity=0.7, imgSrc='glow2', width=2))
        data['pinList'] = pinList
    data['zoneNames'] = zoneNames

    return flask.render_template('object.html', data=data, obj=obj)
