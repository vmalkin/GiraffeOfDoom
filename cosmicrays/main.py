import time
import cv2
import numpy as np
import datetime

averaging_iterations = 100
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


def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    return greyimg


if __name__ == '__main__':
    n = posix2utc(time.time(), '%Y_%m_%d_%H_%M')
    filename = "bkp_" + n + ".jpg"

    averaging_array = []
    display_flag = True
    camera = cv2.VideoCapture(current_camera)
    camera_setup_c270(camera)

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
            # convert anything equal of over to 255
            testing_img = np.where(testing_img <= 0, 0,testing_img)
            # testing_img = np.where(testing_img > 0, 255, testing_img)
            # cv2.imshow('Cumulative', testing_img)

            pixel_count = cv2.countNonZero(testing_img)
            if pixel_count > 0:
                if pixel_count < blob_size:
                    print("Noise? Count: ", pixel_count)
            if pixel_count >= blob_size:
                t = posix2utc(time.time(), '%Y-%m-%d %H:%M')
                print(t + " Blob detected! " + str(pixel_count) + " pixels. Hot: " + str(np.max(testing_img)))

                n = posix2utc(time.time(), '%Y-%m-%d')
                filename = "CRays_" + n + ".jpg"
                show_img = show_img + testing_img
                image_save(filename, show_img)
                cv2.imshow('Cumulative', show_img)

        c = cv2.waitKey(1)
        if c == 27:
            break

    camera.release()
    cv2.destroyAllWindows()