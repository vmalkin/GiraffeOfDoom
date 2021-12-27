import sqlite3
import common_data

database = common_data.database
"""
ERD: [satellite] 1..* [data] *..1 [data_type]
"""

def db_create():
    print("Creating database...")
    data_b = sqlite3.connect(database)
    db = data_b.cursor()
    db.execute("drop table if exists sat;")
    db.execute("drop table if exists data;")
    db.execute("drop table if exists type;")
    db.execute("create table sat(sat_name text primary key);")
    db.execute("create table type(data_type text primary key);")
    db.execute("create table data("
               "posixtime integer,"
               "data real,"
               "sat_name text,"
               "data_type text,"
               "foreign key (sat_name) references sat(sat_name),"
               "foreign key (data_type) references type(data_type)"
               ");")
    data_b.commit()
    db.close()


def db_populate():
    data_b = sqlite3.connect(database)
    db = data_b.cursor()
    db.execute("insert into sat (sat_name) values (?);", ["discovr"])
    db.execute("insert into sat (sat_name) values (?);", ["goes_primary"])
    db.execute("insert into sat (sat_name) values (?);", ["sdo"])
    db.execute("insert into data (data_type) values (?);", ["speed"])
    db.execute("insert into data (data_type) values (?);", ["density"])
    db.execute("insert into data (data_type) values (?);", ["forecast_speed"])
    db.execute("insert into data (data_type) values (?);", ["ch_coverage"])
    data_b.commit()
    db.close()


def db_insert_data(posixtime, data, sat_name, data_type):
    data_b = sqlite3.connect(database)
    db = data_b.cursor()
    db.execute("insert into data (posixtime, data, sat_name, data_type) values (?,?,?,?);",
               [int(posixtime), float(data), sat_name, data_type])
    data_b.commit()
    db.close()

def db_first_date():
    data_b = sqlite3.connect(database)
    db = data_b.cursor()
    result = db.execute("select min(posixtime) from data;")
    for item in result:
        returnvalue = item[0]
    db.close()
    return returnvalue

def db_last_date():
    data_b = sqlite3.connect(database)
    db = data_b.cursor()
    result = db.execute("select max(posixtime) from data;")
    for item in result:
        returnvalue = item[0]
    db.close()
    return returnvalue