# Automatically create a folder based on UTC date and copy all jpegs to it.
import os
import shutil
import datetime
import glob


def get_directory():
    returnvalue = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return returnvalue


if __name__ == "__main__":
    current_directory = get_directory()
    os.makedirs(current_directory, exist_ok=True)

    for data in glob.glob("*.jpg"):
        shutil.move(data, current_directory)
