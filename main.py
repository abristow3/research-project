from camera import Camera
from moisture import Moisture
from humidity import TempHumidity
from ph import Ph
from data_handler import DataHandler


if __name__ == '__main__':
    data_handler = DataHandler()
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

    # TODO setup yellowing from image processing. Yellowing should be a 1 if present or 0 if not
    data_handler.create_data_entry(temperature=temp_humid_reading['temperature'], moisture=moisture_reading,
                                   humidity=temp_humid_reading['humidity'], ph=ph_reading, image_name=image_filename,
                                   yellowing=1)

