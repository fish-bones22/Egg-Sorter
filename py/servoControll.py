from Servo import Servo
import RPi.GPIO as GPIO
import time

                
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servoPin = 4
servo = Servo(servoPin)

try:
    while True:
        servo.rotate(0)
        time.sleep(1)
        servo.rotate(45)
        time.sleep(2)

except KeyboardInterrupt:
    servo.rotate(0)
    GPIO.cleanup()