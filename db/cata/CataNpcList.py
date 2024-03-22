from db.NpcList import NpcList

import os.path
import pickle


class CataNpcList(NpcList):
    """Holds a list of Npc() objects. Requires a pymysql cursor to cmangos classicdb."""

    def __init__(self, version, debug=False):
        super().__init__(version, debug)

    def run(self, cursor, dictCursor, recache=False, extractSpawns=True):
        if not os.path.isfile(f'data/cata/npcs.pkl') or recache:
            dicts = self.getNpcTables(cursor, dictCursor)
            print('Caching NPCs...')
            self.cacheNpcs(dicts, extractSpawns)
        else:
            try:
                with open(f'data/cata/npcs.pkl', 'rb') as f:
                    self.nList = pickle.load(f)
                print('Using cached NPCs.')
            except:
                print('ERROR: Something went wrong while loading cached NPCs. Re-caching.')
                dicts = self.getNpcTables(cursor, dictCursor)
                self.cacheNpcs(dicts, extractSpawns)

    def getNpcTables(self, cursor, dictCursor):
        print("Selecting NPC related MySQL tables...")

        print("  SELECT creature_template")
        # FactionAlliance and FactionHorde seem to contain the same data
        cursor.execute(
            "SELECT Entry, Name, MinLevel, MaxLevel, MinLevelHealth, MaxLevelHealth, `Rank`, FactionAlliance, SubName, NpcFlags, KillCredit1, KillCredit2 FROM creature_template")
        npc_tpl = []
        for a in cursor.fetchall():
            npc_tpl.append(a)

        print('  SELECT creature')
        cursor.execute('SELECT id, map, position_x, position_y, guid FROM creature')
        npc = {}
        for a in cursor.fetchall():
            if a[0] not in npc:
                npc[a[0]] = []
            npc[a[0]].append(a)

        print("  SELECT quest_relation")
        npc_start = {}
        npc_end = {}
        # actor 0=creature, 1=gameobject
        # entry=creature_template.entry or gameobject_template.entry
        # quest=quest_template.entry
        # role 0=start, 1=end
        cursor.execute("SELECT entry, quest, role FROM quest_relations WHERE actor=0")
        for a in cursor.fetchall():
            entry = a[0]
            quest = a[1]
            if a[2] == 0:
                if quest not in npc_start:
                    npc_start[quest] = []
                npc_start[quest].append((entry, quest))
            elif a[2] == 1:
                if quest not in npc_end:
                    npc_end[quest] = []
                npc_end[quest].append((entry, quest))

        print("  SELECT creature_movement")
        cursor.execute("SELECT point, id, position_x, position_y FROM creature_movement")
        npc_mov = {}
        for a in cursor.fetchall():
            if (a[1] in npc_mov):
                npc_mov[a[1]].append(a)
            else:
                npc_mov[a[1]] = []
                npc_mov[a[1]].append(a)

        print("  SELECT creature_movement_template")
        cursor.execute("SELECT point, entry, position_x, position_y, wpguid FROM creature_movement_template")
        npc_mov_tpl = {}
        for a in cursor.fetchall():
            if (a[1] in npc_mov_tpl):
                npc_mov_tpl[a[1]].append(a)
            else:
                npc_mov_tpl[a[1]] = []
                npc_mov_tpl[a[1]].append(a)

        print("  SELECT locales_creature")
        count = dictCursor.execute("SELECT * FROM locales_creature")
        loc_npc = {}
        for _ in range(0, count):
            q = dictCursor.fetchone()
            loc_npc[q['entry']] = q

        print("Done.")
        return {
            'npc_template': npc_tpl,
            'npc': npc,
            'npc_start': npc_start,
            'npc_end': npc_end,
            'npc_movement': npc_mov,
            'npc_movement_template': npc_mov_tpl,
            'locales_npc': loc_npc,
        }
