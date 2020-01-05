import sqlite3

conn = sqlite3.connect('riometer.db')

# Purge tables if they exists, then recreate
conn.execute("DROP TABLE IF EXISTS 'station'")
conn.commit()
conn.execute("CREATE TABLE station(station_id text primary key)")
conn.commit()
conn.execute("DROP TABLE IF EXISTS 'station_data'")
conn.commit()
conn.execute("CREATE TABLE station_data(station_id text, posix_time text, data_value text, FOREIGN KEY(station_id) REFERENCES station(station_id))")
conn.commit()

# Add the station.
conn.execute("INSERT INTO 'station' VALUES('FK2')")
conn.commit()