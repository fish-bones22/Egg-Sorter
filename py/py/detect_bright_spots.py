# USAGE
#ppython detect_bright_spots.py --image images/lights_01.png

# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# threshold the image to reveal light regions in the
# blurred image
thresh = cv2.threshold(blurred, 105, 255, cv2.THRESH_BINARY)[1]

# perform a series of erosions and dilations to remove
# any small blobs of noise from the thresholded image
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)

# Get size and radius of image for cropping
height, width, _ = image.shape
radius = int(height/2 if height < width else width/2) + int(abs(height-width)/4)
# create circle mask
circMask = np.zeros((height, width), np.uint8)
cv2.circle(circMask, (int(width/2), int(height/2)), radius, (255, 255, 255), thickness=-1)

thresh = np.invert(thresh)
thresh = cv2.bitwise_and(thresh, thresh, mask=circMask)


# perform a connected component analysis on the thresholded
# image, then initialize a mask to store only the "large"
# components
#labels = measure.label(thresh, neighbors=8, background=0)
#mask = np.zeros(thresh.shape, dtype="uint8")

white = cv2.countNonZero(thresh)

# loop over the unique components
#for label in np.unique(labels):
	# if this is the background label, ignore it
#	if label == 0:
#		continue

	# otherwise, construct the label mask and count the
	# number of pixels 
#	labelMask = np.zeros(thresh.shape, dtype="uint8")
#	labelMask[labels == label] = 255
#	numPixels = cv2.countNonZero(labelMask)

	# if the number of pixels in the component is sufficiently
	# large, then add it to our mask of "large blobs"
#	if numPixels > 300:
#		mask = cv2.add(mask, labelMask)

# find the contours in the mask, then sort them from left to
# right
#cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#	cv2.CHAIN_APPROX_SIMPLE)
#cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#cnts = contours.sort_contours(cnts)[0]

# loop over the contours
#for (i, c) in enumerate(cnts):
	# draw the bright spot on the image
#	(x, y, w, h) = cv2.boundingRect(c)
#	((cX, cY), radius) = cv2.minEnclosingCircle(c)
#	cv2.circle(thresh, (int(cX), int(cY)), int(radius),
#		(0, 0, 255), 3)
#	cv2.putText(thresh, "#{}".format(i + 1), (x, y - 15),
#		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# show the output image

filename = args["image"].split("/")
filename = "mod-"+filename[len(filename)-1]
print(filename, "exported")
print("Dark pixels:", white)
print("Total pixels:", width*height)
cv2.imwrite(filename, thresh)
