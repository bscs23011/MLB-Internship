import cv2
import numpy as np

image1 = cv2.imread('3.png')
image2 = cv2.imread('4.png')
image3 = cv2.imread('9.png')    



# Convert an image to grayscale.
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)


# Apply Gaussian Blur before edge detection.
image1 = cv2.GaussianBlur(image1, (5, 5), 0)
image2 = cv2.GaussianBlur(image2, (5, 5), 0)
image3 = cv2.GaussianBlur(image3, (5, 5), 0)

# Detect edges using:
   
# Sobel
sobelx = cv2.Sobel(image2, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(image2, cv2.CV_64F, 0, 1, ksize=3)
sobel = np.sqrt(sobelx**2 + sobely**2)

cv2.imshow('Original Image 1', image1)
cv2.imshow('Sobel Edge Detection', sobel)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Laplacian
laplacian = cv2.Laplacian(image3, cv2.CV_64F)

cv2.imshow('Original Image 2', image2)
cv2.imshow('Laplacian Edge Detection', laplacian)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Canny
canny = cv2.Canny(image3, 100, 200)
cv2.imshow('Original Image 3', image3)
cv2.imshow('Canny Edge Detection', canny)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Compare the output of all three edge detection methods.
# Apply each morphological operation separately.
# Compare the images before and after applying morphological operations.