import os
filesep = os.sep

copyright = 'DunedinAurora.NZ, (c) 2024.'
folder_source_images = 'source'
folder_output_to_publish = 'publish'
solar_wind_database = 'solarwind.db'

# dataitem [url, save files, difference images, name]
noaa_image_data = [
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/',
        folder_source_images + filesep + 'store_goes_p_171',
        folder_source_images + filesep + 'diffs_goes_p_171',
        '171A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/',
        folder_source_images + filesep + 'store_goes_p_195',
        folder_source_images + filesep + 'diffs_goes_p_195',
        '195A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/',
        folder_source_images + filesep + 'store_goes_p_284',
        folder_source_images + filesep + 'diffs_goes_p_284',
        '284A'
    ]
]

