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
averaging_iterations = 20
highpass_threshold = 5
current_camera = 2
blob_size = 4


def image_save(file_name, image_object):
    img = np.array(image_object, np.uint8)
    cv2.imwrite(file_name, img)


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def camera_setup_c270(cam):
    cam.set(cv2.CAP_PROP_GAIN, 255)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 120)
    cam.set(cv2.CAP_PROP_SATURATION, 100)
    cam.set(cv2.CAP_PROP_CONTRAST, 32)
    cam.set(cv2.CAP_PROP_SHARPNESS, 255)
    cam.set(cv2.CAP_PROP_EXPOSURE, 120)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)


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



if __name__ == '__main__':
    # Check that we have folders and database in place
    if os.path.isfile(database) is False:
        print("No database file, initialising")
        database_create()

    # n = posix2utc(time.time(), '%Y_%m_%d_%H_%M')
    # filename = "bkp_" + n + ".jpg"
    n_old = posix2utc(time.time(), '%Y-%m-%d')

    averaging_array = []
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
    print("Frame size: ", sh_x, sh_y)

    # Create a highpass filter
    highpass = np.full((sh_y, sh_x), highpass_threshold)

    # initial old image to calculate the rate of change in the image
    detrended_old = np.full((sh_y, sh_x), 0)

    # Image to show accumulating stikes
    show_img = np.full((sh_y, sh_x), 0)

    while True:
        ret, image = camera.read()
        img_g = greyscale_img(image)

        # Create an array of pictures with which to create an average
        averaging_array.append(img_g)

        if len(averaging_array) >= averaging_iterations:
            # ALWAYS POP
            averaging_array.pop(0)
            avg_img = np.mean(averaging_array, axis=0)

            if display_flag == True:
                print("Max avg pixel value. Make threshold above this: ", str(int(np.max(avg_img))))
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

            # We now have a flat image, with no noise. Hopefully cosmic ray hits will show in the sensor images
            # Clip any value less than zero, to zero.
            # convert anything over zero to 255
            testing_img = np.where(testing_img <= 0, 0,testing_img)
            testing_img = np.where(testing_img > 0, 255, testing_img)

            pixel_count = cv2.countNonZero(testing_img)
            if pixel_count > 0:
                if pixel_count < blob_size:
                    print("Noise? " + str(pixel_count) + " pixels.")
            if pixel_count >= blob_size:
                tt = int(time.time())
                t = posix2utc(tt, '%Y-%m-%d %H:%M')
                print(t + " Blob detected! " + str(pixel_count) + " pixels.")

                # add to database, get data for time period.
                database_add_data(tt, pixel_count)
                current_data = database_get_data(24)

                n = posix2utc(tt, '%Y-%m-%d')
                if n_old == n:
                    filename = "CRays_" + n + ".png"
                    show_img = show_img + testing_img
                    image_save(filename, show_img)
                else:
                    n_old = n
                    show_img = np.full((sh_y, sh_x), 0)

    camera.release()
    cv2.destroyAllWindows()