from db.ObjList import ObjList

import os.path
import pickle

from db.cata.readMangosObjList import read_mangos_obj_list
from db.cata.readTrinityObjList import read_trinity_obj_list


class CataObjList(ObjList):
    def __init__(self, version):
        super().__init__(version)

    def run(self, cursor, db_flavor, extractSpawns=True, recache=False):
        if not os.path.isfile(f'data/cata/objects.pkl') or recache:
            dicts = load_objects(cursor, db_flavor)
            print('Caching objects...')
            self.cacheObjects(dicts, extractSpawns)
        else:
            try:
                with open(f'data/cata/objects.pkl', 'rb') as f:
                    self.objectList = pickle.load(f)
                print('Using cached objects.')
            except:
                print('ERROR: Something went wrong while loading cached objects. Re-caching.')
                dicts = load_objects(cursor, db_flavor)
                self.cacheObjects(dicts, extractSpawns)


def load_objects(cursor, db_flavor):
    if db_flavor == 'trinity':
        return read_trinity_obj_list(cursor)
    else:
        return read_mangos_obj_list(cursor)
