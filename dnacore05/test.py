import sqlite3
import constants as k

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
db.execute("insert into station(station_id) values (?)", ("GOES_17"))