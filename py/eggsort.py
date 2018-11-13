from servo import Servo
from imageParser import ImageParser
from imageCapturer import ImageCapturer
import RPi.GPIO as GPIO

import time
import config

pushServoPin = config.pushServoPin
laneServoLeftPin = config.laneServoLeftPin
laneServoRightPin = config.laneServoRightPin

servoPush = None
servoLaneLeft = None
servoLaneRight = None

camera = None

parser = None

def init():
    # Prepare GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Instantiate Servo motors
    servoPush = Servo(servoPush, 0)
    servoLaneLeft = Servo(servoLaneLeft, 90)
    servoLaneRight = Servo(servoLaneRight, 90)
    # Instantiate image capturer
    camera = ImageCapturer()
    camera.setZoom(config.cropArea)
    # Instantiate image parser
    parser = ImageParser()


def sort():

    imageName = camera.takeImage()

    if not image:
        return
    
    ratio = parser.parseImage(imageName, config.dirtSensitivity)

    if ratio >= config.dirtThresh:
        servoLaneLeft.rotate(config.laneAngle)
        servoLaneRight.rotate(config.laneAngle)
        push()
        print("Egg is dirty.")
        return

    ratio = parser.parseImage(imageName, config.rottenSensitivity)

    if ratio >= config.rottenThresh:
        servoLaneLeft.rotate(-config.laneAngle)
        servoLaneRight.rotate(-config.laneAngle)
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
        sort()
        reset()
    except KeyboardInterrupt:
        GPIO.cleanup()
        camera.close()
    
    GPIO.cleanup()
    camera.close()


if __name__ == '__main__':
    main()