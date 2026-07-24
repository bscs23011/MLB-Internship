import cv2
import math

# Load an image.
# Detect all shapes present.
# Draw contours around each shape.
# Label each detected shape (Circle, Rectangle, Square, Triangle, etc.).
# Display the area and perimeter of each shape.
# Save the final output image.

for i in range(1,11):
    image  = cv2.imread(f'sample-images/{i}.png')
    cv2.imshow('Original Image', image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Image', image)

    # Apply thresholding.

    #simple thresholding
    # _, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    #adaptive thresholding
    # threshold = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    #otsu's thresholding
    _, threshold = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )


    # Detect contours.
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw all contours on the image.
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    # Calculate the area and perimeter of each contour.
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        print(f"Contour Area: {area}, Contour Perimeter: {perimeter}")
        circularity = (4 * math.pi * area) / (perimeter * perimeter)


    # Draw a bounding rectangle around each detected object.
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imwrite(f'contour-detection-images/output_{i}.png', image)


    # Detect simple shapes such as circles, rectangles, squares, and triangles.
    if len(contours) > 0:
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            x, y, w, h = cv2.boundingRect(approx)
            if circularity > 0.8:
                shape_name = "Circle"
            elif len(approx) == 3:
                shape_name = "Triangle"
            elif len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                    shape_name = "Square"
                else:
                    shape_name = "Rectangle"
            elif len(approx) == 5:
                shape_name = "Pentagon"
            elif len(approx) == 6:
                shape_name = "Hexagon"
            elif len(approx) == 7:
                shape_name = "Heptagon"
            elif len(approx) == 8:
                shape_name = "Octagon"
            else:
                shape_name = f"{len(approx)}-sided Polygon"    

            cv2.putText(image, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Save all output images.
    cv2.imwrite(f'final-images/output_{i}.png', image)