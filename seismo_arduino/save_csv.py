import constants as k
import time
import os
import mgr_database
import standard_stuff


def savedata():
    # create logfile
    nowtime = time.time()
    filename = standard_stuff.posix2utc(nowtime, '%Y-%m-%d') + '.csv'
    savefile = k.dir_saves['logs'] + os.sep + filename
    time_start_24hr = nowtime - (60 * 60 * 24)
    result_24hr = mgr_database.db_data_get(time_start_24hr)
    if len(result_24hr) > 0:
        try:
            with open(savefile, 'w') as s:
                for line in result_24hr:
                    l = line + '\n'
                    s.write(l)
            s.close()
        except:
            print(f'Unable to write to logfile {savefile}')