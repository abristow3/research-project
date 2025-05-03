import cv2
from datetime import datetime
import os
import shutil

import cv2
import os
import shutil
from datetime import datetime
import time


class Camera:
    def __init__(self):
        self.unprocessed_images_folder = "unprocessed_images"
        self.processed_images_folder = "processed_images"

        # Initialize the webcam (attempt to use the default camera)
        self.camera = cv2.VideoCapture(0)

        # Add delay to allow the camera to initialize
        time.sleep(2)

        # Ensure the folders exist
        self.setup()

        # Check if the camera is opened successfully
        if not self.camera.isOpened():
            print("cannot access camera")
            exit()

    def setup(self) -> None:
        if not os.path.exists(self.unprocessed_images_folder):
            os.makedirs(self.unprocessed_images_folder)

        if not os.path.exists(self.processed_images_folder):
            os.makedirs(self.processed_images_folder)

    def take_photo(self) -> str:
        # Read a single frame
        ret, frame = self.camera.read()
        if not ret:
            print("failed to grab frame")
            self.camera.release()
            exit()

        # Generate a timestamped filename
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
        filename = f"{self.unprocessed_images_folder}/{filename}"

        # Save the captured image
        cv2.imwrite(filename, frame)
        print(f"image saved as {filename}")

        return filename

    def move_processed_image(self, filename: str) -> None:
        src_path = os.path.join(self.unprocessed_images_folder, filename)
        dest_path = os.path.join(self.processed_images_folder, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
        else:
            print(f"{filename} does not exist")

    def release_camera(self):
        if self.camera.isOpened():
            self.camera.release()
            print("Camera released.")
