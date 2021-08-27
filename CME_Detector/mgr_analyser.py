# offset values when coronagraph mask support-vane in top-right position
offset_x = -5
offset_y = 10

image_size = 512
imagecentre = image_size / 2
cme_min = 0.4
cme_partial = 0.6
cme_halo = 0.8


def processimages_detrend(listofimages, storage_folder, analysisfolder):
    avg_array = []
    pixel_count = []
    dates = []
    for i in range(0, len(listofimages)):
        p = storage_folder + "//" + listofimages[i]

        try:
            pic = image_load(p)
            pic = greyscale_img(pic)

            # convert image to a single channel
            pic = cv2.split(pic)
            pic = pic[0]

            kernel1 = np.ones((3, 3), np.uint8)
            pic = cv2.erode(pic, kernel1, iterations=1)
            avg_array.append(pic)

            # 100 images is about a day
            if len(avg_array) >= 100:
                # ALWAYS POP
                avg_array.pop(0)
                avg_img = np.mean(avg_array, axis=0)

                pic = np.float32(pic)
                avg_img = np.float32(avg_img)

                detrended_img = cv2.subtract(pic, avg_img)
                ret, detrended_img = cv2.threshold(detrended_img, 3, 255, cv2.THRESH_BINARY)
                final_img = np.uint8(detrended_img)

                # convert the image from polar to rectangular coords in order to more easily
                # map CME occurences and identify halo CMEs
                dst = 220
                ang = 360
                t = []
                for dist in range(dst, 0, -1):
                    for angle in range(0, ang):
                        coords = polar_to_rectangular(angle, dist)
                        t.append(final_img[coords[1], coords[0]])

                # https://www.geeksforgeeks.org/convert-a-numpy-array-to-an-image/
                # array = np.array(t)
                array = np.reshape(np.array(t), (dst, ang))

                mask = create_mask(array, ang, dst, 40, 50)
                masked = cv2.bitwise_and(array, mask)

                # Pixelcounter to create graphic pf CMEs
                # A full halo CME should produce counts in the order of 3600
                px = count_nonzero(masked)
                #  pixelcount as a percentage of the area monitored
                px = float(px) / 3600
                px = round(px, 3)
                t = listofimages[i].split("_")
                posixtime = filehour_converter(t[0], t[1])
                hr = posix2utc(posixtime, "%Y-%m-%d %H:%M")

                # Create a text alert to be exported to DunedinAurora and potentially
                # twitter
                text_alert(px, hr)


                pixel_count.append(px)
                dates.append(hr)

                array = annotate_image(array, ang, dst, hr)

                # cv2.imshow('Example - Show image in window', array)
                # cv2.waitKey(0)  # waits until a key is pressed
                # cv2.destroyAllWindows()  # destroys the window showing image

                f_image = analysisfolder + "//" + "dt_" + listofimages[i]
                # add_stamp("High Contrast CME Detection", final_img, f_image)
                image_save(f_image, array)

                print("dt", i, len(listofimages))
        except:
            print("Error processing image")

    print(len(dates), len(pixel_count))
    pixel_count = median_filter(pixel_count)
    dates.pop(len(dates) - 1)
    dates.pop(0)
    plot(dates, pixel_count, "cme_plot.jpg", 1800, 600)

    dates = dates[-100:]
    pixel_count = pixel_count[-100:]
    plot_mini(dates, pixel_count)


def wrapper():
    pass