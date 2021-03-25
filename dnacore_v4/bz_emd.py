import matplotlib.pyplot as plt
import emd
import numpy as np

a = []
with open("Geomag_Bz.csv", "r") as f:
    for line in f:
        line = line.split(",")
        d = line[1].strip()
        try:
            d = float(str(d))
            a.append(d)
        except:
            pass

a.pop(0)
n = np.array(a, dtype='float')

def my_get_next_imf(x, zoom=None, sd_thresh=0.1):

    proto_imf = x.copy()  # Take a copy of the input so we don't overwrite anything
    continue_sift = True  # Define a flag indicating whether we should continue sifting
    niters = 0            # An iteration counter

    if zoom is None:
        zoom = (0, x.shape[0])

    # Main loop - we don't know how many iterations we'll need so we use a ``while`` loop
    while continue_sift:
        niters += 1  # Increment the counter

        # Compute upper and lower envelopes
        upper_env = emd.utils.interp_envelope(proto_imf, mode='upper')
        lower_env = emd.utils.interp_envelope(proto_imf, mode='lower')

        # Compute average envelope
        avg_env = (upper_env+lower_env) / 2

        # Add a summary subplot
        plt.subplot(5, 1, niters)
        plt.plot(proto_imf[zoom[0]:zoom[1]], 'k')
        # plt.plot(upper_env[zoom[0]:zoom[1]])
        # plt.plot(lower_env[zoom[0]:zoom[1]])
        # plt.plot(avg_env[zoom[0]:zoom[1]])


        # Should we stop sifting?
        stop, val = emd.sift.sd_stop(proto_imf-avg_env, proto_imf, sd=sd_thresh)

        # Remove envelope from proto IMF
        proto_imf = proto_imf - avg_env

        # and finally, stop if we're stopping
        if stop:
            continue_sift = False


    # Return extracted IMF
    plt.show()
    return proto_imf

imf1 = my_get_next_imf(n)