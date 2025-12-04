import plotter_helicorder
import os
import constants as k

result_1d = []

def try_create_directory(directory):
    if not os.path.isdir(directory):
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


for directory in k.dir_images:
    try_create_directory(directory)

with open('datagenerator.csv', 'r') as d:
    for item in d:
        try:
            ii = item.strip()
            i = ii.split(',')
            date = float(i[0])
            d1 = int(i[1])
            d2 = int(i[2])
            d3 = int(i[3])
            row = [date, d1, d2, d3]
            result_1d.append(row)
        except:
            print(f'Invalid data: {item}')

plotter_helicorder.wrapper(result_1d)




