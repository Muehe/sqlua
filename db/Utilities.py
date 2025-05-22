localesMap = {
'enUS': 0,
'koKR': 1,
'frFR': 2,
'deDE': 3,
'zhCN': 4,
'twCN': 5, # ?
'esES': 6,
'esSA': 7, # ?
'ruRU': 8,
}

def escapeDoubleQuotes(inp):
    if inp is None:
        return inp
    name = inp.replace('"', '\\"').lstrip().rstrip()
    return name

def escapeQuotes(inp):
    if inp is None:
        return inp
    name = inp.replace("'", "\\'").lstrip().rstrip()
    return name

def removeTrailingData(inp):
    #Remove trailing comma/data
    for i in range(1, 10): #That degree really pays off!
        inp = inp.replace('nil,}', '}')
    inp = inp.replace(",}", "}")
    inp = inp.replace(",nil}", "}")
    inp = inp.replace("{}", "nil")
    return inp

# Reads the quest IDs by line from a given file.
def read_quest_ids(file_path: str) -> list[int]:
    print("Reading quest IDs from", file_path)
    with open(file_path, 'r') as file:
        return [int(line.strip()) for line in file if line.strip().isdigit()]
