import sqlite3

connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    discord_id TEXT PRIMARY KEY,
    name TEXT
    email TEXT
    token TEXT
    password TEXT
)""")

connectionDB.commit()
print('Tabla creada!')
