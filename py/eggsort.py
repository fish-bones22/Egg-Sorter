from servo import Servo
from imageParser import ImageParser
from imageCapturer import ImageCapturer
import RPi.GPIO as GPIO
from gpiozero import Button
from tendo import singleton


import os.path
import subprocess
from time import sleep

import config


def init():

    global pushServoPin, laneServoLeftPin, laneServoRightPin 

    global servoPush, servoLaneLeft, servoLaneRight 
    global camera, parser
    global button

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
    # Instantiate button
    button = Button(config.buttonPin, bounce_time = 0.5)
    button.when_pressed = buttonPressed


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


def buttonPressed():
    print("Button is pressed")
    if not os.path.isfile("/home/pi/on"):
        subprocess.Popen("touch /home/pi/on", shell=True, stdout=subprocess.PIPE)
        print("Starting")
        reset() 
        sort()
        subprocess.Popen("sudo rm -f /home/pi/on", shell=True, stdout=subprocess.PIPE)
        print("Done")


def main():
    
    me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

    print ("Starting Egg Sorter program ( ͡° ͜ʖ ͡°)")

    init()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        button.close()
        GPIO.cleanup()
        camera.close()
    
    button.close()
    GPIO.cleanup()
    camera.close()


if __name__ == '__main__':
    main()