import os
import datetime

def getdate():
    # a formatted Datetime object for recording inside the logfile
    logdate = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return logdate

def makefolder(foldername):
    print("Making a folder " + foldername)

def movefiles():
    pass

if __name__ == "__main__":
    nowdate = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # if utcnow() == current folder
    if os.path.exists(nowdate):
        # move files into folder (copy/delete)
    else:
        # else make new folder, create thumbnails and HTML to view images in old folder
    pass
