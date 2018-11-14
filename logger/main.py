# Automatically create a folder based on UTC date and copy all jpegs to it.

from shutil import copy
import datetime

def get_directory():
    returnvalue = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return returnvalue


if __name__ == "__main__":
    current_directory = get_directory()
    copy("*.jpg", current_directory)