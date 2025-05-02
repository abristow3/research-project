from camera import Camera
from moisture import Moisture
from humidity import TempHumidity
from ph import Ph

if __name__ == '__main__':
    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()
    ph = Ph()

    # Get sensor readings
    temp_humid_reading = temp_humidity.get_reading()
    moisture_reading = moisture.get_moisture_reading()
    ph_reading = ph.get_ph_reading()

    print("PH", ph_reading)

    # Take photo
    camera.take_photo()

