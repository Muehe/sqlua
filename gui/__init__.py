import flask

from config import *

from db.NpcList import *
from db.QuestList import *
from db.ObjList import *
from db.ItemList import *

from gui.questPage import *
from gui.npcPage import *
from gui.objectPage import *
from gui.itemPage import *

npcs = NpcList(None, None, version, recache=False)
quests = QuestList(None, None, version, recache=False)
objects = ObjList(None, None, version, recache=False)
items = ItemList(None, version, recache=False)

app = flask.Flask(__name__)

@app.route('/')
def index():
    data = {'npcs': npcs, 'quests': quests, 'objects': objects, 'itms': items} # items is a jinja-builtin
    return flask.render_template('index.html', data=data)

@app.route('/quest/<int:questID>')
def quest(questID):
    return questPage(questID, quests, npcs, objects, items)

@app.route('/npc/<int:npcID>')
def npc(npcID):
    return npcPage(npcID, npcs, quests)

@app.route('/object/<int:objectID>')
def obj(objectID):
    return objectPage(objectID, objects, quests)

@app.route('/item/<int:itemID>')
def item(itemID):
    return itemPage(itemID, items, npcs, objects, quests)
