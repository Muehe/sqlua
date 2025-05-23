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
