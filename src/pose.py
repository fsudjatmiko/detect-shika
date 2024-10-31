import cv2
import os
import numpy as np

# Directory containing images
image_dir = "./images"

# Define color ranges for different body parts in HSV
color_ranges = {
    "head": ([0, 30, 60], [20, 150, 255]),  # Adjusted skin color range
    "shirt": ([0, 0, 200], [180, 50, 255]),  # White color range
    "pants": ([100, 150, 0], [140, 255, 255]),  # Blue color range
}

# Iterate over all images in the directory
for image_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_name)
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    keypoints = []

    # Detect key points for each body part based on color
    for part, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv_image, lower, upper)

        # Find contours for the masked image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Calculate the centroid of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                keypoints.append((cX, cY))
                cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

    # Draw skeleton (lines between key points)
    if len(keypoints) >= 7:
        # Example: Draw lines between some key points to form a simplified skeleton
        cv2.line(image, keypoints[0], keypoints[1], (255, 0, 0), 2)  # Head to shoulder
        cv2.line(image, keypoints[1], keypoints[2], (255, 0, 0), 2)  # Shoulder to elbow
        cv2.line(image, keypoints[2], keypoints[3], (255, 0, 0), 2)  # Elbow to wrist
        cv2.line(image, keypoints[1], keypoints[4], (255, 0, 0), 2)  # Shoulder to hip
        cv2.line(image, keypoints[4], keypoints[5], (255, 0, 0), 2)  # Hip to knee
        cv2.line(image, keypoints[5], keypoints[6], (255, 0, 0), 2)  # Knee to ankle

    # Display the output image
    cv2.imshow("Output-Keypoints", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()