import time
import cv2
import numpy as np
import datetime
import sqlite3
import os
import mgr_daily_count
import mgr_plot_hits
import mgr_emd
from threading import Thread


class ThreadPlotter(Thread):
    def __init__(self):
        Thread.__init__(self, name="ThreadPlotter")

    def run(self):
        time.sleep(10)
        while True:
            print("*** Beginning plots...")
            data = database_get_data(24*7)
            try:
                mgr_daily_count.wrapper()
            except:
                print("Failed to plot cumulative totals")

            try:
                mgr_plot_hits.wrapper(data)
            except:
                print("Failed to plot hits")

            try:
                emd_data = get_emd_data()
                datetimes = emd_data[0]
                datavalues = emd_data[1]
                mgr_emd.wrapper(datavalues, datetimes, "test_emd.jpg")
            except:
                print("Failed to plot Empirical Mode Decomposition")

            print("*** Plots finished")
            time.sleep(3600)


database = "events.db"
averaging_iterations = 100
highpass_threshold = 3
current_camera = 2
blob_size = 4

# milli sec
exposure_win = -1
exposure_lin = int((2 ** exposure_win) * 1000)

print("Exposure, Windows: ", exposure_win)
print("Exposure, Linux mSec: ", exposure_lin)
print("Database file is: ", database)
print("Frames for averaging: ", averaging_iterations)
print("Highpass filter threshold manually set to: ", highpass_threshold)
print("Camera ID: ", current_camera)
print("Blob size to count as muon hit: ", blob_size)
print("\n")


def image_save(file_name, image_object):
    img = np.array(image_object, np.uint8)
    cv2.imwrite(file_name, img)
    print("File saved: ", file_name)


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def camera_setup_c270(cam):
    gain = 255
    brightness = 120
    saturation = 100
    contrast = 32
    sharpness = 255
    height = 480
    width = 640
    exposure = exposure_lin
    # exposure = exposure_win

    cam.set(cv2.CAP_PROP_GAIN, gain)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    cam.set(cv2.CAP_PROP_SATURATION, saturation)
    cam.set(cv2.CAP_PROP_CONTRAST, contrast)
    cam.set(cv2.CAP_PROP_SHARPNESS, sharpness)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # Disable auto exposure
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

    # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
    cam.set(cv2.CAP_PROP_EXPOSURE, exposure)
    
    print("set / get gain: ", gain, cam.get(cv2.CAP_PROP_GAIN))
    print("set / get brightness: ", brightness, cam.get(cv2.CAP_PROP_BRIGHTNESS))
    print("set / get saturation: ", saturation, cam.get(cv2.CAP_PROP_SATURATION))
    print("set / get contrast: ", contrast, cam.get(cv2.CAP_PROP_CONTRAST))
    print("set / get sharpness: ", sharpness, cam.get(cv2.CAP_PROP_SHARPNESS))
    print("set / get height: ", height, cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("set / get width: ", width, cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("set / get exposure: ", exposure, cam.get(cv2.CAP_PROP_EXPOSURE))
    print("set / get frames per second: ", cam.get(cv2.CAP_PROP_FPS))
    print("set / get autoexposure: ", cam.get(cv2.CAP_PROP_AUTO_EXPOSURE))

def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    return greyimg


def database_create():
    print("No database, creating file")
    gpsdb = sqlite3.connect(database)
    db = gpsdb.cursor()
    db.execute('drop table if exists data;')
    db.execute('create table data ('
               'posixtime text,'
               'datavalue integer'
               ');')
    gpsdb.commit()
    db.close()


def database_add_data(timestamp, datavalue):
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute("insert into data (posixtime, datavalue) values (?,?);", [timestamp, datavalue])
    db.commit()
    db.close()


def database_get_data(hours_duration):
    duration = hours_duration * 3600
    tempdata = []
    starttime = int(time.time()) - duration
    db = sqlite3.connect(database)
    cursor = db.cursor()
    result = cursor.execute("select posixtime from data where posixtime > ? order by posixtime asc", [starttime])
    for line in result:
        d = line[0]
        tempdata.append(d)
    db.close()
    return tempdata


def show_cam_image(img):
    cv2.imshow('TEST', img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()


def report_image_params(image):
    max_pixel_value = round(np.max(image), 4)
    min_pixel_value = round(np.min(image), 4)
    avg_pixel_value = round(np.average(image), 4)
    r = [max_pixel_value, avg_pixel_value, min_pixel_value]
    return r

def create_highpass(x, y, value):
    # Create a highpass filter
    highpass = np.full((y, x), value)
    print("Highpass filter created. Value is: ", value)
    return highpass


def check_pixel_coords(pixel_coords, pixel_count):
    # To test that a set of pixel cordinates is a cosmic ray hit
    result = "noise"
    xs = []
    ys = []

    # Determine the spread of the coordinates in the X and Y axis. Create the X and Y lists
    for item in pixel_coords:
        xs.append(item[0][0])
        ys.append(item[0][1])

    xd = max(xs) - min(xs)
    yd = max(ys) - min(ys)

    # xd and yd are the sides of a bounding box for the blob of pixels. If either of these
    # values is a zero, then we have a line of pixels, which seems to be what sensor noise
    # looks like. The other test is for scatter - if a size of the box is bigger than the
    # count of pixels, then we have a spray of pixels ie, they are not contiguous, therefore
    # are not a cosmic ray hit. Otherwise we have a genuine blob!
    if xd > 0:
        if yd > 0:
            # if xd <= pixel_count:
            #     if yd <= pixel_count:
            result = "blob"
    print(xd, yd, pixel_count, result)
    return result

def get_emd_data():
    data = database_get_data(24 * 365)
    # data = [10,20,30,40]
    data_counts = []
    data_times = []
    tmp = []
    for i in range(0, len(data) - 1):
        if posix2utc(data[i + 1], "%d") == posix2utc(data[i], "%d"):
            # print("Match", i, len(data))
            tmp.append(1)

        if posix2utc(data[i + 1], "%d") != posix2utc(data[i], "%d"):
            # print("Not Match", i, len(data))
            tmp.append(1)
            tt = posix2utc(data[i], "%Y-%m-%d")
            dd = sum(tmp)
            data_counts.append(dd)
            data_times.append(tt)
            tmp = []

        if i == len(data) - 2:
            # print("End", i, len(data))
            tmp.append(1)
            tt = posix2utc(data[i], "%Y-%m-%d")
            dd = sum(tmp)
            data_counts.append(dd)
            data_times.append(tt)

    returnvalue = []
    returnvalue.append(data_times)
    returnvalue.append(data_counts)
    return returnvalue



if __name__ == '__main__':
    # Check that we have folders and database in place
    if os.path.isfile(database) is False:
        print("No database file, initialising")
        database_create()

    n_old = posix2utc(time.time(), '%Y-%m-%d')

    averaging_array = []
    avg_pixels = None
    display_flag = True

    camera = cv2.VideoCapture(current_camera)
    camera_setup_c270(camera)

    plotter = ThreadPlotter()
    try:
        plotter.start()
        print("\nStarting plotter thread...")
    except:
        print("Unable to start plotter thread in MAIN.PY!!")

    sh_x = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    sh_y = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Image to show accumulating stikes
    cumulative_image = np.full((sh_y, sh_x), 0)

    while True:
        # Reads the latest image from the camera
        ret, image = camera.read()
        img_g = greyscale_img(image)

        # Create an array of pictures with which to create an average
        averaging_array.append(img_g)

        if len(averaging_array) >= averaging_iterations:
            # ALWAYS POP
            averaging_array.pop(0)
            avg_img = np.mean(averaging_array, axis=0)
            max_avg_pixels = int(np.max(avg_img))

            # Some initialisation stuff, including experimental automatic setting of highpass
            # filter
            if display_flag == True:
                print("\nAverage Image parameters")
                report_image_params(avg_img)
                print("\nCreating dynamic highpass filter...")
                highpassfilter = create_highpass(sh_x, sh_y, max_avg_pixels)
                display_flag = False

            # The image to test is made up of the original image, minus the average minus the highpass
            testing_img = img_g - avg_img - highpassfilter

            # Clip image to with 0 - 255
            testing_img = np.where(testing_img <= 0, 0,testing_img)
            testing_img = np.where(testing_img > 0, 254, testing_img)

            # Count any white pixels - potential cosmic ray hits
            pixel_count = cv2.countNonZero(testing_img)

            tt = int(time.time())
            t = posix2utc(tt, '%Y-%m-%d %H:%M:%S')

            # Report as noise hits that dont meet the size criteria
            if pixel_count != 0 and pixel_count < blob_size:
                print(t + " Noise! " + str(pixel_count) + " pixels. ", report_image_params(testing_img))

            # if a hit is over the size for a blob of pixels, get the coordinates
            #  of the blobs pixels and check. If it's genuine then treat as a
            # cosmic ray hit
            if pixel_count >= blob_size:
                pixel_coords = np.array(cv2.findNonZero(testing_img))
                print(t + " Blob! " + str(pixel_count) + " pixels. ", report_image_params(testing_img))

                blobcheck = check_pixel_coords(pixel_coords, pixel_count)
                if blobcheck == "blob":
                    # add to database, get data for time period.
                    database_add_data(tt, pixel_count)
                    current_data = database_get_data(24)

                    n = posix2utc(tt, '%Y-%m-%d')
                    if n_old == n:
                        filename = "CRays_" + n + ".png"
                        cumulative_image = cumulative_image + testing_img
                        image_save(filename, cumulative_image)
                    else:
                        n_old = n
                        cumulative_image = np.full((sh_y, sh_x), 0)

    # camera.release()
    # cv2.destroyAllWindows()
