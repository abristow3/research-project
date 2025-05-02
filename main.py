from Camera import Camera
from Moisture import Moisture
from Humidity import TempHumidity
from Ph import Ph
from DataHandler import DataHandler
from YellowDetector import YellowDetector
import os
import time

if __name__ == '__main__':
    data_handler = DataHandler()
    yellow_detector = YellowDetector()

    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()
    ph = Ph()

    while True:
        # Get sensor readings
        temp_humid_reading = temp_humidity.get_reading()
        moisture_reading = moisture.get_moisture_reading()
        ph_reading = ph.get_ph_reading()

        # Take photo
        image_filename = camera.take_photo()

        # Check image for yellowing
        yellowing = 0
        yellow_percentage = yellow_detector.detect_yellowing(f"unprocessed_images/{image_filename}")

        if yellow_percentage >= 20:
            yellowing = 1

        entry = data_handler.create_data_entry(temperature=temp_humid_reading['temperature'], moisture=moisture_reading,
                                               humidity=temp_humid_reading['humidity'], ph=ph_reading,
                                               image_name=image_filename, yellowing=yellowing)

        data_handler.write_data_entry(data=entry)

        # Sleep 8 hours in seconds
        time.sleep(28800)
