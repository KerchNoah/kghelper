import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/civ_combos.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS combos")

cursor.execute("""
CREATE TABLE combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    leader TEXT NOT NULL,
    civ TEXT NOT NULL,
    abilities TEXT NOT NULL,
    synergy TEXT NOT NULL
)
""")

conn.commit()
conn.close()