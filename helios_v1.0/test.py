from global_config import goes_dict

# for sat in goes_dict:
#     print(goes_dict[sat]['false_colour'])
#     print(goes_dict[sat]['false_diffs'])

for sat in goes_dict:
    print(sat)
    for key in goes_dict[sat]['wavelengths']:
        # print(goes_dict[sat]['wavelengths'][key]['url'])
        print(key)
        print(goes_dict[sat]['wavelengths'][key]['diffs'])

