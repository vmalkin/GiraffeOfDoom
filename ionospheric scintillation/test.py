from statistics import mean, stdev

intensity = [0.2, 0.6, 0.5, 0.45, 0.1]

def get_s4():
    # http://mtc-m21b.sid.inpe.br/col/sid.inpe.br/mtc-m21b/2017/08.25.17.52/doc/poster_ionik%20%5BSomente%20leitura%5D.pdf
    returnvalue = 0
    if len(intensity) > 2:
        avg_intensity = mean(intensity)
        sigma = stdev(intensity)
        if avg_intensity > 0:
            returnvalue = round(((sigma / avg_intensity) * 100), 5)
    return returnvalue

print(get_s4())