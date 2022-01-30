import time
import cv2
import numpy as np
import datetime
import sqlite3
import os
import mgr_plot_flux
import mgr_plot_hits
from threading import Thread

class ThreadPlotter(Thread):
    def __init__(self):
        Thread.__init__(self, name="ThreadPlotter")
    def run(self):
        time.sleep(10)
        while True:
            # print("Beginning plot...")
            data = database_get_data(24*7)
            try:
                mgr_plot_flux.wrapper(data)
            except:
                print("Failed to print cumulative totals")

            try:
                mgr_plot_hits.wrapper(data)
            except:
                print("Failed to print hits")
            # print("Plot finished")
            time.sleep(1800)

database = "events.db"
averaging_iterations = 50
highpass_threshold = 3
current_camera = 2
blob_size = 3

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
    print("File saved: " , file_name)


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

    # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
    cam.set(cv2.CAP_PROP_EXPOSURE, exposure)
    
    print("set//get gain: ", gain, cam.get(cv2.CAP_PROP_GAIN))
    print("set//get brightness: ", brightness, cam.get(cv2.CAP_PROP_BRIGHTNESS))
    print("set//get saturation: ", saturation, cam.get(cv2.CAP_PROP_SATURATION))
    print("set//get contrast: ", contrast, cam.get(cv2.CAP_PROP_CONTRAST))
    print("set//get sharpness: ", sharpness, cam.get(cv2.CAP_PROP_SHARPNESS))
    print("set//get height: ", height, cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("set//get width: ", width, cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("set//get exposure: ", exposure, cam.get(cv2.CAP_PROP_EXPOSURE))



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
    cv2.imshow('TEST',img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()

def report_image_params(image):
    max_pixel_value = "{:.3f}".format((round(np.max(image), 4)))
    avg_pixel_value = "{:.3f}".format(round(np.average(image), 4))
    min_pixel_value = "{:.3f}".format(round(np.min(image), 4))
    print("max_p, avg_p, min_p ", max_pixel_value, avg_pixel_value, min_pixel_value)
    
if __name__ == '__main__':
    # Check that we have folders and database in place
    if os.path.isfile(database) is False:
        print("No database file, initialising")
        database_create()

    # n = posix2utc(time.time(), '%Y_%m_%d_%H_%M')
    # filename = "bkp_" + n + ".jpg"
    n_old = posix2utc(time.time(), '%Y-%m-%d')

    averaging_array = []
    avg_pixels = None
    display_flag = True
    camera = cv2.VideoCapture(current_camera)
    camera_setup_c270(camera)

    plotter = ThreadPlotter()
    try:
        plotter.start()
        print("Starting plotter thread...")
    except:
        print("Unable to start plotter thread in MAIN.PY!!")

    print("Exposure: ", camera.get(cv2.CAP_PROP_EXPOSURE))
    sh_x = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    sh_y = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print("Frame size: ", sh_x, sh_y)

    # Create a highpass filter
    highpass = np.full((sh_y, sh_x), highpass_threshold)

    # initial old image to calculate the rate of change in the image
    detrended_old = np.full((sh_y, sh_x), 0)

    # Image to show accumulating stikes
    cumulative_image = np.full((sh_y, sh_x), 0)

    while True:
        ret, image = camera.read()
        img_g = greyscale_img(image)

        # Create an array of pictures with which to create an average
        averaging_array.append(img_g)

        if len(averaging_array) >= averaging_iterations:
            # ALWAYS POP
            averaging_array.pop(0)
            
            avg_img = np.mean(averaging_array, axis=0)
            max_avg_pixels = int(np.max(avg_img))

            if display_flag == True:
                print("Average Image parameters")
                report_image_params(avg_img)
                display_flag = False
                
            # the detrended image is the current image minus the average image. This should remove
            # persistent noise, and hot zones from the current image.
            detrended_new = img_g - avg_img

            # Essentially an image with the rate of change. only sudden changes in pixel brightness will
            # show. Cosmic ray hits, sudden noise, etc. Dont forget to make the new image, the new old image
            # for the next iteration... :-)
            testing_img = detrended_new - detrended_old
            detrended_old = detrended_new

            # FInally, there is still a residuum of noise, that is due to sudden hot pixels, especially in the
            # quadrant of the CMOS near the camera electronics.
            testing_img = testing_img - highpass
            report_image_params(testing_img)

            # # We now have a flat image, with no noise. Hopefully cosmic ray hits will show in the sensor images
            # # Clip any value less than zero, to zero.
            # # convert anything over zero to 255
            # testing_img = np.where(testing_img <= 0, 0,testing_img)
            # testing_img = np.where(testing_img > 0, 255, testing_img)
            #
            # pixel_count = cv2.countNonZero(testing_img)
            # if pixel_count >= blob_size:
            #     tt = int(time.time())
            #     t = posix2utc(tt, '%Y-%m-%d %H:%M:%S')
            #     print(t + " Blob detected! " + str(pixel_count) + " pixels. Max average: " + str(max_avg_pixels))
            #
            #     # add to database, get data for time period.
            #     database_add_data(tt, pixel_count)
            #     current_data = database_get_data(24)
            #
            #     n = posix2utc(tt, '%Y-%m-%d')
            #     if n_old == n:
            #         filename = "CRays_" + n + ".png"
            #         # filename = posix2utc(tt, '%H-%M-%S') + ".jpg"
            #         cumulative_image = cumulative_image + testing_img
            #         show_cam_image(cumulative_image)
            #         image_save(filename, cumulative_image)
            #     else:
            #         n_old = n
            #         cumulative_image = np.full((sh_y, sh_x), 0)

    camera.release()
    cv2.destroyAllWindows()
