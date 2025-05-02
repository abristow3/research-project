import cv2
from datetime import datetime
import os
import shutil


class Camera:
    def __init__(self):
        self.unprocessed_images_folder = "unprocessed_images"
        self.processed_images_folder = "processed_images"

        # Initialize the webcam
        self.camera = cv2.VideoCapture(0)

        self.setup()

    def setup(self) -> None:
        if not os.path.exists(self.unprocessed_images_folder):
            os.makedirs(self.unprocessed_images_folder)

        if not os.path.exists(self.processed_images_folder):
            os.makedirs(self.processed_images_folder)

    def take_photo(self) -> str:
        # Wait for camera to warm up
        if not self.camera.isOpened():
            print("cannot access camera")
            exit()

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

        # Release the camera
        self.camera.release()

        return filename

    def move_processed_image(self, filename: str) -> None:
        src_path = os.path.join(self.unprocessed_images_folder, filename)
        dest_path = os.path.join(self.processed_images_folder, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
        else:
            print(f"{filename} does not exist")
