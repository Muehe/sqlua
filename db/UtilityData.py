npcFlagsClassic = {
    0: 'NONE',
    1: 'GOSSIP',
    2: 'QUESTGIVER',
    4: 'VENDOR',
    8: 'FLIGHTMASTER',
    16: 'TRAINER',
    32: 'SPIRITHEALER',
    64: 'SPIRITGUIDE',
    128: 'INNKEEPER',
    256: 'BANKER',
    512: 'PETITIONER',
    1024: 'TABARDDESIGNER',
    2048: 'BATTLEMASTER',
    4096: 'AUCTIONEER',
    8192: 'STABLEMASTER',
    16384: 'REPAIR',
}

npcFlagsTBC = {
    0: 'NONE',
    1: 'GOSSIP',
    2: 'QUESTGIVER',
    4: 'UNK1',
    8: 'UNK2',
    16: 'TRAINER',
    32: 'TRAINER_CLASS',
    64: 'TRAINER_PROFESSION',
    128: 'VENDOR',
    256: 'VENDOR_AMMO',
    512: 'VENDOR_FOOD',
    1024: 'VENDOR_POISON',
    2048: 'VENDOR_REAGENT',
    4096: 'REPAIR',
    8192: 'FLIGHTMASTER',
    16384: 'SPIRITHEALER',
    32768: 'SPIRITGUIDE',
    65536: 'INNKEEPER',
    131072: 'BANKER',
    262144: 'PETITIONER',
    524288: 'TABARDDESIGNER',
    1048576: 'BATTLEMASTER',
    2097152: 'AUCTIONEER',
    4194304: 'STABLEMASTER',
    8388608: 'GUILD_BANKER',
    1677216: 'SPELLCLICK',
}

ranks = {
    0: 'NORMAL',
    1: 'ELITE',
    2: 'RAREELITE',
    3: 'WORLDBOSS',
    4: 'RARE',
    5: 'UNKNOWN',
}

itemFlags ={
    0: 'None',
    1: 'Soulbound',
    2: 'Conjured',
    4: 'Lootable (can be opened by right-click)',
    8: 'Wrapped',
    32: 'Totem',
    64: 'Activatable with right-click',
    256: 'Wrapper',
    1024: 'Gifts',
    2048: 'Item is party loot and can be looted by all',
    8192: 'Charter (Arena or Guild)',
    32768: 'PvP reward item',
    524288: 'Unique equipped (player can only have one equipped at the same time)',
    4194304: 'Throwable (for tooltip ingame)',
    8388608: 'Special Use',
}

itemClass = {
    0: 'Consumable',
    1: 'Container',
    2: 'Weapon',
    3: 'Gem',
    4: 'Armor',
    5: 'Reagent',
    6: 'Projectile',
    7: 'Trade Goods',
    8: 'Generic(OBSOLETE)',
    9: 'Recipe',
    10: 'Money(OBSOLETE)',
    11: 'Quiver',
    12: 'Quest',
    13: 'Key',
    14: 'Permanent(OBSOLETE)',
    15: 'Miscellaneous',
    16: 'Glyph',
}

itemSubclass = {
    0: { # Consumable
        0: 'Consumable',
        1: 'Potion',
        2: 'Elixir',
        3: 'Flask',
        4: 'Scroll',
        5: 'Food & Drink',
        6: 'Item Enhancement',
        7: 'Bandage',
        8: 'Other',
    },
    1: { # Container
        0: 'Bag',
        1: 'Soul Bag',
        2: 'Herb Bag',
        3: 'Enchanting Bag',
        4: 'Engineering Bag',
        5: 'Gem Bag',
        6: 'Mining Bag',
        7: 'Leatherworking Bag',
    },
    2: { # Weapon
        0: 'Axe (One handed)',
        1: 'Axe (Two handed)',
        2: 'Bow',
        3: 'Gun',
        4: 'Mace (One handed)',
        5: 'Mace (Two handed)',
        6: 'Polearm',
        7: 'Sword (One handed)',
        8: 'Sword (Two handed)',
        9: 'Obsolete',
        10: 'Staff',
        11: 'Exotic',
        12: 'Exotic',
        13: 'Fist Weapon',
        14: 'Miscellaneous',
        15: 'Dagger',
        16: 'Thrown',
        17: 'Spear',
        18: 'Crossbow',
        19: 'Wand',
        20: 'Fishing pole',
    },
    3: { # Gems
        0: 'Red',
        1: 'Blue',
        2: 'Yellow',
        3: 'Purple',
        4: 'Green',
        5: 'Orange',
        6: 'Meta',
        7: 'Simple',
        8: 'Prismatic',
    },
    4: { # Armor
        0: 'Miscellaneous',
        1: 'Cloth',
        2: 'Leather',
        3: 'Mail',
        4: 'Plate',
        5: 'Buckler(OBSOLETE)',
        6: 'Shield',
        7: 'Libram',
        8: 'Idol',
        9: 'Totem',
    },
    5: { # Reagent
        0: 'Reagent',
    },
    6: { # Projectile
        0: 'Wand(OBSOLETE)',
        1: 'Bolt(OBSOLETE)',
        2: 'Arrow',
        3: 'Bullet',
        4: 'Thrown(OBSOLETE)',
    },
    7: { # Trade Goods
        0: 'Trade Goods',
        1: 'Parts',
        2: 'Explosives',
        3: 'Devices',
        4: 'Jewelcrafting',
        5: 'Cloth',
        6: 'Leather',
        7: 'Metal & Stone',
        8: 'Meat',
        9: 'Herb',
        10: 'Elemental',
        11: 'Other',
        12: 'Enchanting',
    },
    8: { # Generic(OBSOLETE)
        0: 'Generic(OBSOLETE)',
    },
    9: { # Recipe
        0: 'Book',
        1: 'Leatherworking',
        2: 'Tailoring',
        3: 'Engineering',
        4: 'Blacksmithing',
        5: 'Cooking',
        6: 'Alchemy',
        7: 'First Aid',
        8: 'Enchanting',
        9: 'Fishing',
        10: 'Jewelcrafting',
    },
    10: { # Money(OBSOLETE)
        0: 'Money(OBSOLETE)',
    },
    11: { # Quiver
        0: 'Quiver(OBSOLETE)',
        1: 'Quiver(OBSOLETE) 	',
        2: 'Quiver',
        3: 'Ammo Pouch',
    },
    12: { # Quest
        0: 'Quest',
    },
    13: { # Key
        0: 'Key',
        1: 'Lockpick',
    },
    14: { # Permanent(OBSOLETE)
        0: 'Permanent',
    },
    15: { # Miscellaneous
        0: 'Junk',
        1: 'Reagent',
        2: 'Pet',
        3: 'Holiday',
        4: 'Other',
        5: 'Mount',
    },
    16: { # Glyph
        0: '',
        1: 'Warrior',
        2: 'Paladin',
        3: 'Hunter',
        4: 'Rogue',
        5: 'Priest',
        6: 'Death Knight',
        7: 'Shaman',
        8: 'Mage',
        9: 'Warlock',
        10: '',
        11: 'Druid',
    },
}

foodType = {
    1: 'Meat',
    2: 'Fish',
    3: 'Cheese',
    4: 'Bread',
    5: 'Fungus',
    6: 'Fruit',
    7: 'Raw Meat',
    8: 'Raw Fish',
}

ammoType = {
    2: 'Arrows',
    3: 'Bullets',
}

QuestObjectiveType = {
    0: 'QUEST_OBJECTIVE_MONSTER', # kill
    1: 'QUEST_OBJECTIVE_ITEM', # collect
    2: 'QUEST_OBJECTIVE_GAMEOBJECT', # interact object
    3: 'QUEST_OBJECTIVE_TALKTO', # interact npc
    4: 'QUEST_OBJECTIVE_CURRENCY',
    5: 'QUEST_OBJECTIVE_LEARNSPELL',
    6: 'QUEST_OBJECTIVE_MIN_REPUTATION',
    7: 'QUEST_OBJECTIVE_MAX_REPUTATION',
    8: 'QUEST_OBJECTIVE_MONEY',
    9: 'QUEST_OBJECTIVE_PLAYERKILLS',
    10: 'QUEST_OBJECTIVE_AREATRIGGER',
    11: 'QUEST_OBJECTIVE_WINPETBATTLEAGAINSTNPC',
    12: 'QUEST_OBJECTIVE_DEFEATBATTLEPET',
    13: 'QUEST_OBJECTIVE_WINPVPPETBATTLES',
    14: 'QUEST_OBJECTIVE_CRITERIA_TREE',
    15: 'QUEST_OBJECTIVE_PROGRESS_BAR',
    16: 'QUEST_OBJECTIVE_HAVE_CURRENCY', # requires the player to have X currency when turning in but does not consume it
    17: 'QUEST_OBJECTIVE_OBTAIN_CURRENCY', # requires the player to gain X currency after starting the quest but not required to keep it until the end (does not consume)
    18: 'QUEST_OBJECTIVE_INCREASE_REPUTATION', # requires the player to gain X reputation with a faction
    19: 'QUEST_OBJECTIVE_AREA_TRIGGER_ENTER',
    20: 'QUEST_OBJECTIVE_AREA_TRIGGER_EXIT',
    21: 'QUEST_OBJECTIVE_KILL_WITH_LABEL',
}

QuestObjectiveTypeKey = {v: k for k, v in QuestObjectiveType.items()}

QuestObjectiveFlags = {
    0: 'QUEST_OBJECTIVE_FLAG_NONE',
    1: 'QUEST_OBJECTIVE_FLAG_TRACKED_ON_MINIMAP', # client displays large yellow blob on minimap for creature/gameobject
    2: 'QUEST_OBJECTIVE_FLAG_SEQUENCED', # client will not see the objective displayed until all previous objectives are completed
    4: 'QUEST_OBJECTIVE_FLAG_OPTIONAL', # not required to complete the quest
    8: 'QUEST_OBJECTIVE_FLAG_HIDDEN', # never displayed in quest log
    16: 'QUEST_OBJECTIVE_FLAG_HIDE_CREDIT_MSG', # skip showing item objective progress
    32: 'QUEST_OBJECTIVE_FLAG_PRESERVE_QUEST_ITEMS',
    64: 'QUEST_OBJECTIVE_FLAG_PART_OF_PROGRESS_BAR', # hidden objective used to calculate progress bar percent (quests are limited to a single progress bar objective)
    128: 'QUEST_OBJECTIVE_FLAG_KILL_PLAYERS_SAME_FACTION',
    256: 'QUEST_OBJECTIVE_FLAG_NO_SHARE_PROGRESS',
    521: 'QUEST_OBJECTIVE_FLAG_IGNORE_SOULBOUND_ITEMS',
}

raceIDs = {
    'NONE': 0,
    'HUMAN': 1,
    'ORC': 2,
    'DWARF': 4,
    'NIGHT_ELF': 8,
    'UNDEAD': 16,
    'TAUREN': 32,
    'GNOME': 64,
    'TROLL': 128,
    'GOBLIN': 256,
    'BLOOD_ELF': 512,
    'DRAENEI': 1024,
    'WORGEN': 2097152,
    'PANDAREN_N': 8388608,
    'PANDAREN_A': 16777216,
    'PANDAREN_H': 33554432,
}

raceIDsByKey = {v: k for k, v in raceIDs.items()}

raceCombos = {
    'CLASSIC_ALLIANCE': 77,
    'CLASSIC_HORDE': 178,
    'CLASSIC_ALL': 255,
    'TBC_ALLIANCE': 1101,
    'TBC_HORDE': 690,
    'TBC_ALL': 1791,
    'CATA_ALLIANCE': 2098253,
    'CATA_HORDE': 946,
    'CATA_ALL': 2099199,
    'MOP_ALLIANCE': 18875469,
    'MOP_HORDE': 33555378,
    'MOP_ALL': 60819455,
}

raceCombosByKey = {v: k for k, v in raceCombos.items()}

classIDs = {

}

questType = {
    "Elite": 1,
    "Life": 21,
    "PvP": 41,
    "Raid": 62,
    "Dungeon": 81,
    "World Event": 82,
    "Legendary": 83,
    "Escort": 84,
    "Heroic": 85,
    "Raid (10)": 88,
    "Raid (25)": 89,
    "Scenario": 98,
    "Account": 102,
    "Celestial": 294,
}

questTypeByKey = {v: k for k, v in questType.items()}
