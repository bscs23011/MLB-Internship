What are contours?

Contours are the boundaries or outlines of objects in an image. They are formed by connecting all the continuous points that have the same intensity or color, allowing OpenCV to identify the shape and size of an object.
Contours are typically detected on binary images, where the object is white (foreground) and the background is black. 
Once detected, contours can be used to calculate various properties such as area, perimeter, bounding rectangles, enclosing circles, and to classify different geometric shapes.

How contour detection works.

Load the image using OpenCV.
Convert the image to grayscale to simplify processing.
Apply thresholding to convert the grayscale image into a binary image, separating the object from the background.
Find contours using cv2.findContours(), which traces the boundaries of all white objects.
Approximate the contour using cv2.approxPolyDP() to reduce unnecessary points while preserving the overall shape.
Analyze the contour by calculating:
Area using cv2.contourArea()
Perimeter using cv2.arcLength()
Bounding rectangle using cv2.boundingRect()
Aspect ratio to distinguish between squares and rectangles.
Classify the shape based on the number of vertices and geometric properties.
Draw the contour and label the detected shape on the original image.

Which shapes your program can detect.

Triangle (3 vertices)
Square (4 vertices with aspect ratio close to 1)
Rectangle (4 vertices with aspect ratio different from 1)
Pentagon (5 vertices)
Hexagon (6 vertices)
Heptagon (7 vertices)
Octagon (8 vertices)
Polygons (more than 8 vertices)
Circle (identified using circularity or a high number of contour points)

Any challenges you faced.
Low-contrast images: When the object and background had similar grayscale values, contour detection became inaccurate. This was improved using contrast enhancement techniques such as CLAHE and histogram equalization.
Noise: Small unwanted white regions produced extra contours with very small areas (sometimes even area = 0). This was solved by applying Gaussian Blur and filtering contours based on a minimum area threshold.
