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

goes_dict = {
    'primary': {
        'false_colour': folder_source_images + filesep + 'sv_false_x',
        'false_diffs': folder_source_images + filesep + 'sv_diffs_x',
        'wavelengths': {
            '171': {
                'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/',
                'store': folder_source_images + filesep + 'goes_x_171',
                'diffs': folder_source_images + filesep + 'goes_x_df_171'
            },
            '195': {
                'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/',
                'store': folder_source_images + filesep + 'goes_x_195',
                'diffs': folder_source_images + filesep + 'goes_x_df_195'
            },
            '284': {
                'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/',
                'store': folder_source_images + filesep + 'goes_x_284',
                'diffs': folder_source_images + filesep + 'goes_x_df_284'
            }
        }
    },
    'secondary': {
            'false_colour': folder_source_images + filesep + 'sv_false_y',
            'false_diffs': folder_source_images + filesep + 'sv_diffs_y',
            'wavelengths': {
                '171': {
                    'url': 'https://services.swpc.noaa.gov/images/animations/suvi/secondary/171/',
                    'store': folder_source_images + filesep + 'goes_y_171',
                    'diffs': folder_source_images + filesep + 'goes_y_df_171'
                },
                '195': {
                    'url': 'https://services.swpc.noaa.gov/images/animations/suvi/secondary/195/',
                    'store': folder_source_images + filesep + 'goes_y_195',
                    'diffs': folder_source_images + filesep + 'goes_y_df_195'
                },
                '284': {
                    'url': 'https://services.swpc.noaa.gov/images/animations/suvi/secondary/284/',
                    'store': folder_source_images + filesep + 'goes_y_284',
                    'diffs': folder_source_images + filesep + 'goes_y_df_284'
                }
            }
        }
    }

