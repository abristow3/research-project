from datetime import datetime
import os
import csv


class DataHandler:
    def __init__(self):
        self.data_folder = 'data'
        self.data_file_name = 'timeseries_data.csv'

        self.setup()

    def setup(self):
        # Create data folder and empty file
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # Check if the file exists, if not, create it
        if not os.path.exists(self.data_file_name):
            # Create the file and write the header if it's a CSV
            with open(self.data_file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Create headers
                writer.writerow(
                    ['timestamp', 'ph', 'temperature', 'soil_moisture', 'humidity', 'yellowing', 'image_filepath'])
            print(f"File {self.data_file_name} created.")
        else:
            print(f"File {self.data_file_name} already exists.")

    @staticmethod
    def create_data_entry(temperature, moisture, humidity, ph, image_name, yellowing):
        # Get current datetime
        now = datetime.now()

        # Get current time in milliseconds
        milliseconds = int(now.timestamp() * 1000)
        data = {
            milliseconds:
                {
                    'ph': ph,
                    'temperature': temperature,
                    'soil_moisture': moisture,
                    'humidity': humidity,
                    'image_name': image_name,
                    'yellowing': yellowing
                }
        }

        return data

    def write_data_entry(self, data: dict):
        for timestamp, entry in data.items():
            # Extract the data from the entry dictionary
            ph = entry['ph']
            temperature = entry['temperature']
            soil_moisture = entry['soil_moisture']
            humidity = entry['humidity']
            image_name = entry['image_name']
            yellowing = entry['yellowing']

            # Open CSV file in append mode
            with open(self.data_file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write the data as a new row
                writer.writerow([
                    timestamp, ph, temperature, soil_moisture, humidity, yellowing, image_name
                ])
            print(f"Data written for timestamp {timestamp}")

    def read_data_entry(self):
        ...
