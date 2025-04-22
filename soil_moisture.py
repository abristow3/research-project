import RPi.GPIO as GPIO
import time

# Set up the GPIO mode and the pin to which the sensor is connected
GPIO.setmode(GPIO.BCM)
MOISTURE_SENSOR_PIN = 17  # You can change this to any GPIO pin you use

# Set the GPIO pin as input
GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

# Function to read the moisture sensor
def read_soil_moisture():
    if GPIO.input(MOISTURE_SENSOR_PIN):
        print("Soil is Wet")
    else:
        print("Soil is Dry")

# Main loop to check moisture every 2 seconds
try:
    while True:
        print("\nChecking Soil Moisture...")
        read_soil_moisture()
        time.sleep(2)  # Check every 2 seconds

except KeyboardInterrupt:
    print("\nProgram exited.")
    GPIO.cleanup()  # Clean up GPIO on exit
