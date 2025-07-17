from sys import argv
from struct import unpack
import csv

file = argv[1]

with open(file, 'rb') as f:
    content = f.read()

dbcHeader = 'iiiii'
wmaEntry = 'iiiiffffiiiiii' #5.4.8

magic, record_count, field_count, record_size, string_block_size = unpack(dbcHeader, content[:20])

records = 20
string_block = records + record_size * record_count

entries = []

for i in range(0, record_count):
    start = records + i * record_size
    end = start + record_size
    entry = list(unpack(wmaEntry, content[start:end]))
    pointer = string_block+entry[3]
    entry[3] = ''
    while content[pointer] != 0:
        entry[3] += chr(content[pointer])
        pointer += 1
    entries.append(entry)

print(file)

with open(file+'.CSV', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(entries)
