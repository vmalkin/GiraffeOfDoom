
# get image list of LASCO files for the last x-hours.
# if time difference between img_x, ing_y < time threshold
#   Convert img_x, img_y to greyscale
#   Convert img_x, img_y to single channel
#   New savefile = img_y name
#   for img_x, img_y:
#       for same pixel location in img_x, img_y:
#           if diff between px_img_x and px_img_y greater than pixel_threshold:
#               new_pixel = median pixel value
#               else new_pixel = old_pixel
#       save new image, img_z