import os

filesep = os.sep

folder_source_images = 'source'
folder_output_to_publish = 'publish'
solar_wind_database = 'solarwind.db'

noaa_image_data = [
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/',
        folder_source_images + filesep + 'goes_p_171'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/',
        folder_source_images + filesep + 'goes_p_195'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/',
        folder_source_images + filesep + 'goes_p_284'
    ]
]

tm = int(time.time())
ymd_now = int(posix2utc(tm, "%Y%m%d"))
ymd_old1 = ymd_now - 1
ymd_old2 = ymd_old1 - 1
year = posix2utc(tm, "%Y")

# LASCO coronagraph
baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + str(ymd_now) + "/"

# Parse for old epoch files that have been added
baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + str(ymd_old1) + "/"

# Parse for old epoch files that have been added
baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + str(ymd_old2) + "/"

lasco_image_data = []
