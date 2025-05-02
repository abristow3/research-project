import RPi.GPIO as GPIO


class Ph:
    def __init__(self):
        self.clk_pin = 17  # SPI Clock (Pin 11)
        self.miso_pin = 27  # SPI MISO (Pin 13)
        self.mosi_pin = 22  # SPI MOSI (Pin 15)
        self.cs_pin = 26  # SPI CS (Pin 37)

        self.setup()

    def setup(self):
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk_pin, GPIO.OUT)
        GPIO.setup(self.miso_pin, GPIO.IN)
        GPIO.setup(self.mosi_pin, GPIO.OUT)
        GPIO.setup(self.cs_pin, GPIO.OUT)

    def get_ph_reading(self):
        adc_val = self.read_adc(0)
        voltage = self.adc_to_voltage(adc_val)
        ph = self.voltage_to_ph(voltage)

        # Print for logging
        print(f"ADC: {adc_val} | Voltage: {voltage:.2f} V | pH: {ph:.2f}")
        return ph

    def read_adc(self, channel):
        if channel < 0 or channel > 7:
            return -1

        GPIO.output(self.cs_pin, True)
        GPIO.output(self.clk_pin, False)
        GPIO.output(self.cs_pin, False)

        command = channel
        command |= 0x18  # Start bit + single-ended
        command <<= 3

        for i in range(5):
            GPIO.output(self.mosi_pin, command & 0x80)
            command <<= 1
            GPIO.output(self.clk_pin, True)
            GPIO.output(self.clk_pin, False)

        result = 0
        for i in range(12):
            GPIO.output(self.clk_pin, True)
            GPIO.output(self.clk_pin, False)
            result <<= 1
            if GPIO.input(self.miso_pin):
                result |= 0x1

        GPIO.output(self.cs_pin, True)
        result >>= 1  # drop null bit
        return result

    @staticmethod
    def adc_to_voltage(adc_value, vref=3.3):
        return adc_value * (vref / 1023.0)

    @staticmethod
    def voltage_to_ph(voltage) -> float:
        # Adding a calibration to formula since sensor is not calibrated
        voltage_at_ph7 = 3.30  # Your actual voltage at pH 7.0
        volts_per_ph = 0.18  # Adjust this based on real buffer testing
        ph = 7.0 + (voltage_at_ph7 - voltage) / volts_per_ph
        return float(ph)
