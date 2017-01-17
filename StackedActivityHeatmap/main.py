import Station
import os
from decimal import Decimal, getcontext
import time

getcontext().prec = 5


# #########################################
# M a i n   p r o g r a m   h e r e
# #########################################
while True:
    # create the magnetometer stations for this run

    Dalmore = Station.Station("Dalmore01", "Dalmore01.1minbins.csv")
    Corstorphine = Station.Station("Corstorphine01", "Corstorphine01.1minbins.csv")

    print(Dalmore.stationdata)
    print(Dalmore.begintime)
    print(Corstorphine.stationdata)

    time.sleep(600)