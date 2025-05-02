import RPi.GPIO as GPIO


class Moisture:
    def __init__(self):
        self.sensor_pin = 13  # GPIO17 (Pin 33)
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    def get_moisture_reading(self):
        if GPIO.input(self.sensor_pin) == GPIO.LOW:
            print("Soil is wet")
        else:
            print("Soil is dry")
