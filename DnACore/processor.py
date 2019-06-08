import re
import constants as k
import json

# def average_20mins(name, list):
#     if len(list) > 25:
#         data = list[len(list)-1].data
#         time = list[len(list)-1].posix_time
#         name = name
#
#         # dp = {"data": data, "posix_time": time, "name": name}
#         dp = '{"data": ' + str(data) + ', "time": ' + str(time) + ', "name": "' + str(name) + '"}'
#         with open(name + ".json", "w") as f:
#             f.write(dp)
#         print(dp)

def average_20mins(name, list):
    if len(list) > 25:
        list = list[len(list)-20:]
        time = list[len(list) - 1].posix_time
        name = name

        data = list[len(list)-1].data
        value = float(0)
        for d in list:
            value = value + float(d.data)
        value = round((value / len(list)), 1)

        dp = {"data": value, "posix_time": time, "name": name}
        savefile = name + ".json"
        with open(savefile, "w") as f:
            json.dump(dp, f)

