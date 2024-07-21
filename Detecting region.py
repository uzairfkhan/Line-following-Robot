import cv2
from PIL import Image
import numpy as np


def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle hue wrap-around
    lowerLimit = np.array([max(0, hue - 10), 100, 100], dtype=np.uint8)
    upperLimit = np.array([min(180, hue + 10), 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit





cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the color for detection (e.g., green)
    color_to_detect = [0, 255, 0]

    # Get the lower and upper limits for the color
    lowerLimit, upperLimit = get_limits(color=color_to_detect)

    # Create a mask using the color limits
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around each detected region
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 5)

    # Display the frame with rectangles
    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
