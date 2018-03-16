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
    pass
