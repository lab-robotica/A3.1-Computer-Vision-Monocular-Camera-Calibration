"""
Configuration file for the camera calibration script
Change the variables to suit your needs

The test data variables will be used to test the script
"""
from pathlib import Path
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

## Test data
MODEL_NAME = os.getenv("MODEL_NAME", "")
CHESSBOARD_SIZE_EVEN = os.getenv("CHESSBOARD_SIZE_EVEN", "")
CHESSBOARD_SIZE_ODD = os.getenv("CHESSBOARD_SIZE_ODD", "")
IMAGE_EXTENSIONS = os.getenv("IMAGE_EXTENSIONS", "")
CAMERA_INDEX = os.getenv("CAMERA_INDEX", "")

if not all(
    [
        MODEL_NAME,
        CHESSBOARD_SIZE_EVEN,
        CHESSBOARD_SIZE_ODD,
        IMAGE_EXTENSIONS,
    ]
):
    raise Exception(
        "Please check your environment variables! It appears that some are missing"
    )

CHESSBOARD_SIZE = (int(CHESSBOARD_SIZE_EVEN), int(CHESSBOARD_SIZE_ODD))
CAMERA_INDEX = int(CAMERA_INDEX)


# Tests for correct data

# Check image path
UNCALIBRATED_IMAGES_PATH = Path(".") / "uncalibrated-images" / MODEL_NAME
CALIBRATED_IMAGE_PATH = Path(".") / "calibrated-images" / MODEL_NAME
CALIBRATED_IMAGE_PATH.mkdir(parents=True, exist_ok=True)

if not UNCALIBRATED_IMAGES_PATH.exists():
    UNCALIBRATED_IMAGES_PATH.mkdir(parents=True, exist_ok=True)

# Check even x odd chessboard size
if CHESSBOARD_SIZE[0] % 2 != 0:
    raise Exception("CHESSBOARD_SIZE[0] must be even")
if CHESSBOARD_SIZE[1] % 2 == 0:
    raise Exception("CHESSBOARD_SIZE[1] must be odd")
