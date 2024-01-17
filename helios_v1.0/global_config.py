import os

folder_source_images = 'source'
folder_output_to_publish = 'publish'
solar_wind_database = 'solarwind.db'

noaa_image_data = {
    'GOES_primary': {
        '171': {
            'instrument': 'suvi',
            'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/',
            'storage_folder': folder_source_images + os.pathsep + 'goes_p_171'
        },
        '195': {
            'instrument': 'suvi',
            'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/',
            'storage_folder': folder_source_images + os.pathsep + 'goes_p_195'
        },
        '284': {
            'instrument': 'suvi',
            'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/',
            'storage_folder': folder_source_images + os.pathsep + 'goes_p_284'
        }
    }
}