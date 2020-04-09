import sqlite3
import constants as k

dna_core = sqlite3.connect(k.dbfile)

# PRAGMA foreign_keys = ON; for each NEW instance of a connector, otherwise FK constraints
#  are not enforced.

db = dna_core.cursor()

# db.execute('drop table if exists station;')
# db.execute('drop table if exists station_data;')
# db.execute('drop table if exists station_statistics;')
db.execute('PRAGMA foreign_keys = ON;')

try:
    db.execute('create table station_statistics ('
               'station_id text not null,'
               'std_dev real,'
               'foreign key (station_id) references station(station_id)'
               ');')
except sqlite3.OperationalError:
    pass

try:
    db.execute('create table station ('
               'station_id text not null primary key'
               ');')
except sqlite3.OperationalError:
    pass

try:
    db.execute('create table station_data('
               'station_id text, '
               'posix_time integer, '
               'data_value text, '
               'foreign key (station_id) references station(station_id)'
               ');')
except sqlite3.OperationalError:
    pass

# Watch the syntax for the value to be passed into the query!
# https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta#16856730
try:
    for station in k.stations:
        db.execute("insert into station(station_id) values (?)", (station,))
except sqlite3.IntegrityError:
    pass

dna_core.commit()

# for row in db.execute('select * from station'):
#     print(row)

db.close()