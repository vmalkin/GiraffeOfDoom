import numpy as np, os, matplotlib.pyplot as plt
from datetime import datetime


def nmeaParser(array):
    newArray = []
    currentPackage = []

    for row in array:
        try:
            if row[1] == 'G' and row[2] == 'P' and row[3] == 'G' and row[4] == 'S' and row[5] == 'V':
                gpgsv = row.split(',')
                gpgsv = gpgsv[4 : len(gpgsv)]
                gpgsv[len(gpgsv)-1] = gpgsv[len(gpgsv) - 1].split('*')[0]
                i = 0

                while i <= len(gpgsv) - 4:
                    currentPackage.append(';'.join(gpgsv[i : i + 4]) + ';')
                    i += 4

            elif row[1] == 'G' and row[2] == 'P' and row[3] == 'Z' and row[4] == 'D' and row[5] == 'A':
                gpzda = ';'.join(row.split(',')[1 : 5]) + ';'
                for newRow in currentPackage:
                    newArray.append(gpzda + newRow)
                currentPackage = []

        except Exception as e:
            pass

    return newArray


def getTime(dateStr):
    dateStr = dateStr[:2] + ';' + dateStr[2:4] + ';' + dateStr[4:6] + ';' + dateStr[11:]
    date = datetime.strptime(dateStr, '%H;%M;%S;%d;%m;%Y')
    return date


def getSummary(array):
    minute = array[1].split(';')[0][2 : 4]
    returnArray = []
    summary = []
    summarize = []

    for i in range(1, len(array)):
        snr = array[i].split(';')[7]
        elevation = array[i].split(';')[7]

        if i == len(array) - 1 or minute != array[i + 1].split(';')[0][2 : 4]:
            if i != len(array) - 1:
                minute = array[i + 1].split(';')[0][2 : 4]
                time = ';'.join(array[i].split(';')[0 : 4])

        if len(summarize) > 0:
            summary.append({
                'time': getTime(time),
                's4': 100.0 * S4Index(summarize),
                'elevation': float(elevation)
                })

            summarize=[]

        if snr != "":
            summarize.append(snr)

    return summary


def S4Index(array):
    intensity = []

    for snr in array:
        intensity.append((10.0 ** (float(snr) / 10.0)))

    s4 = round(1.0 * np.std(intensity) / np.mean(intensity), 3)
    return s4


def plot(x, y, yy, prn, directory):
    plt.plot(x, y, 'r--', x, yy, 'b--')
    plt.ylim([0,90])
    plt.title('PRN ' + prn)
    plt.legend(['100 * S4', 'Elevation'])
    plt.savefig(directory + '/' + prn + '.png', bbox_inches='tight')
    plt.close()


def getNmea():
    array = []

    with open('nmea_example.txt', 'rb') as f:
        for line in f:
            array.append(line[:len(line) - 1])

    return array


if __name__ == "__main__":
    array = getNmea()
    array = nmeaParser(array)
    prns = set([ elem.split(';')[4] for elem in array])
    now = datetime.now()
    directory = 'images_nmea_parser_'+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.second)

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(prns)

    for prn in prns:
        try:
            filtered_array = [elem for elem in array if elem.split(';')[4] == prn]
            array_to_plot = getSummary(filtered_array)
            x = [el['time'] for el in array_to_plot]
            y = [el['s4'] for el in array_to_plot]
            yy = [el['elevation'] for el in array_to_plot]
            plot(x, y, yy, prn, directory)

        except Exception as e:
            pass
