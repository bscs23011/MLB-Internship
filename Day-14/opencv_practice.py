import cv2
import numpy as np

# Read an image and display its dimensions, number of channels, and file size.
image = cv2.imread('image2.PNG')
print("Image dimensions:", image.shape)
print("Number of channels:", image.shape[2])
print("File size:", image.nbytes, "bytes")

# Convert a color image to grayscale.
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize an image to different resolutions.
resized_image = cv2.resize(image, (400, 400))
cv2.imwrite('output/resized_image.png', resized_image)

# Crop different regions of an image.
croped = image[50:200, 100:300] 
cv2.imwrite('output/cropped_image.png', croped)

# Rotate the image by 90°, 180°, and 270°.
rotated_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
rotated_180 = cv2.rotate(image, cv2.ROTATE_180)
rotated_270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

cv2.imwrite('output/rotated_90.png', rotated_90)
cv2.imwrite('output/rotated_180.png', rotated_180)
cv2.imwrite('output/rotated_270.png', rotated_270)

# Flip the image horizontally and vertically.
flip_h = cv2.flip(image, 1)
flip_v = cv2.flip(image, 0)

cv2.imwrite('output/flip_horizontal.png', flip_h)
cv2.imwrite('output/flip_vertical.png', flip_v)

# Draw:
   
# Rectangle
rectangle_image = image.copy()
cv2.rectangle(rectangle_image, (50, 50), (200, 200), (0, 255, 0), 3)
cv2.imwrite('output/rectangle_image.png', rectangle_image)

# Circle
circle_image = image.copy()
cv2.circle(circle_image, (150, 150), 50, (255, 0, 0), -1)
cv2.imwrite('output/circle_image.png', circle_image)

# Line
line_image = image.copy()
cv2.line(line_image, (0, 0), (300, 300), (0, 0, 255), 5)
cv2.imwrite('output/line_image.png', line_image)

# Polygon
polygon_image = image.copy()
cv2.polylines(polygon_image, [np.array([[100, 100], [200, 50], [300, 100], [250, 200], [150, 200]])], isClosed=True, color=(0, 255, 255), thickness=3)
cv2.imwrite('output/polygon_image.png', polygon_image)

# Add custom text (your name and today's date) on the image.
text_image = image.copy()
text = "Hassan , 7/20/2026"
cv2.putText(text_image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.imwrite('output/text_image.png', text_image)

# Save all processed images into an output folder.
