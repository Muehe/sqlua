from db.ObjList import ObjList

import os.path
import pickle


class CataObjList(ObjList):
    def __init__(self, version):
        super().__init__(version)

    def run(self, cursor, extractSpawns=True, recache=False):
        if not os.path.isfile(f'data/cata/objects.pkl') or recache:
            print('Caching objects...')
            dicts = self.getObjTables(cursor)
            self.cacheObjects(dicts, extractSpawns)
        else:
            try:
                with open(f'data/cata/objects.pkl', 'rb') as f:
                    self.objectList = pickle.load(f)
                print('Using cached objects.')
            except:
                print('ERROR: Something went wrong while loading cached objects. Re-caching.')
                dicts = self.getObjTables(cursor)
                self.cacheObjects(dicts, extractSpawns)

    def getObjTables(self, cursor):
        print("Selecting object related MySQL tables...")
        print("  SELECT gameobject_template")
        cursor.execute("SELECT entry, name, type, faction, data1 FROM gameobject_template")
        obj_tpl = []
        for a in cursor.fetchall():
            obj_tpl.append(a)

        print(" SELECT gameobject")
        cursor.execute("SELECT id, map, position_x, position_y, guid FROM gameobject")
        obj = {}
        for a in cursor.fetchall():
            if a[0] not in obj:
                obj[a[0]] = []
            obj[a[0]].append(a)

        print("  SELECT quest_relation")
        obj_start = {}
        obj_end = {}
        # actor 0=creature, 1=gameobject
        # entry=creature_template.entry or gameobject_template.entry
        # quest=quest_template.entry
        # role 0=start, 1=end
        cursor.execute("SELECT entry, quest, role FROM quest_relations WHERE actor=1")
        for a in cursor.fetchall():
            entry = a[0]
            quest = a[1]
            if a[2] == 0:
                if quest not in obj_start:
                    obj_start[quest] = []
                obj_start[quest].append((entry, quest))
            elif a[2] == 1:
                if quest not in obj_end:
                    obj_end[quest] = []
                obj_end[quest].append((entry, quest))

        print("  SELECT locales_gameobject")
        cursor.execute("SELECT * FROM locales_gameobject")
        loc_obj = {}
        for a in cursor.fetchall():
            if (a[0] in loc_obj):
                loc_obj[a[0]].append(a)
            else:
                loc_obj[a[0]] = []
                loc_obj[a[0]].append(a)

        print("Done.")
        return {
            'object_template': obj_tpl,
            'object': obj,
            'object_start': obj_start,
            'object_end': obj_end,
            'locales_object': loc_obj
        }
