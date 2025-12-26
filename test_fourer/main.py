import requests
import os
import time
import constants as k
import plotter_spectrum_baro

#
# def try_create_directory(directory):
#     if os.path.isdir(directory) is False:
#         print("Creating image file directory...")
#         try:
#             os.makedirs(directory)
#             print("Directory created.")
#         except:
#             if not os.path.isdir(directory):
#                 print("Unable to create directory")


def get_url_data(pageurl):
    url = pageurl
    response = requests.get(url)
    html_lines = response.iter_lines()
    return html_lines


def process_csv_from_web(csvdata):
    return csvdata


def make_decimal(string_value):
    result = 0
    try:
        result = float(string_value)
        result = round(result, 4)
    except ValueError:
        print("ERROR - string is not a number.")
    return result


if __name__ == "__main__":
    t_start = time.time()
    # csv_from_web = get_url_data("http://dunedinaurora.nz/dnacore04/Ruru_Obs.csv")
    csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    # csv_from_web = process_csv_from_web(csv_from_web)

    cleaned_csv = []
    for line in csv_from_web:
        l = line.decode('utf-8')
        # l = line.strip()
        l = l.split(",")
        data_info = l[1]
        time_info = l[0]
        decimal_data = make_decimal(data_info)
        dp = [time_info, decimal_data]
        cleaned_csv.append(dp)

    # plotter_spectrum_baro.wrapper(cleaned_csv)

    t_end = time.time()
    t_elapsed = (t_end - t_start) / 60
    print(f"Elapsed time: {t_elapsed} minutes.")
