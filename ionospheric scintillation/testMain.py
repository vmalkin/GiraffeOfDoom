import constants as k
import mgr_comport
import time
from threading import Thread
import os
import sqlite3

com = mgr_comport.SerialManager(k.portName,k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

sat_database = "gps_satellites.db"
gpsdb = sqlite3.connect(sat_database)
db = gpsdb.cursor()

class SatelliteCollator(Thread):
    def __init__(self):
        Thread.__init__(self, name="SatelliteCollator")

    def run(self):
        while True:
            pass  # do something here
            time.sleep(60)


def create_database():
    if not os.path.exists(sat_database):
        print("No database, creating file")

        db.execute('drop table if exists satdata')
        db.execute('create table satdata('
                   'sat_id text,'
                   'posixtime integer,'
                   'alt integer,'
                   'az integer,'
                   'snr integer'
                   ')')
        db.close()


def nmea_sentence(sentence):
    sentence = sentence[1:]
    sentence = sentence.split("*")
    sentence = sentence[0].split(",")
    return sentence


if __name__ == "__main__":
    # will create the database if it exists
    create_database()

    sat_collation = SatelliteCollator()
    try:
        sat_collation.start()
    except:
        print("Unable to start Satellite Collator")

    print("Starting GPS collection...")

    recordlength = 4
    while True:

        posix_time = int(time.time())
        line = com.data_recieve()
        sentence = nmea_sentence(line)
        constellation = sentence[0]
        s_id = 4
        s_alt = 5
        s_az = 6
        s_snr = 7

        # to determine how many records there are in the sentence. Minus the 4 slots at the front, div by four
        # to create the range for the FOR loop
        max_iter = int(((len(sentence) - 4) / 4) )

        # only if we have a sentence long enough
        if len(sentence) > recordlength + 4:
            for i in range(0, max_iter):
                # print(posix_time, constellation + "_" + sentence[s_id], sentence[s_alt], sentence[s_az], sentence[s_snr])
                sat_name = constellation + "_" + sentence[s_id]

                db = gpsdb.cursor()
                db.execute('insert into satdata(sat_id, posixtime, alt, az, snr) values (?, ?, ?, ?, ?)',[sat_name, posix_time, sentence[s_alt], sentence[s_az], sentence[s_snr]])
                gpsdb.commit()
                db.close()

                s_id = s_id + recordlength
                s_alt = s_alt + recordlength
                s_az = s_az + recordlength
                s_snr = s_snr + recordlength

