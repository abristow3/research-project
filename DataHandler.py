from datetime import datetime
import os
import csv


class DataHandler:
    def __init__(self):
        self.data_folder = 'data'
        self.data_file_name = 'timeseries_data.csv'

        self.setup()

    def setup(self) -> None:
        # create data dir
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # check if file exists, if not, create it
        if not os.path.exists(self.data_file_name):
            # create the file and write headers
            with open(self.data_file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['timestamp', 'ph', 'temperature', 'soil_moisture', 'humidity', 'yellowing', 'image_filepath'])
            print(f"{self.data_file_name} created.")
        else:
            print(f"{self.data_file_name} already exists.")

    @staticmethod
    def create_data_entry(temperature, moisture, humidity, ph, image_name, yellowing) -> dict:
        # Get current datetime
        now = datetime.now()

        # Get current time in milliseconds
        milliseconds = int(now.timestamp() * 1000)
        data = {'timestamp': milliseconds,
                'ph': ph,
                'temperature': temperature,
                'soil_moisture': moisture,
                'humidity': humidity,
                'image_name': image_name,
                'yellowing': yellowing
                }

        return data

    def write_data_entry(self, data: dict) -> None:
        timestamp = data['timestamp']
        ph =data['ph']
        temperature = data['temperature']
        soil_moisture = data['soil_moisture']
        humidity = data['humidity']
        image_name = data['image_name']
        yellowing = data['yellowing']

        # append csv
        with open(f"{self.data_folder}/{self.data_file_name}", mode='a', newline='') as file:
            writer = csv.writer(file)
            # write the data as a new row
            writer.writerow([
                timestamp, ph, temperature, soil_moisture, humidity, yellowing, image_name
            ])
        print(f"data written for timestamp {timestamp}")
