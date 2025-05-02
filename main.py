from Camera import Camera
from Moisture import Moisture
from Humidity import TempHumidity
from Ph import Ph
from DataHandler import DataHandler
from YellowDetector import YellowDetector
import os
import time

def load_model():
    ...

if __name__ == '__main__':
    data_handler = DataHandler()
    yellow_detector = YellowDetector()

    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()
    ph = Ph()

    # TODO Load our ML Model

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

        # TODO if it was yellow, run a model on the data and test if it was due to envinromental factors or not


        # Sleep 24 hours in seconds
        time.sleep(86400)
