import RPi.GPIO as GPIO


class Moisture:
    def __init__(self):
        self.sensor_pin = 13  # GPIO17 (Pin 33)
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    def get_moisture_reading(self) -> int:
        # Returns a 1 if the soil is wet
        # Returns a 0 if the soil is dry

        if GPIO.input(self.sensor_pin) == GPIO.LOW:
            print("Soil is wet")
            return 1
        else:
            print("Soil is dry")
            return 0
