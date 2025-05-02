from Camera import Camera
from Moisture import Moisture
from Humidity import TempHumidity
from Ph import Ph
from DataHandler import DataHandler
from YellowDetector import YellowDetector
import os

if __name__ == '__main__':
    data_handler = DataHandler()
    yellow_detector = YellowDetector()

    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()
    ph = Ph()

    # Get sensor readings
    temp_humid_reading = temp_humidity.get_reading()
    moisture_reading = moisture.get_moisture_reading()
    ph_reading = ph.get_ph_reading()

    # Take photo
    image_filename = camera.take_photo()

    yellowing = 0
    count = 0
    ycount = 0
    for filename in os.listdir("archive2/BPLD/yellow mosaic"):
        count += 1
        yellow_percentage = yellow_detector.detect_yellowing(f"archive2/BPLD/yellow mosaic/{filename}")

        if yellow_percentage >= 20:
            ycount += 1
            yellowing = 1

    print(f"{count} Test Images | {ycount} Detections at 20% threshold")

    entry = data_handler.create_data_entry(temperature=temp_humid_reading['temperature'], moisture=moisture_reading,
                                           humidity=temp_humid_reading['humidity'], ph=ph_reading,
                                           image_name=image_filename, yellowing=yellowing)

    data_handler.write_data_entry(data=entry)
