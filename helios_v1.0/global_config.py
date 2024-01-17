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
