from servo import Servo
from imageParser import ImageParser
from imageCapturer import ImageCapturer
import RPi.GPIO as GPIO

from time import sleep
import config

# global pushServoPin
# global laneServoLeftPin
# global laneServoRightPin 

# global servoPush
# global servoLaneLeft
# global servoLaneRight 
# global camera
# global parser

def init():

    global pushServoPin, laneServoLeftPin, laneServoRightPin 

    global servoPush, servoLaneLeft, servoLaneRight 
    global camera, parser

    # Prepare GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Initialize variables
    pushServoPin = config.pushServoPin
    laneServoLeftPin = config.laneServoLeftPin
    laneServoRightPin = config.laneServoRightPin
    # Instantiate Servo motors
    servoPush = Servo(pushServoPin, 0)
    servoLaneLeft = Servo(laneServoLeftPin, config.returnAngle)
    servoLaneRight = Servo(laneServoRightPin, config.returnAngle)
    # Instantiate image capturer
    camera = ImageCapturer()
    camera.setZoom(config.cropArea)
    # Instantiate image parser
    parser = ImageParser()


def sort():

    global camera, parser, servoLaneLeft, servoLaneRight, servoPush

    imageName = camera.takeImage()

    if not imageName:
        return

    # Check for dirtiness
    ratio = parser.parseImage(imageName, config.dirtSensitivity)
    print(ratio, "% of pixels are dark enough to be dirty. Threshold is", config.dirtThresh)
    if ratio >= config.dirtThresh:
        servoLaneLeft.rotate(config.returnAngle + config.laneAngle)
        servoLaneRight.rotate(config.returnAngle + config.laneAngle)
        push()
        print("Egg is dirty.")
        return

    # Check for rotteness
    ratio = parser.parseImage(imageName, config.rottenSensitivity)
    print(ratio, "% of pixels are dark enough to be rotten. Threshold is", config.rottenThresh)
    if ratio >= config.rottenThresh:
        servoLaneLeft.rotate(config.returnAngle-config.laneAngle)
        servoLaneRight.rotate(config.returnAngle-config.laneAngle)
        push()
        print("Egg is rotten.")
        return

    push()
    print("Egg is fresh")


def push():
    servoPush.rotate(90)
    sleep(0.5)
    servoPush.reset()


def reset():
    servoLaneLeft.reset()
    servoLaneRight.reset()


def main():
    try:
        init()
        reset()
        sort()
    except KeyboardInterrupt:
        GPIO.cleanup()
        camera.close()
    
    GPIO.cleanup()
    camera.close()


if __name__ == '__main__':
    main()