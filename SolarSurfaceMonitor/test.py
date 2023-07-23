import glob
import requests
import os
import time
import mgr_diffs as diffs
import mgr_gif as make_gif

pathsep = os.sep
suvidata = {
    '171': {
        'store': 'store_b',
        'diffs': 'diffs_b',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/'
    },
    '195': {
        'store': 'store_g',
        'diffs': 'diffs_g',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/'
    },
    '284': {
        'store': 'store_r',
        'diffs': 'diffs_r',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/'
    }
}

diffs.wrapper(suvidata)
