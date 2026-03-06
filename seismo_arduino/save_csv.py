import constants as k
import time
import os
import mgr_database
import standard_stuff


def savedata(queryresult):
    # create logfile
    nowtime = time.time()
    # filename = standard_stuff.posix2utc(nowtime, '%Y-%m-%d') + '.csv'
    # savefile = k.dir_saves['logs'] + os.sep + filename
    # time_start_24hr = nowtime - (60 * 60 * 24)
    # result_24hr = mgr_database.db_data_get(time_start_24hr)
    result_24hr = mgr_database.db_data_get(queryresult)
    initialdate = standard_stuff.posix2utc(result_24hr[0], '%Y-%m-%d')

    # skip the first set of dates in the data
    # if the date changes, close old file if exists, open a new file.
    # if the next record has the same date, append to open file.
    # has the date changed?
    # when all records done, fin!

    if len(result_24hr) > 0:
        try:
            with open(savefile, 'w') as s:
                for line in result_24hr:
                    d = f'{line[0]}, {line[1]}, {line[2]}, {line[3]}\n'
                    s.write(d)
            s.close()
        except:
            print(f'Unable to write to logfile {savefile}')