import os
import constants as k
import standard_stuff

class File_Object:
    def __init__(self, utcday):
        self.utcday = utcday
        self.data = []
        self.savefile = k.dir_saves['logs'] + os.sep + utcday + '.csv'

    def append_savefile(self):
        with open(self.savefile, 'a') as f:
            for item in self.data:
                d = f'{item[0]}, {item[1]}'
                f.write(d + '\n')
            f.close()


def csv_save(parseddata):
    # [1737274820, 21.05]
    # Create list of CSV filenames based on parsed data.

    print(f'*** Creating Logfile START')
    print(f'PASS 1: Create file object list.')
    file_object_list = []
    oldname = None
    for item in parseddata:
        utc_day = standard_stuff.posix2utc(item[0], '%Y-%m-%d')
        if oldname != utc_day:
            file_object_list.append(File_Object(utc_day))
            oldname = utc_day

    print(f'PASS 2: Add data to file objects.')
    for file_object in file_object_list:
        for item in parseddata:
            if standard_stuff.posix2utc(item[0], '%Y-%m-%d') == file_object.utcday:
                file_object.data.append(item)

    print(f'PASS 3: Append data to disc files.')
    for file_object in file_object_list:
        file_object.append_savefile()
    print(f'*** Creating Logfile FINISHED')

