import sqlite3
import time

import constants as k

dna_old = sqlite3.connect(k.dbfile)
dna_new = sqlite3.connect("dna_core.new")

try:
    dna_new.execute('create table station ('
               'station_id text not null primary key'
               ');')
except:
    print("Error creating station table")

try:
    dna_new.execute('create table station_data('
               'station_id text, '
               'posix_time integer, '
               'data_value text, '
               'foreign key (station_id) references station(station_id)'
               ');')
except:
    print("Error creating station_data table")

try:
    dna_new.execute('create table events('
               'posix_time integer, '
               'station_id text, '
               'message text,'
               'foreign key (station_id) references station(station_id));')
except:
    print("Error creating events table")

try:
    dna_new.execute('create table dashboard('
               'posix_time integer, '
               'station_id text, '
               'message text,'
               'foreign key (station_id) references station(station_id));')
except:
    print("Error creating dashboard table")

# Watch the syntax for the value to be passed into the query!
# https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta#16856730
try:
    for station in k.stations:
        dna_new.execute("insert into station(station_id) values (?)", (station,))
except sqlite3.IntegrityError:
    pass

dna_new.commit()

for row in dna_new.execute('select * from station'):
    print(row)


# Get last two weeks of data from station_data in the old database.

nt = time.time()
starttime = nt - (14 * 86400)
result = dna_old.execute("select * from station_data where posix_time > ?", (starttime,))
for item in result:
    dna_new.execute("insert into station_data (station_id, posix_time, data_value) values (?,?,?)", (item[0], item[1], item[2],))

# I always forget this!
dna_new.commit()

# Close the databases
dna_old.close()
dna_new.close()