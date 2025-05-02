import RPi.GPIO as GPIO
import time

# GPIO pin setup (BCM numbering)
CLK = 17     # SPI Clock (Pin 11)
MISO = 27    # SPI MISO (Pin 13)
MOSI = 22    # SPI MOSI (Pin 15)
CS = 26      # SPI CS (Pin 37)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1

    GPIO.output(CS, True)
    GPIO.output(CLK, False)
    GPIO.output(CS, False)

    command = channel
    command |= 0x18  # Start bit + single-ended
    command <<= 3

    for i in range(5):
        GPIO.output(MOSI, command & 0x80)
        command <<= 1
        GPIO.output(CLK, True)
        GPIO.output(CLK, False)

    result = 0
    for i in range(12):
        GPIO.output(CLK, True)
        GPIO.output(CLK, False)
        result <<= 1
        if GPIO.input(MISO):
            result |= 0x1

    GPIO.output(CS, True)
    result >>= 1  # drop null bit
    return result

def adc_to_voltage(adc_value, vref=3.3):
    return adc_value * (vref / 1023.0)

def voltage_to_ph(voltage):
    voltage_at_pH7 = 3.30  # Your actual voltage at pH 7.0
    volts_per_pH = 0.18    # Adjust this based on real buffer testing
    return 7.0 + (voltage_at_pH7 - voltage) / volts_per_pH

try:
    while True:
        adc_val = read_adc(0)
        voltage = adc_to_voltage(adc_val)
        ph = voltage_to_ph(voltage)

        print(f"ADC: {adc_val} | Voltage: {voltage:.2f} V | pH: {ph:.2f}")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting.")

