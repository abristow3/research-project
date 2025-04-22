import Adafruit_DHT
import time

# Set the sensor type and the GPIO pin connected to the sensor
sensor = Adafruit_DHT.DHT22  # DHT22 sensor
gpio_pin = 17  # GPIO pin number (change as necessary)


def read_dht22():
    # Try to get a valid reading from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)

    # Check if reading was successful
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
    else:
        print("Failed to retrieve data from the sensor. Try again!")


# Main loop
try:
    while True:
        print("\nReading from the DHT22 sensor...")
        read_dht22()
        time.sleep(2)  # Wait 2 seconds before reading again

except KeyboardInterrupt:
    print("\nProgram exited.")