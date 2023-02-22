#!/usr/bin/python

## This is for the HC-SR04 distance sensor NOT the Radar sensor
import RPi.GPIO as GPIO
import time


def get_distance():
    try:
        sensor = DistanceSensor(12, 11)
        return sensor.take_measurement()
    except Exception as e:
        print(e)
        return 0


# This class is used to interface with the HC-SR04 distance sensor
class DistanceSensor:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        self.pin_setup(echo, trigger)
        self.distance = 0

    # This function sets up the pins for the sensor
    def pin_setup(self, echo=12, trigger=11):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

    # This function takes a measurement from the sensor
    def take_measurement(self):
        GPIO.output(self.trigger, GPIO.LOW)
        # Waiting for sensor to settle
        time.sleep(2)

        print("Reading at:" + time.asctime())
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)
        while GPIO.input(self.echo) == 0:
            pass
        pulse_start_time = time.time()
        while GPIO.input(self.echo) == 1:
            pass
        pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        self.distance = round(pulse_duration * 17150, 2)
        print("Distance: ", self.distance, " cm")
        return self.distance

    # This function cleans up the GPIO pins
    def __del__(self):
        GPIO.cleanup()
