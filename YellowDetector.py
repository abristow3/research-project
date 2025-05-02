# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
import os

import cv2
import numpy as np


class YellowDetector:
    def __init__(self):
        self.lower_yellow = (15, 80, 100)
        self.upper_yellow = (40, 255, 255)
        self.lower_green = (35, 40, 40)
        self.upper_green = (85, 255, 255)

    def detect_yellowing(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("The image path provided is invalid or the image could not be loaded.")

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Step 1: Create a mask to isolate the green areas (leaf color)
        green_mask = cv2.inRange(hsv_image, self.lower_green, self.upper_green)

        # Step 2: Create a mask for yellow pixels (yellowing areas)
        yellow_mask = cv2.inRange(hsv_image, self.lower_yellow, self.upper_yellow)

        # Step 3: Combine the green and yellow masks
        combined_mask = cv2.bitwise_or(green_mask, yellow_mask)

        # Step 4: Calculate the yellow percentage compared to the combined mask
        # Extract yellow pixels from the yellow mask
        yellow_pixels = np.sum(yellow_mask == 255)

        # Calculate the total pixels in the combined mask (green + yellow pixels)
        total_pixels = np.sum(combined_mask == 255)

        # Avoid division by zero if there are no green or yellow pixels
        if total_pixels == 0:
            return 0.0

        # Calculate the percentage of yellow pixels in the combined mask
        yellow_percentage = (yellow_pixels / total_pixels) * 100

        # Return the percentage of yellowing detected in the image
        return yellow_percentage


if __name__ == "__main__":
    yellow_detector = YellowDetector()
    yellowing = 0
    count = 0
    ycount = 0
    for filename in os.listdir("archive2/BPLD/yellow mosaic"):
        count += 1
        yellow_percentage = yellow_detector.detect_yellowing(f"archive2/BPLD/yellow mosaic/{filename}")

        if yellow_percentage >= 20:
            ycount += 1
            yellowing = 1

    print(f"{count} Test Images | {ycount} Detections at 20% threshold")
    print(f"{ycount/count * 100}")



