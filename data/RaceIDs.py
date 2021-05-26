import config

#Set a default
raceKeys = {
    "ALL_ALLIANCE"  :1101,  # 77
    "ALL_HORDE"     :690,   # 178
    #"ALL"           :1791,
    #"ALL"           :2047,
    "ALL"           :2047,  # 255
    "NONE"          :0,
    "HUMAN"         :1,
    "ORC"           :2,
    "DWARF"         :4,
    "NIGHT_ELF"     :8,
    "UNDEAD"        :16,
    "TAUREN"        :32,
    "GNOME"         :64,
    "TROLL"         :128,
    #GOBLIN         :256,
    "BLOOD_ELF"     :512,
    "DRAENEI"       :1024
}

if config.version == "tbc":
  print("Setting RaceKeys to TBC")
  raceKeys = {
    "ALL_ALLIANCE"  :1101,  # 77
    "ALL_HORDE"     :690,   # 178
    #"ALL"           :1791,
    #"ALL"           :2047,
    "ALL"           :2047,  # 255
    "NONE"          :0,
    "HUMAN"         :1,
    "ORC"           :2,
    "DWARF"         :4,
    "NIGHT_ELF"     :8,
    "UNDEAD"        :16,
    "TAUREN"        :32,
    "GNOME"         :64,
    "TROLL"         :128,
    #GOBLIN         :256,
    "BLOOD_ELF"     :512,
    "DRAENEI"       :1024
  }
else:
  print("Setting RaceKeys to Classic")
  raceKeys = {
    "ALL_ALLIANCE"  :77,  # 77
    "ALL_HORDE"     :178,   # 178
    #"ALL"           :1791,
    #"ALL"           :2047,
    "ALL"           :255,  # 255
    "NONE"          :0,
    "HUMAN"         :1,
    "ORC"           :2,
    "DWARF"         :4,
    "NIGHT_ELF"     :8,
    "UNDEAD"        :16,
    "TAUREN"        :32,
    "GNOME"         :64,
    "TROLL"         :128,
    #GOBLIN         :256,
    "BLOOD_ELF"     :512,
    "DRAENEI"       :1024
  }