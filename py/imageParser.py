from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

class IamgeParser:

    image = ""
    resultingImage = ""
    thresholdValue = 0
    width = 0
    height = 0

    def parseImage(self, fileName, thresholdValue):
        
        try:
            self.image = cv2.imread(fileName)
            self.thresholdValue = thresholdValue
            self.processImage()
            ratio = self.countPixels()
            self.exportImage(fileName)

            return ratio

        except:
            print("Error reading image file.")
            return False

    
    def processImage(self):

        processedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        processedImage = cv2.GaussianBlur(processedImage, (11, 11), 0)
        # threshold the image to reveal light regions in the
        # blurred image
        processedImage = cv2.threshold(processedImage, self.thresholdValue, 255, cv2.THRESH_BINARY)[1]
        # perform a series of erosions and dilations to remove
        # any small blobs of noise from the thresholded image
        processedImage = cv2.erode(processedImage, None, iterations=2)
        processedImage = cv2.dilate(processedImage, None, iterations=4)

        # Crop image  
        self.height, self.width, _ = self.image.shape
        radius = int(self.height/2 if self.height < self.width else self.width/2) + int(abs(self.height-self.width)/4)
        # create circle mask
        circMask = np.zeros((self.height, self.width), np.uint8)
        cv2.circle(circMask, (int(self.width/2), int(self.height/2)), radius, (255, 255, 255), thickness=-1)
        # Invert colors
        processedImage = np.invert(processedImage)
        # Apply mask for cropped effect
        processedImage = cv2.bitwise_and(processedImage, processedImage, mask=circMask)

        self.resultingImage = processedImage


    def countPixels(self):

        if self.resultingImage is "":
            return 0

        total = self.width*self.height
        white = cv2.countNonZero(self.resultingImage)

        return white/total*100

    
    def exportImage(self, fileName):
                
        filename = fileName.split("/")
        filename = "mod-"+filename[len(filename)-1]
        print(filename, "exported")
        cv2.imwrite(filename, thresh)