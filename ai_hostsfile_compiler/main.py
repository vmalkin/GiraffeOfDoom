import requests
import logging

"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.INFO
logging.basicConfig(filename="error.log", format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

datasource = 'https://github.com/mahseema/awesome-ai-tools'
def do_get_data(datasource):
    """Get data"""
    result = []
    try:
        webdata = requests.get(datasource, timeout=20)
    except Exception:
        logging.error("Unable to get data from URL: ", datasource)

    if webdata.status_code == 200:
        # else parse for datetime, data
        webdata = webdata.content.decode('utf-8')
        webdata = webdata.split('\n')

        for row in webdata:
            if row[:4] == '<li>':
                r = row.split('"')
                if r[1][:4] == 'http':
                    result.append(r[1])

    return result

if __name__ == "__main__":
    ai_list = do_get_data(datasource)