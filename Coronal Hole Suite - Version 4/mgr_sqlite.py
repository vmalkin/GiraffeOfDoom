import sqlite3

database = "solarwind.db"


def db_create():
    print("Creating database...")
    data_b = sqlite3.connect(database)
    db = data_b.cursor()
    db.execute("drop table if exists sat")
    db.execute("drop table if exists data")
    db.execute("drop table if exists type")

    db.execute("create table sat(sat_name text primary key)")
    db.execute("create table type(data_type text primary key)")
    db.execute("create table data("
               "posixtime integer,"
               "data real,"
               "sat_name text,"
               "data_type text,"
               "foreign key sat_name references sat(sat_name),"
               "foreign key data_type references type(data_type)"
               ")")
    data_b.commit()
    db.close()


def db_populate():
    pass
