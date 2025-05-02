import cv2
from datetime import datetime

# Initialize the webcam (0 is usually the first USB camera)
cam = cv2.VideoCapture(0)

# Wait for camera to warm up
if not cam.isOpened():
    print("Cannot access camera")
    exit()

# Read a single frame
ret, frame = cam.read()
if not ret:
    print("Failed to grab frame")
    cam.release()
    exit()

# Generate a timestamped filename
filename = datetime.now().strftime("usb_photo_%Y%m%d_%H%M%S.jpg")

# Save the captured image
cv2.imwrite(filename, frame)
print(f"Image saved as {filename}")

# Release the camera
cam.release()

