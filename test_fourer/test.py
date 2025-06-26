from scipy.fft import rfft, rfftfreq
import requests

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


csv_data = []
csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
csv_from_web = process_csv_from_web(csv_from_web)

for line in csv_from_web:
    l = line.decode('utf-8')
    # l = line.strip()
    l = l.split(",")
    string_data = l[1]

    # # this is weird, why do we need to add 100 here?
    decimal_data = make_decimal(string_data)
    # np.append(csv_data, decimal_data)
    csv_data.append(decimal_data)
