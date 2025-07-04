import flask
import pickle

from os.path import isfile

from main import *

from db.NpcList import *
from db.QuestList import *
from db.ObjList import *
from db.ItemList import *

from gui.questPage import *
from gui.questsPage import *
from gui.npcPage import *
from gui.objectPage import *
from gui.itemPage import *

dbs = {}
if False: #isfile('gui/cache.pkl'):
    with open('gui/cache.pkl', 'rb') as f:
        dbs = pickle.load(f)
else:
    for f in flavors:
        flavor = f
        dbs[f] =  {}
        for v in config.dbInfo[f]:
            version = v
            cursor, dictCursor = getCursors(version, flavor)
            quests, npcs, objects, items = getClassInstances(False, v, f)
            dbs[f][v] = {'quests': quests, 'npcs': npcs, 'objects': objects, 'items': items}
    #with open('gui/cache.pkl', 'wb') as f:
    #    pickle.dump(dbs, f, protocol=pickle.HIGHEST_PROTOCOL)

app = flask.Flask(__name__)

@app.route('/<string:f>/<string:v>')
def index(f, v):
    return flask.render_template('index.html', data={'npcs': dbs[f][v]['npcs'], 'quests': dbs[f][v]['quests'], 'objects': dbs[f][v]['objects'], 'itms': dbs[f][v]['items']}) # items is a jinja-builtin

@app.route('/quests/<int:questID>')
def quests(questID):
    return questsPage(questID, dbs)

@app.route('/<string:f>/<string:v>/quest/<int:questID>')
def quest(f, v, questID):
    return questPage(questID, dbs[f][v]['quests'], dbs[f][v]['npcs'], dbs[f][v]['objects'], dbs[f][v]['items'])

@app.route('/<string:f>/<string:v>/npc/<int:npcID>')
def npc(f, v, npcID):
    return npcPage(npcID, dbs[f][v]['npcs'], dbs[f][v]['quests'])

@app.route('/<string:f>/<string:v>/object/<int:objectID>')
def obj(f, v, objectID):
    return objectPage(objectID, dbs[f][v]['objects'], dbs[f][v]['quests'])

@app.route('/<string:f>/<string:v>/item/<int:itemID>')
def item(f, v, itemID):
    return itemPage(itemID, dbs[f][v]['items'], dbs[f][v]['npcs'], dbs[f][v]['objects'], dbs[f][v]['quests'])

@app.route('/hasmap/<int:mapID>')
def map(mapID):
    if isfile(f'static/maps/{mapID}.jpg'):
        return True
    else:
        return False
