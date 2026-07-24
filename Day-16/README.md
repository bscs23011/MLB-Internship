1. Difference between Sobel, Laplacian, and Canny
Sobel Operator
Sobel detects edges by calculating the gradient (change in pixel intensity) in the horizontal and vertical directions.
It uses two filters: one for horizontal edges and one for vertical edges.
It provides information about the direction of edges.
It is simple and fast but is sensitive to image noise.
Laplacian Operator
Laplacian detects edges by calculating the second derivative of the image intensity.
It detects edges in all directions rather than only horizontal or vertical.
It highlights regions where the intensity changes rapidly.
It is more sensitive to noise than Sobel, so it is usually applied after Gaussian Blur.
Canny Edge Detection
Canny is a multi-stage edge detection algorithm that includes noise reduction, gradient calculation, non-maximum suppression, double thresholding, and edge tracking.
It produces thin, continuous, and accurate edges.
It is less affected by noise compared to Sobel and Laplacian.
It is widely used because it provides the best balance between accuracy and noise removal.

2. Purpose of Each Morphological Operation
Erosion
Removes small white noise by shrinking white objects.
Helps separate connected objects.
Dilation
Expands white objects.
Fills small gaps and connects broken edges.
Opening
Performs erosion followed by dilation.
Removes small white noise while preserving the shape of larger objects.
Closing
Performs dilation followed by erosion.
Fills small holes and gaps in objects and connects broken edges.
Morphological Gradient
Calculates the difference between the dilated and eroded images.
Highlights the boundaries of objects.
Top Hat
Calculates the difference between the original image and its opening.
Highlights small bright objects and fine details.
Black Hat
Calculates the difference between the closing and the original image.
Highlights small dark objects or dark regions.

3. Which Combination of Techniques Gave the Best Results

The best results for document boundary detection were obtained using:
Grayscale Conversion – Simplified the image by removing color information.
Gaussian Blur – Reduced image noise before edge detection.
Canny Edge Detection – Produced clear and accurate document edges.
Morphological Closing – Connected broken edges and filled small gaps.
Largest Contour Detection – Identified the document boundary by selecting the contour with the largest area.

This combination produced cleaner edges and more reliable contour detection than using Sobel or Laplacian alone.

4. Challenges Faced While Detecting Document Boundaries
Some images did not have a clear visible border around the document, making it difficult to detect the actual page boundary.
In some cases, the largest contour detected was around the text instead of the document because the page edges were not clearly visible.
Choosing suitable Canny threshold values required experimentation. Low thresholds detected too much noise, while high thresholds missed important edges.
Small gaps in the detected edges sometimes prevented a complete document contour, which was improved using the Morphological Closing operation.
Image noise and uneven lighting also affected edge detection, making Gaussian Blur necessary before applying Canny.
