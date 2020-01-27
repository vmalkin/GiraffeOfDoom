import sqlite3

dbfile = "dna_core.db"

db = sqlite3.connect(dbfile)

db.close()