import RPi.GPIO as GPIO
from time import sleep

class Servo:

    pin = 0
    pwm = ""
    sleepInterval = 0.02
    frequency = 50
    __constFactor = 0.05556
    resetValue = 0


    def __init__ (self, pin, resetValue):

        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.pin, self.frequency)

        self.pwm.start(self.resetValue)


    def __del__(self):
        self.rotate(self.resetValue)
        self.pwm.stop()


    def reset(self):
        self.rotate(self.resetValue)


    def rotate(self, degree):
        cycle = self.__convertFromDegreeToCycle(degree)
        self.pwm.ChangeDutyCycle(cycle)
        sleep(self.sleepInterval)


    def __convertFromDegreeToCycle(self, degree):
        
        if degree < 0:
            degree += 180

        if degree > 180:
            degree -= 180
        
        return round(2.5 + (degree*self.__constFactor), 2)
        
