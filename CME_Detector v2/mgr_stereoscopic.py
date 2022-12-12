import os

def wrapper(directory, interpupilliary_distance_mm):
    # create video of the last 24 hours from the enhanced folder.
    # approx no of images in a day is 30 for the enhanced folder!
    imagelist_enhanced = os.listdir(directory)
    imagelist_enhanced.sort()
    if len(imagelist_enhanced) > 40:
        imagelist_enhanced = imagelist_enhanced[-40:]
    imagelist_enhanced.sort()
    print(imagelist_enhanced)


folder = "enhanced_512"
wrapper(folder, 70)