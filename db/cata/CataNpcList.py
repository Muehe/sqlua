from db.NpcList import NpcList

import os.path
import pickle

from db.cata.readTrinityNpcList import read_trinity_npc_list


class CataNpcList(NpcList):
    def __init__(self, version, debug=False):
        super().__init__(version, debug)

    def run(self, cursor, dictCursor, db_flavor, recache=False, extractSpawns=True):
        if not os.path.isfile(f'data/cata/npcs.pkl') or recache:
            dicts = load_npcs(cursor, dictCursor, db_flavor)
            print('Caching NPCs...')
            self.cacheNpcs(dicts, extractSpawns)
        else:
            try:
                with open(f'data/cata/npcs.pkl', 'rb') as f:
                    self.nList = pickle.load(f)
                print('Using cached NPCs.')
            except:
                print('ERROR: Something went wrong while loading cached NPCs. Re-caching.')
                dicts = load_npcs(cursor, dictCursor, db_flavor)
                self.cacheNpcs(dicts, extractSpawns)


def load_npcs(cursor, dictCursor, db_flavor):
    if db_flavor == 'trinity':
        return read_trinity_npc_list(cursor, dictCursor)
