# use "pip install opencv-python" if cv2 is not found
import cv2
import glob

# Get a list of PNG images on the "test_images" folder
images = glob.glob("combined/*.png")
# You can also use the following two lines to get PNG files in a folder.
# import os
# images = [os.path.join("../test_images", file) for file in os.listdir("../test_images") if file.endswith(".png")]
# Sort images by name. Optional step.
images = sorted(images)
# Define codec and create a VideoWriter object
# cv2.VideoWriter_fourcc(*"mp4v") or cv2.VideoWriter_fourcc("m", "p", "4", "v")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(
    filename="output.mp4", fourcc=fourcc, fps=30.0, frameSize=(430, 430)
)

# Read each image and write it to the video
for image in images:
    # read the image using OpenCV
    frame = cv2.imread(image)
    # Optional step to resize the input image to the dimension stated in the
    # VideoWriter object above
    frame = cv2.resize(frame, dsize=(430, 430))
    video.write(frame)

# Exit the video writer
video.release()