import os
import cv2
import numpy as np


class YellowDetector:
    def __init__(self):
        self.lower_yellow = (15, 80, 100)
        self.upper_yellow = (40, 255, 255)
        self.lower_green = (35, 40, 40)
        self.upper_green = (85, 255, 255)

    def detect_yellowing(self, image_path) -> float:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("The image path provided is invalid or the image could not be loaded.")

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # create mask for green pixels
        green_mask = cv2.inRange(hsv_image, self.lower_green, self.upper_green)

        # create a mask for yellow pixels
        yellow_mask = cv2.inRange(hsv_image, self.lower_yellow, self.upper_yellow)

        # combine masks
        combined_mask = cv2.bitwise_or(green_mask, yellow_mask)

        # Get yellow pixels
        yellow_pixels = np.sum(yellow_mask == 255)

        # calculate combined pixels
        total_pixels = np.sum(combined_mask == 255)

        # avoid division by zero
        if total_pixels == 0:
            return 0.0

        # calc percentage of yellow pixels in combined mask
        yellow_percentage = (yellow_pixels / total_pixels) * 100

        # return percentage of yellowing detected in image
        return yellow_percentage

# if __name__ == "__main__":
#     yellow_detector = YellowDetector()
#     yellowing = 0
#     count = 0
#     ycount = 0
#     for filename in os.listdir("archive2/BPLD/yellow mosaic"):
#         count += 1
#         yellow_percentage = yellow_detector.detect_yellowing(f"archive2/BPLD/yellow mosaic/{filename}")
#
#         if yellow_percentage >= 15:
#             ycount += 1
#             yellowing = 1
#
#     print(f"{count} Test Images | {ycount} Detections at 20% threshold")
#     print(f"{ycount / count * 100}")
#
#     yellowing = 0
#     count = 0
#     ycount = 0
#
#     for filename in os.listdir("archive2/BPLD/healthy"):
#         count += 1
#         yellow_percentage = yellow_detector.detect_yellowing(f"archive2/BPLD/healthy/{filename}")
#
#         if yellow_percentage >= 15:
#             ycount += 1
#             yellowing = 1
#
#     print(f"{count} Test Images | {ycount} Detections at 20% threshold")
#     print(f"{ycount / count * 100}")
