import cv2
import numpy as np

for i in range(1,11):

    # Load the document image
    img_path = f'sample_images/{i}.png'
    img = cv2.imread(img_path)

    if img is None:
        print(f"{i}.png not found.")
        continue

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Morphological Closing to remove small gaps
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find the document boundary (largest contour)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print(f"No contour found in {i}.png")
        continue

    largest_contour = max(contours, key=cv2.contourArea)

    # Draw the boundary on the original image
    cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 2)

    # Save the final output
    cv2.imwrite(f"output_images/output_{i}.jpg", img)

print("Done!")