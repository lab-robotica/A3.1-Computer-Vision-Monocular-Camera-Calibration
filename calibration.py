# Orginal code from https://github.com/niconielsen32/CameraCalibration
# Adapted by G00Z-G00Z

import numpy as np
import cv2 as cv
import glob
import pickle
from pathlib import Path
from configuration import (
    CHESSBOARD_SIZE,
    IMAGE_EXTENSIONS,
    UNCALIBRATED_IMAGES_PATH,
    CALIBRATED_IMAGE_PATH,
)

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################


def main():
    # Tests data

    if not UNCALIBRATED_IMAGES_PATH.exists():
        raise Exception(f"Path {UNCALIBRATED_IMAGES_PATH} does not exist")

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0 : CHESSBOARD_SIZE[0], 0 : CHESSBOARD_SIZE[1]].T.reshape(
        -1, 2
    )

    size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(f"{UNCALIBRATED_IMAGES_PATH.absolute()}/*.{IMAGE_EXTENSIONS}")

    gray: MatLike | None = None
    for image in images:
        img = cv.imread(image)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

        # If found, add object points, image points (after refining them)
        if not ret:
            print(f"Image {image} does not contain a chessboard")
            continue

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, CHESSBOARD_SIZE, corners2, ret)
        cv.imshow("img", img)
        # cv.waitKey(0)

    cv.destroyAllWindows()

    ############## CALIBRATION #######################################################

    if gray is None:
        raise RuntimeError("No images found")
    ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    # Save the camera calibration result for later use (we won't worry about rvecs / tvecs)

    pickle.dump(
        (cameraMatrix, dist),
        open(f"{CALIBRATED_IMAGE_PATH.absolute()}/calibration.pkl", "wb"),
    )
    pickle.dump(
        cameraMatrix, open(f"{CALIBRATED_IMAGE_PATH.absolute()}/cameraMatrix.pkl", "wb")
    )
    pickle.dump(dist, open(f"{CALIBRATED_IMAGE_PATH.absolute()}/dist.pkl", "wb"))

    ############## UNDISTORTION #####################################################

    # Calibrate and save all images in the calibrated image path

    for image in images:
        img = cv.imread(image)
        h, w = img.shape[:2]
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
            cameraMatrix, dist, (w, h), 1, (w, h)
        )

        # Undistort
        dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]
        cv.imwrite(f"{CALIBRATED_IMAGE_PATH.absolute()}/{Path(image).name}", dst)

    cv.destroyAllWindows()

    # Reprojection Error
    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist
        )
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error

    # Save the error in a file

    with open(f"{CALIBRATED_IMAGE_PATH.absolute()}/reprojection_error.txt", "w") as f:
        f.write("{}".format(mean_error / len(objpoints)))
        print("total error: {}".format(mean_error / len(objpoints)))


if __name__ == "__main__":
    main()
