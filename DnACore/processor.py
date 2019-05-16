import re
import constants as k

def average_20mins(name, list):
    if len(list) > 25:
        data = list[len(list)-1].data
        time = list[len(list)-1].posix_time
        name = name

        # dp = {"data": data, "posix_time": time, "name": name}
        dp = '{"data": ' + str(data) + ', "time": ' + str(time) + ', "name": "' + str(name) + '"}'
        with open(name + ".json", "w") as f:
            f.write(dp)
        print(dp)
