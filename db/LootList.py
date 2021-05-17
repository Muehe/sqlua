class LootList():
    def __init__(self, tablePrefix, dictCursor):
        self.lootList = {}
        dictCursor.execute('SELECT entry AS id, item, ChanceOrQuestChance, groupid, mincountOrRef FROM {}_loot_template'.format(tablePrefix))
        loot_tpl = dictCursor.fetchall()
        for line in loot_tpl:
            if line['id'] in self.lootList:
                if not line['groupid'] in self.lootList[line['id']]:
                    self.lootList[line['id']][line['groupid']] = {'equalyChanced':[], 'explicitlyChanced':[], 'totalChance':0}
                self.__addLine(line)
            else:
                self.lootList[line['id']] = {}
                self.lootList[line['id']][line['groupid']] = {'equalyChanced':[], 'explicitlyChanced':[], 'totalChance':0}
                self.__addLine(line)
        for loot in self.lootList:
            for group in self.lootList[loot]:
                if self.lootList[loot][group]['equalyChanced'] == []:
                    self.lootList[loot][group]['equalyChanced'] = False
                if self.lootList[loot][group]['explicitlyChanced'] == []:
                    self.lootList[loot][group]['explicitlyChanced'] = False
                if self.lootList[loot][group]['explicitlyChanced']:
                    for line in self.lootList[loot][group]['explicitlyChanced']:
                        if line['chance'] > 0:
                            self.lootList[loot][group]['totalChance'] += line['chance']

    def __addLine(self, line):
        if line['ChanceOrQuestChance'] == 0:
            if line['mincountOrRef'] < 0:
                self.lootList[line['id']][line['groupid']]['equalyChanced'].append({'id':-line['mincountOrRef'], 'type':'ref'})
            else:
                self.lootList[line['id']][line['groupid']]['equalyChanced'].append({'id':line['item'], 'type':'item'})
        else:
            if line['mincountOrRef'] < 0:
                self.lootList[line['id']][line['groupid']]['explicitlyChanced'].append({'id':-line['mincountOrRef'], 'type':'ref', 'chance':line['ChanceOrQuestChance']})
            else:
                self.lootList[line['id']][line['groupid']]['explicitlyChanced'].append({'id':line['item'], 'type':'item', 'chance':line['ChanceOrQuestChance']})
