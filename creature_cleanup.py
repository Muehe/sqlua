import config
import pymysql

trinity_connection = pymysql.connect(
    host=config.dbInfo['host'],
    user=config.dbInfo['user'],
    password=config.dbInfo['password'],
    database='trinity',
    port=config.dbInfo["port"],
    charset='utf8'
)
t_cursor = trinity_connection.cursor(pymysql.cursors.DictCursor)

mangos_connection = pymysql.connect(
    host=config.dbInfo['host'],
    user=config.dbInfo['user'],
    password=config.dbInfo['password'],
    database='mangos3',
    port=config.dbInfo["port"],
    charset='utf8'
)
m_cursor = mangos_connection.cursor(pymysql.cursors.DictCursor)

t_cursor.execute("SELECT entry from creature_template")

## Print all entries that are in trinity but not in mangos3
trinity_entries = set()
for row in t_cursor.fetchall():
    trinity_entries.add(row['entry'])

mangos_entries = set()
m_cursor.execute("SELECT Entry from creature_template")
for row in m_cursor.fetchall():
    mangos_entries.add(row['Entry'])

entries = trinity_entries - mangos_entries

# sort entries
entries = list(entries)
entries.sort()

print("Entries in trinity but not in mangos3:")
for entry in entries:
    print(str(entry) + ",")
