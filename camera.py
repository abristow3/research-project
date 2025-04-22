import time
import picamera

# Initialize the camera
camera = picamera.PICamera()

# Allow the camera to warm up
time.sleep(2)

# Capture a still image
camera.capture('image.jpg')
print("Image captured and saved as 'image.jpg'")

# Release the camera
camera.close()
