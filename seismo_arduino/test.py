import plotter_helicorder
import os
import constants as k

result_1d = []

with open('datagenerator.csv', 'r') as d:
    for item in d:
        try:
            date = float(item[0])
            data = int(item[1])
            row = [date, data]
            result_1d.append(row)
        except:
            print(f'Invalid data: {item}')

def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


for directory in k.dir_images:
    try_create_directory(directory)


print(len(result_1d))
plotter_helicorder.wrapper(result_1d)




