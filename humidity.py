from typing import Dict, Any

import Adafruit_DHT
import time


class TempHumidity:
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT22
        self.sensor_pin = 19  # GPIO19 is physical pin 35

    def get_reading(self)->dict:
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)

        if humidity is not None and temperature is not None:
            # Create dict with data points
            sensor_data = {
                'temperature': temperature,
                'humidity': humidity
            }

            # print for logging
            print(f"Temp: {temperature:.1f}°C  |  Humidity: {humidity:.1f}%")
            return sensor_data
        else:
            print("Invalid data: Temperature or Humidity is None.")
            return {}
