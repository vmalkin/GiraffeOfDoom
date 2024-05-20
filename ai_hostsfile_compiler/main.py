import requests


def do_get_data(self):
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
        # convert datetime to posix values
        for row in webdata:
            try:
                r = row.split(',')
                # print(row)
                try:
                    posix_dt = self.utc2posix(r[0])
                    value = round(float(r[1]), 3)
                    dp = str(posix_dt) + "," + str(value)
                    self.mag_data.append(dp)
                except Exception:
                    print("WARNING: unable to parse time")
                    logging.warning(station_id + " WARNING: unable to parse a time value: " + str(posix_dt))
            except IndexError:
                logging.warning(station_id + " WARNING: list index out of range")
                result = "fail"
    else:
        logging.error(station_id + " ERROR: Could not get data from URL")
        result = "fail"

    if len(self.mag_data) > 2:
        result = "success"
    # print(self.mag_data)
    return result

if __name__ ==