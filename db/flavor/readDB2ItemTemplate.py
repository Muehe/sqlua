import csv

def getItemTemplate(version):
    buildVersions = {
        'classic': '1.15.7.61186',
        'tbc':'2.5.4.44833',
        'wotlk':'3.4.4.61187',
        'cata': '4.4.2.60895',
        'mop':'5.5.0.61208',
        'tww':'5.5.0.61208',
    }

    items = {}

    with open(f'data/{version}/Item.{buildVersions[version]}.csv') as file:
        for row in csv.DictReader(file):
            items[int(row['ID'])] = {'class': int(row['ClassID']), 'subclass': int(row['SubclassID']), 'RequiredLevel': int(row['RequiredLevel'])}
    with open(f'data/{version}/ItemSparse.{buildVersions[version]}.csv') as file:
        for row in csv.DictReader(file):
            qid = int(row['ID'])
            items[qid]['id'] = qid
            items[qid]['startquest'] = int(row['StartQuestID'])
            items[qid]['ItemLevel'] = int(row['ItemLevel'])
            items[qid]['name'] = row['Display_lang']
            items[qid]['ammo_type'] = int(row['AmmunitionType'])
            items[qid]['Flags'] = int(row['Flags_0'])
            items[qid]['FoodType'] = 0 # TODO
            #id, name, Flags, startquest, FoodType, ItemLevel, RequiredLevel, ammo_type, class, subclass

    ret = []
    for item in sorted(items.keys()):
        if not 'name' in items[item]:
            continue
        ret.append(items[item])

    return ret
