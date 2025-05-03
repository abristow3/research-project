from Camera import Camera
from Moisture import Moisture
from Humidity import TempHumidity
from Ph import Ph
from DataHandler import DataHandler
from YellowDetector import YellowDetector
import time
from HealthModel import HealthModel


class MonitoringSystem:
    def __init__(self, data_handler, yellow_detector, camera, moisture, temp_humidity, ph, health_model, interval=86400):
        self.data_handler = data_handler
        self.yellow_detector = yellow_detector
        self.camera = camera
        self.moisture = moisture
        self.temp_humidity = temp_humidity
        self.ph = ph
        self.health_model = health_model
        self.interval = interval

    def monitor(self):
        """Start monitoring the system, collecting data and detecting diseases."""
        while True:
            # Get sensor readings
            temp_humid_reading = self.temp_humidity.get_reading()
            moisture_reading = self.moisture.get_moisture_reading()
            ph_reading = self.ph.get_ph_reading()

            # Take photo
            image_filename = self.camera.take_photo()

            # Check image for yellowing
            yellowing = 0
            yellow_percentage = self.yellow_detector.detect_yellowing(f"unprocessed_images/{image_filename}")

            # Determine if enough yellowing present
            if yellow_percentage >= 20:
                yellowing = 1

            entry = self.data_handler.create_data_entry(
                temperature=temp_humid_reading['temperature'],
                moisture=moisture_reading,
                humidity=temp_humid_reading['humidity'],
                ph=ph_reading,
                image_name=image_filename,
                yellowing=yellowing
            )

            self.data_handler.write_data_entry(data=entry)
            disease_detected = self.health_model.predict_disease(entry=entry)

            if disease_detected:
                print("DISEASE DETECTED")

            time.sleep(self.interval)


# Main execution
if __name__ == '__main__':
    # Instantiate the required components
    data_handler = DataHandler()
    yellow_detector = YellowDetector()
    camera = Camera()
    moisture = Moisture()
    temp_humidity = TempHumidity()
    ph = Ph()
    health_model = HealthModel()

    # Frequency in seconds the process will run
    interval = 10

    # Create the monitoring system
    monitoring_system = MonitoringSystem(
        data_handler=data_handler,
        yellow_detector=yellow_detector,
        camera=camera,
        moisture=moisture,
        temp_humidity=temp_humidity,
        ph=ph,
        health_model=health_model,
        interval=interval
    )

    # Start the monitoring process
    monitoring_system.monitor()
