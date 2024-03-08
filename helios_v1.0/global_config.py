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
        folder_source_images + filesep + 'store_goes_x_171',
        folder_source_images + filesep + 'diffs_goes_x_171',
        '171A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/',
        folder_source_images + filesep + 'store_goes_x_195',
        folder_source_images + filesep + 'diffs_goes_x_195',
        '195A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/',
        folder_source_images + filesep + 'store_goes_x_284',
        folder_source_images + filesep + 'diffs_goes_x_284',
        '284A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/secondary/171/',
        folder_source_images + filesep + 'store_goes_y_171',
        folder_source_images + filesep + 'diffs_goes_y_171',
        '171A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/secondary/195/',
        folder_source_images + filesep + 'store_goes_y_195',
        folder_source_images + filesep + 'diffs_goes_y_195',
        '195A'
    ],
    [
        'https://services.swpc.noaa.gov/images/animations/suvi/secondary/284/',
        folder_source_images + filesep + 'store_goes_y_284',
        folder_source_images + filesep + 'diffs_goes_y_284',
        '284A'
    ]
]

