cme_min = 0.4
cme_partial = 0.6
cme_halo = 0.8

def text_alert(px, hr):
    # %Y-%m-%d %H:%M
    timestring = hr
    hr = hr.split(" ")
    hr = hr[0]
    hr = hr.split("-")
    new_hr = hr[0] + "/" + hr[1] + "/" + hr[2]
    url = "https://stereo-ssc.nascom.nasa.gov/browse/" + new_hr +  "/ahead/cor2_rdiff/512/thumbnail.shtml"
    stereo_url = "<a href=\"" + url + "\" target=\"_blank\">" + "Stereo Science Centre</a>"
    savefile = "cme_alert.php"

    if px >= cme_min:
        msg = "A possible CME has been detected with " + str(int(px * 100)) + "% coverage"
        if px >= cme_partial:
            msg = "Warning: A possible PARTIAL HALO CME has been detected with " + str(int(px * 100)) + "% coverage"
            if px >= cme_halo:
                msg = "ALERT: A possible FULL HALO CME has been detected with " + str(int(px * 100)) + "% coverage"
        msg = msg + "<br>Confirm Earth impact with STEREO A satellite data:"

        msg_alert = "<p>" + timestring + "<br>" + msg +  " " + stereo_url
        with open(savefile, "w") as s:
            s.write(msg_alert)

text_alert(0.5, "2021-08-24 23:34:12")