from statistics import mean, stdev


def calc_intensity(snr):
    intensity = 0
    try:
        snr = float(snr)
        intensity = 0
        if snr != 0:
            intensity = pow(10, (snr/10))
    except TypeError:
        print("Type error in data in calc_intensity() " + str(snr))
    except ValueError:
        print("Value error in data in calc_intensity() " + str(snr))
    return intensity



snr = "wibble"
print(calc_intensity(snr))