import RPi.GPIO as GPIO
from time import sleep

class Servo:

    pin = 0
    pwm = ""
    sleepInterval = 0.02
    frequency = 50
    __constFactor = 0.05556


    def __init__ (self, pin):

        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.pin, self.frequency)

        self.pwm.start(0)


    def __del__(self):
        self.rotate(0)
        self.pwm.stop()


    def reset(self):
        self.rotate(0)


    def rotate(self, degree):
        cycle = self.__convertFromDegreeToCycle(degree)
        print ("rotating ", degree, " degrees")
        self.pwm.ChangeDutyCycle(cycle)
        sleep(self.sleepInterval)


    def __convertFromDegreeToCycle(self, degree):
        
        if degree < 0:
            degree += 180

        if degree > 180:
            degree -= 180
        
        return round(2.5 + (degree*self.__constFactor), 2)
        
