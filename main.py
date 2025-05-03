from datetime import datetime

from Camera import Camera
from Moisture import Moisture
from Humidity import TempHumidity
from Ph import Ph
from DataHandler import DataHandler
from YellowDetector import YellowDetector
import time
from HealthModel import HealthModel
import RPi.GPIO as GPIO


class MonitoringSystem:
    def __init__(self, data_handler, yellow_detector, camera, moisture, temp_humidity, ph, health_model, interval=86400,
                 led_pin=17):
        self.data_handler = data_handler
        self.yellow_detector = yellow_detector
        self.camera = camera
        self.moisture = moisture
        self.temp_humidity = temp_humidity
        self.ph = ph
        self.health_model = health_model
        self.interval = interval
        self.led_pin = led_pin

        # Setup GPIO mode and pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.LOW)  # Start with LED off

    def monitor(self):
        while True:
            # Get sensor readings
            temp_humid_reading = self.temp_humidity.get_reading()
            moisture_reading = self.moisture.get_moisture_reading()
            ph_reading = self.ph.get_ph_reading()

            # Take photo
            image_filename = self.camera.take_photo()

            # Check image for yellowing
            yellowing = 0
            yellow_percentage = self.yellow_detector.detect_yellowing(image_path=image_filename)

            # Determine if enough yellowing present
            if yellow_percentage >= 20:
                yellowing = 1

            entry = self.data_handler.create_data_entry(
                temperature=temp_humid_reading['temperature'],
                moisture=moisture_reading,
                humidity=temp_humid_reading['humidity'],
                ph=ph_reading,
                image_name=image_filename,
                yellowing=yellowing
            )

            print(f"ENTRY: {entry}")

            self.data_handler.write_data_entry(data=entry)

            # Uncomment to test LED
            # entry = {
            #     'timestamp': datetime.now(),
            #     'temperature': 22,
            #     'humidity': 70,
            #     'moisture': 1,
            #     'ph': 7,
            #     'yellowing': 1
            # }

            disease_detected = self.health_model.predict_disease(entry=entry)

            if disease_detected:
                print("DISEASE DETECTED")
                self.turn_on_led()

            # Release the camera after use
            self.camera.release_camera()

            # Sleep for the interval before repeating the process
            time.sleep(self.interval)

            # Re-initialize the camera before the next photo
            self.camera = Camera()

    def turn_on_led(self):
        GPIO.output(self.led_pin, GPIO.HIGH)
        print("LED ON")
        time.sleep(10)  # Keep the LED on for 10 seconds
        GPIO.output(self.led_pin, GPIO.LOW)


# Main execution
if __name__ == '__main__':
    data_handler = DataHandler()
    yellow_detector = YellowDetector()
    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()
    ph = Ph()
    health_model = HealthModel()

    # Frequency in seconds the process will run
    interval = 10

    led_pin = 6 # bcm6 (Pin 31)

    # Create the monitoring system
    monitoring_system = MonitoringSystem(
        data_handler=data_handler,
        yellow_detector=yellow_detector,
        camera=camera,
        moisture=moisture,
        temp_humidity=temp_humidity,
        ph=ph,
        health_model=health_model,
        interval=interval,
        led_pin=led_pin
    )

    monitoring_system.monitor()
