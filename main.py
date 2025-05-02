from camera import Camera
from moisture import Moisture
from humidity import TempHumidity

if __name__ == '__main__':
    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()

    temp_humid_data = temp_humidity.get_reading()
    print("SDATA", temp_humid_data)

    moisture.get_moisture_reading()

