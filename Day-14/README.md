1. Difference between BGR and RGB
RGB stands for Red, Green, Blue and is the standard color format used by most image processing libraries and display systems.
BGR stands for Blue, Green, Red and is the default color format used by OpenCV.
Both formats contain the same three color channels, but the order of the channels is different. Using the wrong format can cause colors to appear incorrect

2. What grayscale images are and why they are used
A grayscale image contains only one channel that represents the intensity or brightness of each pixel, ranging from 0 (black) to 255 (white).
Since it does not store color information, it requires less memory and processing power.
Grayscale images are commonly used in image processing tasks such as edge detection, object detection, thresholding, and feature extraction because they simplify computations while preserving important visual details.

3. Which OpenCV functions you used
cv2.imread() – Load an image.
cv2.imshow() – Display the image.
cv2.waitKey() – Wait for a key press before closing the image window.
cv2.destroyAllWindows() – Close all OpenCV windows.
cv2.cvtColor() – Convert the image to grayscale.
cv2.resize() – Resize the image.
cv2.rotate() – Rotate the image.
cv2.flip() – Flip the image horizontally or vertically.
cv2.rectangle() – Draw a rectangle.
cv2.circle() – Draw a circle.
cv2.line() – Draw a line.
cv2.polylines() – Draw a polygon.
cv2.putText() – Add custom text to the image.
cv2.imwrite() – Save the processed image.

4. Challenges:
Drawing the shape where i exactly wanted.
Knowing the coordinates of the image
