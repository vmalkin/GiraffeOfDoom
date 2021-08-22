def text_alert(px, hr):
    # %Y-%m-%d %H:%M
    timestring = hr
    hr = hr.split(" ")
    hr = hr[0]
    hr = hr.split("-")
    new_hr = hr[0] + "/" + hr[1] + "/" + hr[2]
    url = "https://stereo-ssc.nascom.nasa.gov/browse/" + new_hr +  "/ahead/cor2_rdiff/512/thumbnail.shtml"
    stereo_url = "<br><a href=\"" + url + "\" target=\"_blank\">" + url + "</a>"
    savefile = "cme_alert.php"

    if px >= 0.4:
        msg = "A possible CME has been detected with " + str(int(px * 100)) + "% coverage"
        if px >= 0.6:
            msg = "Warning: A possible PARTIAL HALO CME has been detected with " + str(int(px * 100)) + "% coverage"
            if px >= 0.8:
                msg = "ALERT: A possible FULL HALO CME has been detected with " + str(int(px * 100)) + "% coverage"

        msg = msg + "<br>Confirm with STEREO A satellite data here:"
        msg_alert = "<p>" + timestring + ": " + msg + "\n" + stereo_url + "\n\n"
        with open(savefile, "a") as s:
            s.write(msg_alert)

text_alert(0.47, "2021-08-21 10:30")