import cv2 as cv
from testFiles import pysift
import logging
logger = logging.getLogger(__name__)

MIN_MATCH_COUNT = 10

img1 = cv.imread('../images/capturedCard.png', 0)           # queryImage

# Compute SIFT keypoints and descriptors
keypoints, desciptors = pysift.computeKeypointsAndDescriptors(img1)
im2 = 0
im2 = cv.drawKeypoints(img1, keypoints, im2, (0, 255, 9))
cv.imshow("Image", im2)
cv.waitKey()