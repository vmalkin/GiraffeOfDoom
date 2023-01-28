
def wrapper(querydata):
    # query results format:
    # sat_id, posixtime, alt, az, s4, snr

    with open("test.csv", 'w') as t:
        for entry in querydata:
            d = str(entry[0]) + "," + str(entry[1]) + "," + str(entry[2]) + "," + str(entry[3]) + "," + str(entry[4]) + "," + str(entry[5]) + "\n"
            t.write(d)

    t.close()


