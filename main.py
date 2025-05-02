from camera import Camera
from moisture import Moisture

if __name__ == '__main__':
    camera = Camera()
    moisture = Moisture()

    moisture.get_moisture_reading()