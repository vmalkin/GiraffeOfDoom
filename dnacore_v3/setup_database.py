import sqlite3
import constants as k

dna_core = sqlite3.connect(k.dbfile)

# PRAGMA foreign_keys = ON; for each NEW instance of a connector, otherwise FK constraints
#  are not enforced.

db = dna_core.cursor()

db.execute('drop table if exists station;')
db.execute('drop table if exists station_data;')
db.execute('PRAGMA foreign_keys = ON;')

db.execute('create table station ('
           'station_id text not null primary key'
           ');')

db.execute('create table station_data('
           'station_id text, '
           'posix_time text, '
           'data_value text, '
           'foreign key (station_id) references station(station_id)'
           ');'
           '')

stations = ["Ruru_Obs", "Dn_Aurora", "GOES_16", "Geomag_Bz", "SW_speed", "SW_Density"]

# Watch the syntax for the value to be passed into the query!
# https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta#16856730
for station in stations:
    db.execute("insert into station(station_id) values (?)", (station,))

dna_core.commit()

# for row in db.execute('select * from station'):
#     print(row)

db.close()