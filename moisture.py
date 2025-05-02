import RPi.GPIO as GPIO
import time

SENSOR_PIN = 13  # GPIO17 (Pin 33)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:
            print("Soil is wet")
        else:
            print("Soil is dry")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
