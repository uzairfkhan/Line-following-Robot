import socket
import math
import cv2
import numpy as np
import struct
import time

TCP_IP = '192.168.160.96'
Host_IP = '192.168.122.127'
TCP_PORT = 10000
Host_PORT = 8080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
values = "100,300"

Begin = int(input("Press 1 to Begin : "))
if Begin:
    s.send((values + '\n').encode())

# Get LFR sensor values region


def detect_and_draw_green_and_red_patches(frame, min_size=40, min_distance=20):
    global values  # Use the global values variable

    # Convert the frame from BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a range for green color in HSV
    lower_green = np.array([39, 38, 97])  # Lower bound for green color
    upper_green = np.array([86, 255, 255])  # Upper bound for green color

    # Define a range for red color in HSV
    lower_red = np.array([0, 189, 87])  # Lower bound for red color
    upper_red = np.array([13, 255, 255])  # Upper bound for red color

    # Define a range for orange color in HSV
    lower_orng = np.array([15, 177, 130])  # Lower bound for orange color
    upper_orng = np.array([19, 255, 255])  # Upper bound for orange color

    # Threshold the frame to get green and red colors
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    orng_mask = cv2.inRange(hsv_frame, lower_orng, upper_orng)

    # Find contours in the green mask
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find contours in the red mask
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find contours in the orange mask
    orng_contours, _ = cv2.findContours(orng_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Reset values to default
    values = "100,300"

    # Store the detected green and red patches
    green_patches = []
    red_patches = []
    orng_patches = []

    # Draw rectangles around the detected green patches larger than min_size
    for green_contour in green_contours:
        x, y, w, h = cv2.boundingRect(green_contour)

        # Check if the size of the rectangle is larger than min_size
        if w > min_size and h > min_size:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Add text showing the size of the rectangle
            cv2.putText(frame, f"Green Size: {w}x{h}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Store the coordinates of the center of the green patch
            center = (x + w // 2, y + h // 2)
            green_patches.append(center)

    # Draw rectangles around the detected red patches larger than min_size
    for red_contour in red_contours:
        x, y, w, h = cv2.boundingRect(red_contour)

        # Check if the size of the rectangle is larger than min_size
        if w > min_size and h > min_size:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Add text showing the size of the rectangle
            cv2.putText(frame, f"Red Size: {w}x{h}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Store the coordinates of the center of the red patch
            center = (x + w // 2, y + h // 2)
            red_patches.append(center)

    for orng_contour in orng_contours:
        x, y, w, h = cv2.boundingRect(orng_contour)

        # Check if the size of the rectangle is larger than min_size
        if w > min_size and h > min_size:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Add text showing the size of the rectangle
            cv2.putText(frame, f"Orange Size: {w}x{h}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Store the coordinates of the center of the red patch
            center = (x + w // 2, y + h // 2)
            orng_patches.append(center)
    position = 'tbd'
    if len(green_patches) > 0 and len(red_patches) > 0:
        # Calculate the distance between the first green and first red patch
        distance = math.sqrt(
            (red_patches[0][0] - green_patches[0][0]) ** 2 + (red_patches[0][1] - green_patches[0][1]) ** 2)

        # Determine if the green patch is on the left or right of the red patch
        if green_patches[0][0] > red_patches[0][0]:
            position = 'l'
        else:
            position = 'r'

    if len(red_patches) > 0 and len(orng_patches) > 0:
        red_center = red_patches[0]
        orng_center = orng_patches[0]

        # Draw a line between the centers of red and orange patches
        cv2.line(frame, red_center, orng_center, (255, 0, 0), 2)
        values= "100,1"

        # Extend the line to the end of the frame
        frame_height, frame_width, _ = frame.shape
        denom=orng_center[0] - red_center[0]
        slope = (orng_center[1] - red_center[1]) / (orng_center[0] - red_center[0])

        # Calculate the new point at the bottom of the frame
        new_x = int(red_center[0] + (frame_height - red_center[1]) / slope)
        new_y = frame_height

        # Draw the extended line
        cv2.line(frame, red_center, (new_x, new_y), (255, 0, 0), 2)

        if len(green_patches) > 0 and len(red_patches) > 0 and len(orng_patches) > 0:
            green_center = green_patches[0]
            red_center = red_patches[0]
            orng_center = orng_patches[0]

            # Calculate the slope of the extended line
            slope_extended_line = (orng_center[1] - red_center[1]) / (orng_center[0] - red_center[0])

            # Calculate the y-coordinate of the extended line at the x-coordinate of the left side of the green rectangle
            extended_line_y_at_green_left = int(
                slope_extended_line * (green_center[0] - min_size / 2 - red_center[0]) + red_center[1])

            # Calculate the y-coordinate of the extended line at the x-coordinate of the right side of the green rectangle
            extended_line_y_at_green_right = int(
                slope_extended_line * (green_center[0] + min_size / 2 - red_center[0]) + red_center[1])

            # Check if the extended line passes through the vertical boundaries of the green rectangle
            if (
                    min(green_center[1] - min_size / 2,
                        green_center[1] + min_size / 2) < extended_line_y_at_green_left < max(
                green_center[1] - min_size / 2, green_center[1] + min_size / 2) or
                    min(green_center[1] - min_size / 2,
                        green_center[1] + min_size / 2) < extended_line_y_at_green_right < max(
                green_center[1] - min_size / 2, green_center[1] + min_size / 2)
            ):
                cv2.putText(frame, "Intersection Detected!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                            2)
                values="100,300"
                # You can add additional actions or logic here when an intersection is detected

        # Check if green and red patches align horizontally
        if abs(green_patches[0][1] - red_patches[0][1]) < 69:
            # Draw a line between the centers of green and red patches
            cv2.line(frame, green_patches[0], red_patches[0], (255, 255, 255), 2)

        # Display the distance and position on the frame
        cv2.putText(frame, f"Distance: {distance:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Position: {position}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Check if the distance is minimal, then reset the motor values
        if distance < min_distance:
            values = "1,1"

    # Convert the frame back to RGB for display
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return rgb_frame,position


cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open camera.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Detect and draw large green objects in the frame (larger than 5x5 pixels)
    output_frame, position = detect_and_draw_green_and_red_patches(frame, min_size=10, min_distance=100)

    # Send the motor values to the server
    s.send((values + '\n').encode())

    # Display the resulting frame with the detected green objects
    cv2.imshow('Large Green Object Detection', output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()


s.close()
