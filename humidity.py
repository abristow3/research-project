import Adafruit_DHT
import time

# Sensor type and GPIO setup
SENSOR = Adafruit_DHT.DHT22
GPIO_PIN = 19  # GPIO27 is physical pin 35

print("Reading DHT22 sensor on GPIO27 (Pin 35)...")

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO_PIN)
        
        if humidity is not None and temperature is not None:
            print(f"Temp: {temperature:.1f}°C  |  Humidity: {humidity:.1f}%")
        else:
            print("Sensor read failed. Trying again...")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopped by user.")


