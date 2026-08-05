import constants as k
import logging
import requests

"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.INFO
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

data_source = "http://www.ruruobservatory.org.nz/vlf_1_graph.csv"
station_id = "Ruru_Obs"
timeformat = '%Y-%m-%d %H:%M:%S'


def do_get_data(datasource):
    """Get data"""
    result = "fail"
    try:
        webdata = requests.get(datasource, timeout=20)
    except Exception:
        logging.error(station_id + " Unable to get data from URL")

    if webdata.status_code == 200:
        # else parse for datetime, data
        webdata = webdata.content.decode('utf-8')
        webdata = webdata.split('\n')

        # the first line is just header data
        webdata.pop(0)
        # # convert datetime to posix values
        # for row in webdata:
        #     print(row)
    elif webdata.status_code == 404:
        print("Error 404!")
        logging.error(station_id + " Unable to get data from URL")
    else:
        logging.error(station_id + " ERROR: Could not get data from URL")
        result = "fail"
    return webdata


if __name__ == "__main__":
    savefile = "/var/www/html/vlf_1_graph.csv"
    # savefile = "vlf_1_graph.csv"
    vlf = do_get_data(data_source)
    if len(vlf) > 0:
        with open(savefile, "w") as v:
            for row in vlf:
                v.write(row + "\n")
        v.close()