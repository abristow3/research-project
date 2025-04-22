import spidev
import time

# Set up SPI communication
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 1350000  # Set the SPI clock speed


# Function to read ADC value from MCP3008
def read_adc(channel):
    if channel > 7 or channel < 0:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


# Function to convert ADC value to pH value
def adc_to_ph(adc_value):
    # Example calibration equation (you may need to calibrate the sensor):
    voltage = (adc_value / 1023.0) * 3.3  # Convert ADC value to voltage (assuming 3.3V reference)
    # Convert voltage to pH (This will depend on your sensor's calibration)
    # pH = (voltage - 2.5) * 3.5  # This is an example equation; adjust for your sensor's calibration
    pH = (voltage - 0.5) * 10  # Example conversion; this equation needs to be adjusted according to sensor
    return pH


# Main loop
try:
    while True:
        print("\nReading pH value...")

        # Read ADC from channel 0 (connected to pH sensor)
        adc_value = read_adc(0)

        if adc_value == -1:
            print("Invalid ADC channel.")
            continue

        # Convert the ADC value to a pH value
        ph_value = adc_to_ph(adc_value)

        # Display the pH value
        print(f"pH Value: {ph_value:.2f}")

        time.sleep(2)  # Wait for 2 seconds before the next reading

except KeyboardInterrupt:
    print("\nProgram exited.")
    spi.close()  # Close the SPI connection
