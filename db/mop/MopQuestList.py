from db.QuestList import QuestList

import os.path
import pickle

from db.Utilities import read_quest_ids
from db.cata.readTrinityQuestList import read_trinity_quest_list
from db.mop.readSkyfireQuestList import read_skyfire_quest_list


class MopQuestList(QuestList):

    def __init__(self, version):
        super().__init__(version)

    def run(self, cursor, dictCursor, db_flavor, recache=False):
        if not os.path.isfile(f'data/mop/quests.pkl') or recache:
            dicts = load_quests(cursor, dictCursor, db_flavor)
            print('Caching quests...')
            self.cacheQuests(dicts)
        else:
            try:
                with open(f'data/mop/quests.pkl', 'rb') as f:
                    self.qList = pickle.load(f)
                print('Using cached quests.')
            except:
                print('ERROR: Something went wrong while loading cached quests. Re-caching.')
                dicts = load_quests(cursor, dictCursor, db_flavor)
                self.cacheQuests(dicts)

def load_quests(cursor, dictCursor, db_flavor):
    if db_flavor == 'trinity':
        quest_ids = read_quest_ids('./data/mop/mopQuestIds.txt')
        return read_trinity_quest_list(cursor, dictCursor, quest_ids)
    else:
        return read_skyfire_quest_list(cursor, dictCursor)
