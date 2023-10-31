"""
Este script toma fotos de la cámara y las guarda en la carpeta uncalibrated-images

Cuando se active, guardas la foto con "s" y te sales con <esc>
"""
# Original code from https://github.com/niconielsen32/CameraCalibration
# Adapted by G00Z-G00Z

import cv2
from configuration import UNCALIBRATED_IMAGES_PATH, CAMERA_INDEX
import time


# while cap.isOpened():
#     succes, img = cap.read()

#     k = cv2.waitKey(5)

#     if k == 27:
#         break
#     elif k == ord("s"):  # wait for 's' key to save and exit
#         img_name = f"{num}.png"
#         cv2.imwrite(f"{UNCALIBRATED_IMAGES_PATH.absolute()}/{img_name}", img)
#         print("Image saved: " + img_name)
#         num += 1

#     cv2.imshow("Img", img)


# SET THE COUNTDOWN TIMER
# for simplicity we set it to 3
# We can also take this as input
STEP_INTERVAL = int(2)
TOTAL_NUMER_PHOTOS = 2
timer = STEP_INTERVAL

# Open the camera
cap = cv2.VideoCapture(
    CAMERA_INDEX
)  # The index of the camera to use (usually 0 is for the internal, and 2 is for the external)

num = 0

while True:
    # Read and display each frame
    ret, img = cap.read()
    cv2.imshow("a", img)

    # check for the key pressed
    k = cv2.waitKey(125)

    # set the key for the countdown
    # to begin. Here we set q
    # if key pressed is q

    if num >= TOTAL_NUMER_PHOTOS:
        break

    if k == ord("q"):
        prev = time.time()
        timer = STEP_INTERVAL

        while timer >= 0:
            ret, img = cap.read()

            # Display countdown on each frame
            # specify the font and draw the
            # countdown using puttext
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                img, str(timer + 1), (200, 250), font, 7, (0, 255, 255), 4, cv2.LINE_AA
            )
            cv2.imshow("a", img)
            cv2.waitKey(125)

            # current time
            cur = time.time()

            # Update and keep track of Countdown
            # if time elapsed is one second
            # then decrease the counter
            if cur - prev >= 1:
                prev = cur
                timer = timer - 1

        else:
            ret, img = cap.read()

            img_name = f"{num}.png"
            num += 1

            cv2.imshow("a", img)

            # time for which image displayed
            cv2.waitKey(2000)

            cv2.imwrite(f"{UNCALIBRATED_IMAGES_PATH.absolute()}/{img_name}", img)
            print("Image saved: " + img_name)

            # HERE we can reset the Countdown timer
            # if we want more Capture without closing
            # the camera

    # Press Esc to exit
    elif k == 27:
        break

# close the camera
cap.release()

# close all the opened windows
cv2.destroyAllWindows()
