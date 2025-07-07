import sqlite3
import os

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect("data/civ_combos.db")
cursor = conn.cursor()

# Drop the existing combos table if it exists
cursor.execute("DROP TABLE IF EXISTS combos")

# Create a new combos table without the synergy field
cursor.execute("""
CREATE TABLE combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    leader TEXT NOT NULL,
    civ TEXT NOT NULL,
    abilities TEXT NOT NULL
)
""")

# Save and close the connection
conn.commit()
conn.close()