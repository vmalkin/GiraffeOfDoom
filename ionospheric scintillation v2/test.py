# import re
from statistics import mean, stdev, median

class TestClass:
    def __init__(self):
        self.snr = [5,5,5,6,5,4,5,5]

    def calc_intensity(self, snr_array):
        returnarray = []
        for item in snr_array:
            intensity = pow(10, (item / 10))
            returnarray.append(intensity)
        return returnarray


    def get_s4(self):
        # http://mtc-m21b.sid.inpe.br/col/sid.inpe.br/mtc-m21b/2017/08.25.17.52/doc/poster_ionik%20%5BSomente%20leitura%5D.pdf
        if len(self.snr) > 2:
            intensity = self.calc_intensity(self.snr)
            avg_intensity = mean(intensity)
            sigma = stdev(intensity)
            returnvalue = round(((sigma / avg_intensity) * 100), 5)
        else:
            returnvalue = 0
        return returnvalue